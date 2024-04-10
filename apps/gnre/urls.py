from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='gnre_index'),
    path('libera-pagto/', views.libera_pagto, name='gnre_libera_pagto'),
    path('api/gnre-nao-liberadas/', views.api_gnre_nao_liberadas, name='gnre_api_gnre_nao_liberadas'),
]