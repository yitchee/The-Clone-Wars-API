from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='characters_index'),
    re_path(r'random/?', views.RandomCharacterView.as_view(), name='characters_random'),
    re_path(r'^(?P<id>\d+)/?$', views.CharacterIdView.as_view(), name='characters_id'),
]