from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='species_index'),
    re_path(r'random/?', views.RandomSpeciesView.as_view(), name='species_random'),
    re_path(r'^(?P<id>\d+)/?$', views.SpeciesIdView.as_view(), name='species_id'),
]