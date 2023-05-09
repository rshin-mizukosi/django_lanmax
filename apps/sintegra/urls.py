from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='sintegra_index'),
    path('consulta/', views.consulta, name='sintegra_consulta'),
]