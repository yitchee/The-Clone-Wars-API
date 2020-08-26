from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='planets_index'),
    path('random/', views.RandomPlanetView.as_view(), name='planets_random'),
    path('<int:id>/', views.PlanetIdView.as_view(), name='planets_id'),
]