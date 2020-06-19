from django.contrib import admin
from django.urls import path, include
from dataviz_api import urls as dataviz_api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(dataviz_api_urls)),
]
