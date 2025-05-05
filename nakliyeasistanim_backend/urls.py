from django.contrib import admin
from django.urls import path, include # include'u import ettiğinizden emin olun

urlpatterns = [
    path('admin/', admin.site.urls),
    # API endpoint'leri için yeni path ekliyoruz
    path('api/', include('operations.urls')), # operations uygulamasının URL'lerini /api/ altına dahil et
]