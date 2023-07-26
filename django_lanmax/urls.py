from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('mercos/', include('apps.mercos.urls')),
    path('gnre/<str:db>/', include('apps.gnre.urls')),
    path('sintegra/', include('apps.sintegra.urls')),
    path('email/<str:db>/', include('apps.email_lanmax.urls')),
]