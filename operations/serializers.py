from rest_framework import serializers
from .models import (
    Firma, AracSahibi, Arac, NakliyeKaydi, Atama,
    IrsaliyeKaydi, TeslimEvragi, EFatura,
    GiderKategori, OtherGider, Tahsilat, Odeme # Yeni eklenen modeller
)



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

class IrsaliyeKaydiSerializer(serializers.ModelSerializer):
    # Nakliye Kaydı ilişkisini detaylı getirmek için (read_only)
    nakliye_kaydi = NakliyeKaydiSerializer(read_only=True)
    # Nakliye Kaydı ID'si ile kayıt/güncelleme yapmak için (write_only)
    nakliye_kaydi_id = serializers.PrimaryKeyRelatedField(queryset=NakliyeKaydi.objects.all(), source='nakliye_kaydi', write_only=True)

    class Meta:
        model = IrsaliyeKaydi
        # İlişkili alanları ve ID alanını fields listesine ekliyoruz
        fields = ['id', 'nakliye_kaydi', 'nakliye_kaydi_id', 'irsaliye_no', 'irsaliye_tarihi',
                  'duzenleyen_firma_adi', 'belge_dosyasi', 'aciklamalar', 'kayit_tarihi']
        read_only_fields = ['kayit_tarihi'] # Bu alan otomatik oluşacak

# Modül 3 için: Teslim Evrağı Serializer
class TeslimEvragiSerializer(serializers.ModelSerializer):
    # Nakliye Kaydı ilişkisini detaylı getirmek için (read_only)
    nakliye_kaydi = NakliyeKaydiSerializer(read_only=True)
    # Nakliye Kaydı ID'si ile kayıt/güncelleme yapmak için (write_only)
    nakliye_kaydi_id = serializers.PrimaryKeyRelatedField(queryset=NakliyeKaydi.objects.all(), source='nakliye_kaydi', write_only=True)

    class Meta:
        model = TeslimEvragi
        # İlişkili alanları ve ID alanını fields listesine ekliyoruz
        fields = ['id', 'nakliye_kaydi', 'nakliye_kaydi_id', 'teslim_tarih_saat', 'teslim_alan_adi',
                  'belge_dosyasi', 'aciklamalar', 'kayit_tarihi']
        read_only_fields = ['kayit_tarihi']


# Modül 5 için: Gider Kategorisi Serializer
class GiderKategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiderKategori
        fields = '__all__' # Tüm alanları dahil et


# Modül 5 için: Diğer Gider Serializer
class OtherGiderSerializer(serializers.ModelSerializer):
    # Kategori ilişkisini detaylı getirmek için (read_only)
    kategori = GiderKategoriSerializer(read_only=True)
    # Kategori ID'si ile kayıt/güncelleme yapmak için (write_only)
    kategori_id = serializers.PrimaryKeyRelatedField(queryset=GiderKategori.objects.all(), source='kategori', write_only=True, allow_null=True, required=False) # Kategori boş bırakılabilir olduğu için

    class Meta:
        model = OtherGider
        # İlişkili alanları ve ID alanını fields listesine ekliyoruz
        fields = ['id', 'kategori', 'kategori_id', 'tutar', 'tarih', 'aciklama',
                  'belge_dosyasi', 'olusturma_tarihi']
        read_only_fields = ['olusturma_tarihi']


# Modül 4 için: E-Fatura Serializer
class EFaturaSerializer(serializers.ModelSerializer):
    # İlişkili Nakliye Kayıtları (ManyToMany) - Okunurken ID listesi gelir
    # Eğer detayları isterseniz, buraya NakliyeKaydiSerializer ekleyebilirsiniz ama ManyToMany için biraz daha karmaşıktır.
    # Basitlik için şimdilik ID listesi yeterli.
    ilgili_nakliye_kayitlari = serializers.PrimaryKeyRelatedField(
        queryset=NakliyeKaydi.objects.all(), many=True, required=False, allow_empty=True
    )
     # İlişkili Atamalar (ManyToMany) - Okunurken ID listesi gelir
    ilgili_atamalar = serializers.PrimaryKeyRelatedField(
        queryset=Atama.objects.all(), many=True, required=False, allow_empty=True
    )


    class Meta:
        model = EFatura
        # Tüm alanları dahil ediyoruz. ManyToMany alanlar default olarak ID listesi olarak okunur.
        fields = '__all__'
        read_only_fields = ['olusturma_tarihi']


# Modül 5 için: Tahsilat Serializer
class TahsilatSerializer(serializers.ModelSerializer):
    # Firma ilişkisini detaylı getirmek için (read_only)
    firma = FirmaSerializer(read_only=True)
    # Firma ID'si ile kayıt/güncelleme yapmak için (write_only)
    firma_id = serializers.PrimaryKeyRelatedField(queryset=Firma.objects.all(), source='firma', write_only=True)

    # İlgili Faturalar (ManyToMany) - Okunurken ID listesi gelir
    ilgili_faturalar = serializers.PrimaryKeyRelatedField(
        queryset=EFatura.objects.all(), many=True, required=False, allow_empty=True
    )

    class Meta:
        model = Tahsilat
        fields = ['id', 'firma', 'firma_id', 'ilgili_faturalar', 'tutar', 'tarih',
                  'odeme_yontemi', 'aciklama', 'olusturma_tarihi']
        read_only_fields = ['olusturma_tarihi']


# Modül 5 için: Ödeme Serializer
class OdemeSerializer(serializers.ModelSerializer):
    # Firma ilişkisini detaylı getirmek için (read_only)
    firma = FirmaSerializer(read_only=True)
    # Firma ID'si ile kayıt/güncelleme yapmak için (write_only)
    firma_id = serializers.PrimaryKeyRelatedField(queryset=Firma.objects.all(), source='firma', write_only=True)

    # İlgili Faturalar (ManyToMany) - Okunurken ID listesi gelir
    ilgili_faturalar = serializers.PrimaryKeyRelatedField(
        queryset=EFatura.objects.all(), many=True, required=False, allow_empty=True
    )

    class Meta:
        model = Odeme
        fields = ['id', 'firma', 'firma_id', 'ilgili_faturalar', 'tutar', 'tarih',
                  'odeme_yontemi', 'aciklama', 'olusturma_tarihi']
        read_only_fields = ['olusturma_tarihi']
    class Meta:
        model = Atama
        fields = ['id', 'nakliye_kaydi', 'nakliye_kaydi_id', 'atanan_arac', 'atanan_arac_id',
                  'atanan_arac_sahibi', 'atanan_arac_sahibi_id', 'anlasilan_arac_bedeli',
                  'ek_masraflar_arac', 'atama_tarih_saat', 'talimat_notlari']
        read_only_fields = ['atama_tarih_saat'] # Otomatik oluşacak

        