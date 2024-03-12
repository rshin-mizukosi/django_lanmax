from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='monitoramento_nfe_index'),
    path('api/nfe-erro/', views.api_nfe_erro, name='monitoramento_nfe_api_nfe_erro'),
]