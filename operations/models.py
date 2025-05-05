from django.db import models

# Helper Choices (Modellerde kullanılacak seçenekler)
NAKLIYE_STATUS_CHOICES = [
    ('Yeni', 'Yeni Kayıt'),
    ('Atandı', 'Araca Atandı'),
    ('Yolda', 'Yolda'),
    ('Teslim Edildi', 'Teslim Edildi'),
    ('Faturalandı', 'Faturalandırıldı'),
    ('Tahsil Edildi', 'Tahsil Edildi'),
    ('Kapandı', 'Kapandı'),
    ('İptal Edildi', 'İptal Edildi'),
]

ARAC_TUR_CHOICES = [
    ('Tır', 'Tır'),
    ('Kamyon', 'Kamyon'),
    ('Kamyonet', 'Kamyonet'),
    ('Tenteli', 'Tenteli Dorse'),
    ('Acik', 'Açık Dorse'),
    ('SalKasa', 'Sal Kasa Dorse'),
    ('Lowbed', 'Lowbed Dorse'),
    ('Diger', 'Diğer'),
]

# Modül 1 & 5 için temel: Firmalar (Hem müşteriler hem de tedarikçiler olabilir)
class Firma(models.Model):
    firma_adi = models.CharField(max_length=200, verbose_name="Firma Adı")
    vkn_tckn = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="VKN/TCKN") # Vergi Kimlik No / TC Kimlik No
    adres = models.TextField(null=True, blank=True, verbose_name="Adres")
    telefon = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefon")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="Email")
    # İleride müşteri mi, tedarikçi mi, ikisi birden mi gibi ayrım yapılabilir
    is_musteri = models.BooleanField(default=True, verbose_name="Müşteri mi?") # Nakliye işi veriyorsa
    is_tedarikci = models.BooleanField(default=False, verbose_name="Tedarikçi mi?") # Bize fatura kesiyorsa (Tırcılar da tedarikçi)

    def __str__(self):
        return self.firma_adi

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmalar"


# Modül 2 için: Araç Sahipleri / Tırcılar (Sistemi kullanan nakliyeciye hizmet verenler)
class AracSahibi(models.Model):
    # AracSahibi ya bireysel şahıs ya da şirket olabilir. Temel bilgileri burada tutalım.
    adi_soyadi = models.CharField(max_length=100, verbose_name="Adı Soyadı")
    firma_adi = models.CharField(max_length=200, null=True, blank=True, verbose_name="Firma Adı (Şirketse)")
    vkn_tckn = models.CharField(max_length=20, unique=True, verbose_name="VKN/TCKN") # Unique olmalı
    telefon = models.CharField(max_length=20, verbose_name="Telefon")
    adres = models.TextField(null=True, blank=True, verbose_name="Adres")
    banka_hesap_bilgisi = models.TextField(null=True, blank=True, verbose_name="Banka Hesap Bilgisi (IBAN vb.)")

    def __str__(self):
        return f"{self.adi_soyadi} ({self.firma_adi or 'Şahıs'})"

    class Meta:
        verbose_name = "Araç Sahibi / Tırcı"
        verbose_name_plural = "Araç Sahipleri / Tırcılar"


# Modül 2 için: Araç Bilgileri
class Arac(models.Model):
    plaka = models.CharField(max_length=15, unique=True, verbose_name="Plaka") # Plaka tek olmalı
    arac_turu = models.CharField(max_length=50, choices=ARAC_TUR_CHOICES, verbose_name="Araç Türü")
    model_yili = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Model Yılı")
    sasi_no = models.CharField(max_length=50, null=True, blank=True, verbose_name="Şasi No")
    # Bu araç kime ait? (Kendi aracımızsa AracSahibi boş olabilir, veya sistem kullanıcısı ile ilişkilendirilebilir)
    # Şimdilik harici araçlara odaklanalım ve AracSahibi ile ilişkilendirelim.
    sahibi = models.ForeignKey(AracSahibi, on_delete=models.SET_NULL, null=True, blank=True, related_name='araclari', verbose_name="Sahibi")
    sigorta_bitis_tarihi = models.DateField(null=True, blank=True, verbose_name="Sigorta Bitiş Tarihi")
    muayene_bitis_tarihi = models.DateField(null=True, blank=True, verbose_name="Muayene Bitiş Tarihi")
    # İleride şoför bilgisi de buraya eklenebilir veya ayrı bir modelde tutulabilir.

    def __str__(self):
        return f"{self.plaka} ({self.arac_turu})"

    class Meta:
        verbose_name = "Araç"
        verbose_name_plural = "Araçlar"


