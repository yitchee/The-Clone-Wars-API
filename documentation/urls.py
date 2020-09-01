from django.urls import path
from . import views


urlpatterns = [
    path('', views.DocumentationView.as_view(), name='documentation_view'),
]