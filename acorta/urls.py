from django.urls import path, re_path
from . import views

urlpatterns = [
    path('<int:numero>', views.number, name='number'),
    path('', views.index, name='index'),
    re_path(r'.', views.error, name='error'),
]