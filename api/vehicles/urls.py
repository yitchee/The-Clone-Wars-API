from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='vehicles_index'),
    path('random/', views.RandomVehicleView.as_view(), name='vehicles_random'),
    path('<int:id>/', views.VehicleIdView.as_view(), name='vehicles_id'),
]