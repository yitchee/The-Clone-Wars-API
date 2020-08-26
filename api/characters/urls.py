from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='characters_index'),
    path('random/', views.RandomCharacterView.as_view(), name='characters_random'),
    path('<int:id>/', views.CharacterIdView.as_view(), name='characters_id'),
]