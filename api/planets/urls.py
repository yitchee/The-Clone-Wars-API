from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='planets_index'),
    path('random', views.planets_random, name='planets_random'),
    path('<int:id>/', views.planets_id, name='planets_id'),
]