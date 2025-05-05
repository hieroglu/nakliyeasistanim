from rest_framework import serializers
from .models import Firma, AracSahibi, Arac, NakliyeKaydi, Atama

# Firma Modeli için Serializer
class FirmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firma
        fields = '__all__' # Modeldeki tüm alanları API'ye dahil et

# Araç Sahibi Modeli için Serializer
class AracSahibiSerializer(serializers.ModelSerializer):
    class Meta:
        model = AracSahibi
        fields = '__all__'

# Araç Modeli için Serializer
class AracSerializer(serializers.ModelSerializer):
    # Sahibi bilgisi sadece ID yerine daha fazla detayla gelsin istersek
    # sahibi = AracSahibiSerializer(read_only=True)
    class Meta:
        model = Arac
        fields = '__all__'
        # 'sahibi' alanının sadece okunur olmasını ve detaylı gelmesini istersek
        # fields = ['id', 'plaka', 'arac_turu', 'model_yili', 'sasi_no', 'sigorta_bitis_tarihi', 'muayene_bitis_tarihi', 'sahibi']


# Nakliye Kaydı Modeli için Serializer
class NakliyeKaydiSerializer(serializers.ModelSerializer):
    # İlişkili Firma bilgisini detaylı getirmek için
    firma = FirmaSerializer(read_only=True) # Sadece okunur, firma detayları gelir
    firma_id = serializers.PrimaryKeyRelatedField(queryset=Firma.objects.all(), source='firma', write_only=True) # Firma ID'si ile kayıt/güncelleme yapabilmek için

    class Meta:
        model = NakliyeKaydi
        # Firma detayını ve firma_id'yi kullanabilmek için alanları manuel belirtiyoruz
        fields = ['id', 'firma', 'firma_id', 'takip_no', 'yuk_adi', 'nakliye_tipi', 'miktar', 'agirlik', 'hacim_ebat',
                  'yukleme_adresi', 'yukleme_tarih_saat', 'bosaltma_adresi', 'bosaltma_tarih_saat',
                  'anlasilan_bedel', 'ek_masraflar_firma', 'odeme_vadesi', 'aciklamalar', 'durum', 'olusturma_tarihi']
        read_only_fields = ['olusturma_tarihi', 'durum'] # Bu alanlar otomatik oluşacak/güncellenecek, API ile direkt değiştirilmesin


# Atama Modeli için Serializer
class AtamaSerializer(serializers.ModelSerializer):
    # İlişkili Nakliye Kaydı, Araç ve Araç Sahibi bilgilerini detaylı getirmek için
    nakliye_kaydi = NakliyeKaydiSerializer(read_only=True)
    atanan_arac = AracSerializer(read_only=True)
    atanan_arac_sahibi = AracSahibiSerializer(read_only=True)

    # İlişkili ID'ler ile kayıt/güncelleme yapabilmek için
    nakliye_kaydi_id = serializers.PrimaryKeyRelatedField(queryset=NakliyeKaydi.objects.all(), source='nakliye_kaydi', write_only=True)
    atanan_arac_id = serializers.PrimaryKeyRelatedField(queryset=Arac.objects.all(), source='atanan_arac', write_only=True)
    atanan_arac_sahibi_id = serializers.PrimaryKeyRelatedField(queryset=AracSahibi.objects.all(), source='atanan_arac_sahibi', write_only=True)


    class Meta:
        model = Atama
        fields = ['id', 'nakliye_kaydi', 'nakliye_kaydi_id', 'atanan_arac', 'atanan_arac_id',
                  'atanan_arac_sahibi', 'atanan_arac_sahibi_id', 'anlasilan_arac_bedeli',
                  'ek_masraflar_arac', 'atama_tarih_saat', 'talimat_notlari']
        read_only_fields = ['atama_tarih_saat'] # Otomatik oluşacak