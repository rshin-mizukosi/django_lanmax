from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('mercos/', include('apps.mercos.urls')),
    path('gnre/<str:db>/', include('apps.gnre.urls')),
    path('sintegra/', include('apps.sintegra.urls')),
]