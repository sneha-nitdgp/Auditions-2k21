
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('response/',include('response.urls')),
    path('administrator/',include('administrator.urls')),
]
