from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('fiches/', include('fiches.urls')),
    path('accounts/', include('accounts.urls')),
]
