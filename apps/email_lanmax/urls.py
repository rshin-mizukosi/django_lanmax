from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='email_lanmax_index'),
    path('send-email', views.send_email, name='email_lanmax_send_email'),
    path('gera-gnre-email', views.gera_gnre_email, name='email_lanmax_gera_gnre_email'),
]