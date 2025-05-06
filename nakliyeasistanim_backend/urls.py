from django.contrib import admin
from django.urls import path, include

# simplejwt view'larını import ediyoruz
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # simplejwt URL'leri
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Token almak için (login endpoint'i)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Token yenilemek için

    # API endpoint'lerimiz
    path('api/', include('operations.urls')),
]