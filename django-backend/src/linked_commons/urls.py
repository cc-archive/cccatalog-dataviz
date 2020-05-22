from django.contrib import admin
from django.urls import path, include
from api import urls as apiUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(apiUrls)),
]
