import json
from random import shuffle
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpRequest
from django.views.generic import TemplateView
from django.shortcuts import render
from app import models

class IndexPage(TemplateView):
    template_name = 'app/templates/index.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        return render(request, self.template_name)


class GamePage(TemplateView):
    template_name = 'app/templates/game.html'


    def post(self, request: WSGIRequest, *args, **kwargs):
        body = json.loads(request.body)
        if body['stage'] == 'begin-year':
            return JsonResponse({
                'question': 'Когда началась загаданная вами битва?',
                'choices': models.GPWBattle.objects.unique_beginning_years()
            })
        elif body['stage'] == 'end-year':
            request.session['begin-year'] = int(body['begin_year'])
            return JsonResponse({
                'question': 'Когда закончилась загаданная вами битва?',
                'choices': models.GPWBattle.objects.unique_ending_years_by_begin_year(int(body['begin_year']))
            })
        elif body['stage'] == 'location':
            request.session['end-year'] = int(body['end_year'])
            correct_locations = models.GPWBattle.objects.get_location_by_date(
                int(request.session['begin-year']),
                int(request.session['end-year']),
            )
            other_locations = models.GPWBattle.objects.get_location()
            shuffle(other_locations)
            other_locations = [x for x in other_locations if x not in correct_locations]
            prepared_locations = correct_locations + other_locations[:4 - len(correct_locations)]
            shuffle(prepared_locations)
            return JsonResponse({
                'question': 'Где была загаданная вами битва?',
                'choices': prepared_locations
            })
        elif body['stage'] == 'ussr-general':
            request.session['location'] = body['location']
            correct_glavkoms = models.GPWBattle.objects.get_ussr_general_by_filter(
                int(request.session['begin-year']),
                int(request.session['end-year']),
                request.session['location']
            )
            other_glavkoms = models.GPWBattle.objects.get_ussr_general()
            shuffle(other_glavkoms)
            other_glavkoms = [x for x in other_glavkoms if x not in correct_glavkoms]
            prepared_glavkoms = correct_glavkoms + other_glavkoms[:4 - len(correct_glavkoms)]
            shuffle(prepared_glavkoms)
            return JsonResponse({
                'question': 'Кто командовал советскими войсками?',
                'choices': prepared_glavkoms
            })
        elif body['stage'] == 'germ-general':
            request.session['ussr_glavkom'] = body['ussr_glavkom']
            correct_glavkoms = models.GPWBattle.objects.get_germ_general_by_filter(
                int(request.session['begin-year']),
                int(request.session['end-year']),
                request.session['location']
            )
            other_glavkoms = models.GPWBattle.objects.get_germ_general()
            shuffle(other_glavkoms)
            other_glavkoms = [x for x in other_glavkoms if x not in correct_glavkoms]
            prepared_glavkoms = correct_glavkoms + other_glavkoms[:4 - len(correct_glavkoms)]
            shuffle(prepared_glavkoms)
            return JsonResponse({
                'question': 'Кто командовал немецкими войсками?',
                'choices': prepared_glavkoms
            })
        elif body['stage'] == 'result':
            request.session['germ_glavkom'] = body['germ_glavkom']
            battles = models.GPWBattle.objects.get_battle(
                int(request.session['begin-year']),
                int(request.session['end-year']),
                request.session['location'],
                request.session['ussr_glavkom'],
                request.session['germ_glavkom'],
            )
            if len(battles) > 0:
                return JsonResponse({
                'question': f'Ваша битва: {", ".join(battles)}'
            })
            else:
                return JsonResponse({
                    'question': 'Я не знаю такой битвы('
                })

        return JsonResponse({'message': 'arbuz'})


    def get(self, request: WSGIRequest, *args, **kwargs):
        return render(request, self.template_name)
