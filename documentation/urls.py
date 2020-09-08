from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.DocumentationView.as_view(), name='documentation_view'),
    re_path(r'^.*$', views.DocumentationView.as_view(), name='documentation_view')
]