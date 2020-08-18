from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='species_index'),
]