from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('characters/', include('api.characters.urls')),
    path('planets/', include('api.planets.urls')),
    path('species/', include('api.species.urls')),
    path('vehicles/', include('api.vehicles.urls')),
]