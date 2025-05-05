# Mevcut import listesini güncelleyin, yeni modelleri ve serializer'ları ekleyin:
from rest_framework import viewsets
from .models import (
    Firma, AracSahibi, Arac, NakliyeKaydi, Atama,
    IrsaliyeKaydi, TeslimEvragi, EFatura, # Yeni Modeller
    GiderKategori, OtherGider, Tahsilat, Odeme # Yeni Modeller
)
from .serializers import (
    FirmaSerializer, AracSahibiSerializer, AracSerializer, NakliyeKaydiSerializer, AtamaSerializer,
    IrsaliyeKaydiSerializer, TeslimEvragiSerializer, EFaturaSerializer, # Yeni Serializer'lar
    GiderKategoriSerializer, OtherGiderSerializer, TahsilatSerializer, OdemeSerializer # Yeni Serializer'lar
)
from rest_framework.permissions import AllowAny # İzin yönetimi için (şimdilik AllowAny kullanacağız)

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
    
class IrsaliyeKaydiViewSet(viewsets.ModelViewSet):
    queryset = IrsaliyeKaydi.objects.all().order_by('-irsaliye_tarihi')
    serializer_class = IrsaliyeKaydiSerializer
    permission_classes = [AllowAny] # GEÇİCİ: Canlıda IsAuthenticated olmalı

# Modül 3 için: Teslim Evrağı ViewSet
class TeslimEvragiViewSet(viewsets.ModelViewSet):
    queryset = TeslimEvragi.objects.all().order_by('-teslim_tarih_saat')
    serializer_class = TeslimEvragiSerializer
    permission_classes = [AllowAny] # GEÇİCİ: Canlıda IsAuthenticated olmalı


# Modül 5 için: Gider Kategorisi ViewSet
class GiderKategoriViewSet(viewsets.ModelViewSet):
    queryset = GiderKategori.objects.all().order_by('ad')
    serializer_class = GiderKategoriSerializer
    permission_classes = [AllowAny] # GEÇİCİ: Canlıda IsAuthenticated olmalı

# Modül 5 için: Diğer Gider ViewSet
class OtherGiderViewSet(viewsets.ModelViewSet):
    queryset = OtherGider.objects.all().order_by('-tarih')
    serializer_class = OtherGiderSerializer
    permission_classes = [AllowAny] # GEÇİCİ: Canlıda IsAuthenticated olmalı


# Modül 4 için: E-Fatura ViewSet
class EFaturaViewSet(viewsets.ModelViewSet):
    queryset = EFatura.objects.all().order_by('-fatura_tarihi')
    serializer_class = EFaturaSerializer
    permission_classes = [AllowAny] # GEÇİCİ: Canlıda IsAuthenticated olmalı
    # Not: E-Fatura gönderme/alma işlemleri için custom bir action (metot) eklenmesi gerekecek.
    # Bu, entegratör API'si ile konuşacak Viewset içinde ayrı bir fonksiyon olacak.
    # Örn: @action(detail=True, methods=['post']) def send_to_gib(self, request, pk=None): ...


# Modül 5 için: Tahsilat ViewSet
class TahsilatViewSet(viewsets.ModelViewSet):
    queryset = Tahsilat.objects.all().order_by('-tarih')
    serializer_class = TahsilatSerializer
    permission_classes = [AllowAny] # GEÇİCİ: Canlıda IsAuthenticated olmalı

# Modül 5 için: Ödeme ViewSet
class OdemeViewSet(viewsets.ModelViewSet):
    queryset = Odeme.objects.all().order_by('-tarih')
    serializer_class = OdemeSerializer
    permission_classes = [AllowAny] # GEÇİÇİ: Canlıda IsAuthenticated olmalı