# Modül 1 için: Nakliye Kaydı / Sipariş
class NakliyeKaydi(models.Model):
    firma = models.ForeignKey(Firma, on_delete=models.PROTECT, related_name='verilen_nakliyeler', verbose_name="İşi Veren Firma") # Firma silinirse nakliye kaydı silinmesin
    takip_no = models.CharField(max_length=50, unique=True, verbose_name="Takip Numarası") # Otomatik oluşturulabilir ilerde
    yuk_adi = models.CharField(max_length=200, verbose_name="Yük Adı/Tanımı")
    nakliye_tipi = models.CharField(max_length=50, verbose_name="Nakliye Tipi (Komple/Parsiyel vb.)") # İlerde choices olabilir
    miktar = models.CharField(max_length=100, verbose_name="Miktar (örn: 10 Palet)") # Miktar ve birim ayrı alanlar olabilir
    agirlik = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Ağırlık (Ton)") # Veya float olabilir
    hacim_ebat = models.CharField(max_length=200, null=True, blank=True, verbose_name="Hacim/Ebat Bilgisi")
    yukleme_adresi = models.TextField(verbose_name="Yükleme Adresi")
    yukleme_tarih_saat = models.DateTimeField(verbose_name="Yükleme Tarih ve Saat")
    bosaltma_adresi = models.TextField(verbose_name="Boşaltma Adresi")
    bosaltma_tarih_saat = models.DateTimeField(verbose_name="Boşaltma Tarih ve Saat")
    anlasilan_bedel = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Anlaşılan Nakliye Bedeli (Aracının Firmadan alacağı)")
    ek_masraflar_firma = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ek Masraflar (Firmadan alınacak)")
    odeme_vadesi = models.DateField(null=True, blank=True, verbose_name="Ödeme Vadesi (Firmadan)")
    aciklamalar = models.TextField(null=True, blank=True, verbose_name="Açıklamalar")
    durum = models.CharField(max_length=50, choices=NAKLIYE_STATUS_CHOICES, default='Yeni', verbose_name="Durum")
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi") # Kayıt otomatik oluşsun

    def __str__(self):
        return f"NK-{self.takip_no} - {self.firma.firma_adi}"

    class Meta:
        verbose_name = "Nakliye Kaydı"
        verbose_name_plural = "Nakliye Kayıtları"
        ordering = ['-olusturma_tarihi'] # En yeniler üstte görünsün


# Modül 2 için: Atama Bilgisi (Nakliye Kaydının bir araca/şoföre atanması)
class Atama(models.Model):
    nakliye_kaydi = models.ForeignKey(NakliyeKaydi, on_delete=models.CASCADE, related_name='atamalar', verbose_name="Nakliye Kaydı") # Nakliye silinirse atama da silinsin
    atanan_arac = models.ForeignKey(Arac, on_delete=models.PROTECT, related_name='atamalari', verbose_name="Atanan Araç") # Araç silinirse atama silinmesin
    # Şoför bilgisi araç sahibine bağlı veya ayrı bir model olabilir. Basitlik için şimdilik araç sahibiyle ilişkilendirelim.
    atanan_arac_sahibi = models.ForeignKey(AracSahibi, on_delete=models.PROTECT, related_name='verilen_atamalar', verbose_name="Atanan Araç Sahibi / Tırcı") # Araç sahibi silinirse atama silinmesin

    # Aracının tırcıya ödeyeceği bedel
    anlasilan_arac_bedeli = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Anlaşılan Araç Bedeli (Aracının Tırcıya Ödeyeceği)")
    ek_masraflar_arac = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ek Masraflar (Tırcıya ödenecek)")
    atama_tarih_saat = models.DateTimeField(auto_now_add=True, verbose_name="Atama Tarihi ve Saat") # Atama yapıldığında otomatik oluşsun
    talimat_notlari = models.TextField(null=True, blank=True, verbose_name="Talimat Notları") # Atama belgesine yansıyacak notlar

    # İleride bu atama ile ilgili belge (Atama Talimatı PDF'i) alanı eklenebilir.

    def __str__(self):
        return f"Atama: {self.nakliye_kaydi.takip_no} -> {self.atanan_arac.plaka}"

    class Meta:
        verbose_name = "Atama"
        verbose_name_plural = "Atamalar"
        # Bir nakliye kaydına aynı araç/arac sahibi birden fazla atanabilir mi? İş akışına göre karar verilir. Şimdilik izin verelim.

# Not: Modül 3 (Belge Yönetimi), Modül 4 (E-Fatura) ve Modül 5 (Ön Muhasebe) için gerekli modeller (IrsaliyeKaydi, TeslimEvragi, Fatura, Tahsilat, Odeme, Gider) ilerleyen adımlarda tanımlanacaktır.