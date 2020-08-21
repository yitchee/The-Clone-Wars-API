from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='characters_index'),
    path('random/', views.characters_random, name='characters_random'),
    path('<int:id>/', views.characters_id, name='characters_id'),
]