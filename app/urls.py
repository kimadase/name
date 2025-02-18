from django.conf.urls.static import static
from django.urls import path

from akinatorproject import settings
from app.views import IndexPage
from app.views import GamePage

app_name = 'akinator'

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('game/', GamePage.as_view(), name='game'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
