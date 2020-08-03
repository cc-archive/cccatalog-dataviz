from django.contrib import admin
from django.urls import path, include
from linked_commons import urls as linked_commons_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(linked_commons_urls)),
]
