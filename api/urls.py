from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('', views.index.as_view(), name='index'),
    re_path(r'characters/?', include('api.characters.urls')),
    re_path(r'planets/?', include('api.planets.urls')),
    re_path(r'species/?', include('api.species.urls')),
    re_path(r'vehicles/?', include('api.vehicles.urls')),
]