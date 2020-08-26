from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='species_index'),
    path('random/', views.RandomSpeciesView.as_view(), name='species_random'),
    path('<int:id>/', views.SpeciesIdView.as_view(), name='species_id'),
]