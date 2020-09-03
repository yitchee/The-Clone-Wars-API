from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='vehicles_index'),
    re_path(r'random/?', views.RandomVehicleView.as_view(), name='vehicles_random'),
    re_path(r'^(?P<id>\d+)/?$', views.VehicleIdView.as_view(), name='vehicles_id'),
]