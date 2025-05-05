from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FirmaViewSet, AracSahibiViewSet, AracViewSet, NakliyeKaydiViewSet, AtamaViewSet,
    IrsaliyeKaydiViewSet, TeslimEvragiViewSet, EFaturaViewSet, # Yeni ViewSet'ler
    GiderKategoriViewSet, OtherGiderViewSet, TahsilatViewSet, OdemeViewSet # Yeni ViewSet'ler
)
# DRF DefaultRouter kullanarak ViewSet'ler için otomatik URL'ler oluşturuyoruz
router = DefaultRouter()
router.register(r'firmalar', FirmaViewSet)
router.register(r'arac-sahipleri', AracSahibiViewSet)
router.register(r'araclar', AracViewSet)
router.register(r'nakliye-kayitlari', NakliyeKaydiViewSet)
router.register(r'atamalar', AtamaViewSet)
router.register(r'irsaliye-kayitlari', IrsaliyeKaydiViewSet) # Yeni Kayıt
router.register(r'teslim-evraklari', TeslimEvragiViewSet) # Yeni Kayıt
router.register(r'gider-kategorileri', GiderKategoriViewSet) # Yeni Kayıt
router.register(r'diger-giderler', OtherGiderViewSet) # Yeni Kayıt
router.register(r'efaturalar', EFaturaViewSet) # Yeni Kayıt
router.register(r'tahsilatlar', TahsilatViewSet) # Yeni Kayıt
router.register(r'odemeler', OdemeViewSet) # Yeni Kayıt


urlpatterns = [
    # Router tarafından oluşturulan URL'leri dahil ediyoruz
    path('', include(router.urls)),
]