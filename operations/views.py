from rest_framework import viewsets
from .models import Firma, AracSahibi, Arac, NakliyeKaydi, Atama
from .serializers import FirmaSerializer, AracSahibiSerializer, AracSerializer, NakliyeKaydiSerializer, AtamaSerializer
from rest_framework.permissions import AllowAny # İzin yönetimi için (şimdilik AllowAny kullanacağız)
# İleride IsAuthenticated gibi izinler kullanılacak


# Firma Modeli için ViewSet
class FirmaViewSet(viewsets.ModelViewSet):
    queryset = Firma.objects.all().order_by('firma_adi') # Hangi veriyi çekeceğimizi ve sıralamasını belirtiyoruz
    serializer_class = FirmaSerializer # Hangi serializer'ı kullanacağını belirtiyoruz
    permission_classes = [AllowAny] # API'ye kimlerin erişebileceği (şimdilik herkese açık)

# Araç Sahibi Modeli için ViewSet
class AracSahibiViewSet(viewsets.ModelViewSet):
    queryset = AracSahibi.objects.all().order_by('adi_soyadi')
    serializer_class = AracSahibiSerializer
    permission_classes = [AllowAny]

# Araç Modeli için ViewSet
class AracViewSet(viewsets.ModelViewSet):
    queryset = Arac.objects.all().order_by('plaka')
    serializer_class = AracSerializer
    permission_classes = [AllowAny]

# Nakliye Kaydı Modeli için ViewSet
class NakliyeKaydiViewSet(viewsets.ModelViewSet):
    queryset = NakliyeKaydi.objects.all().order_by('-olusturma_tarihi')
    serializer_class = NakliyeKaydiSerializer
    permission_classes = [AllowAny]

# Atama Modeli için ViewSet
class AtamaViewSet(viewsets.ModelViewSet):
    queryset = Atama.objects.all().order_by('-atama_tarih_saat')
    serializer_class = AtamaSerializer
    permission_classes = [AllowAny]