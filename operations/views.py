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
from rest_framework.permissions import IsAuthenticated
class AtamaViewSet(viewsets.ModelViewSet):
    queryset = Atama.objects.all().order_by('-atama_tarih_saat') # Atamalar modelinin queryset'ini belirledik
    serializer_class = AtamaSerializer # Atama Serializer'ını kullandık
    permission_classes = [IsAuthenticated] # Yetkilendirme sınıfını belirledik
    # İleride özel aksiyonlar (örneğin atama belgesi oluşturma gibi) buraya eklenebilir.
class FirmaViewSet(viewsets.ModelViewSet):
    queryset = Firma.objects.all().order_by('firma_adi')
    serializer_class = FirmaSerializer
    permission_classes = [IsAuthenticated] # <- Burayı değiştirdik

class AracSahibiViewSet(viewsets.ModelViewSet):
    queryset = AracSahibi.objects.all().order_by('adi_soyadi')
    serializer_class = AracSahibiSerializer
    permission_classes = [IsAuthenticated] # <- Burayı değiştirdik

# Diğer tüm ViewSet'ler için aynı değişikliği yapın:
class AracViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [IsAuthenticated]

class NakliyeKaydiViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [IsAuthenticated]

class AracViewSet(viewsets.ModelViewSet):
    queryset = Arac.objects.all().order_by('plaka') # <- Bu satırın doğru yazıldığından emin olun
    serializer_class = AracSerializer
    permission_classes = [IsAuthenticated]

class IrsaliyeKaydiViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [IsAuthenticated]

class TeslimEvragiViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [IsAuthenticated]

class GiderKategoriViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [IsAuthenticated]

class OtherGiderViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [IsAuthenticated]

class EFaturaViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [IsAuthenticated]

class TahsilatViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [IsAuthenticated]

class OdemeViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [IsAuthenticated]