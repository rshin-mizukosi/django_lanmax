from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='mercos_index'),
    path('atualiza_produtos_mercos/', views.atualiza_produtos_mercos, name='mercos_atualiza_produtos_mercos'),
    path('produtos_lanmax/', views.produtos_lanmax, name='mercos_produtos_lanmax'),
    path('atualiza_produtos_lanmax/', views.atualiza_produtos_lanmax, name='mercos_atualiza_produtos_lanmax'),
]