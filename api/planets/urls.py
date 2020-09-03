from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='planets_index'),
    re_path(r'random/?', views.RandomPlanetView.as_view(), name='planets_random'),
    re_path(r'^(?P<id>\d+)/?$', views.PlanetIdView.as_view(), name='planets_id'),
]