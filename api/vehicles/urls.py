from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='vehicles_index'),
    path('random', views.vehicles_random, name='vehicles_random'),
]