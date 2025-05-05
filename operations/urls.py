from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FirmaViewSet, AracSahibiViewSet, AracViewSet, NakliyeKaydiViewSet, AtamaViewSet

# DRF DefaultRouter kullanarak ViewSet'ler için otomatik URL'ler oluşturuyoruz
router = DefaultRouter()
router.register(r'firmalar', FirmaViewSet) # /firmalar/ adresinden erisilecek
router.register(r'arac-sahipleri', AracSahibiViewSet) # /arac-sahipleri/ adresinden erisilecek
router.register(r'araclar', AracViewSet) # /araclar/ adresinden erisilecek
router.register(r'nakliye-kayitlari', NakliyeKaydiViewSet) # /nakliye-kayitlari/ adresinden erisilecek
router.register(r'atamalar', AtamaViewSet) # /atamalar/ adresinden erisilecek


urlpatterns = [
    # Router tarafından oluşturulan URL'leri dahil ediyoruz
    path('', include(router.urls)),
]