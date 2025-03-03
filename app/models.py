from django.db import models


class GPWManager(models.Manager):
    def unique_beginning_years(self):
        return [d.year for d in self.dates('beginning_battletime', 'year')]

    def unique_ending_years_by_begin_year(self, year):
        return [d.year for d in self.filter(beginning_battletime__year=year).dates('ending_battletime', 'year')]

    def get_location(self):
        return [o.location for o in self.distinct('location')]

    def get_location_by_date(self, begin_year, end_year):
        return [o.location for o in
                self.filter(beginning_battletime__year=begin_year, ending_battletime__year=end_year).distinct(
                    'location')]

    def get_ussr_general(self):
        return [o.ussr_glavkom for o in self.distinct('ussr_glavkom')]

    def get_ussr_general_by_filter(self, begin_year, end_year, location):
        return [o.ussr_glavkom for o in self.filter(
            beginning_battletime__year=begin_year,
            ending_battletime__year=end_year,
            location=location
        ).distinct('ussr_glavkom')]

    def get_germ_general(self):
        return [o.germ_glavkom for o in self.distinct('germ_glavkom')]

    def get_germ_general_by_filter(self, begin_year, end_year, location):
        return [o.germ_glavkom for o in self.filter(
            beginning_battletime__year=begin_year,
            ending_battletime__year=end_year,
            location=location
        ).distinct('germ_glavkom')]

    def get_battle(self, begin_year, end_year, location, ussr_glavkom, germ_glavkom):
        return [o.name for o in self.filter(
            beginning_battletime__year=begin_year,
            ending_battletime__year=end_year,
            location=location,
            ussr_glavkom=ussr_glavkom,
            germ_glavkom=germ_glavkom
        ).distinct('name')]


class GPWBattle(models.Model):
    objects = GPWManager()
    name = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    beginning_battletime = models.DateField(null=True)
    ending_battletime = models.DateField(null=True)
    ussr_glavkom = models.CharField(max_length=255, null=True)
    germ_glavkom = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=4096, null=True)

    def __str__(self):
        return self.name
