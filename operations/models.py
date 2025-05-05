from django.db import models

# Helper Choices
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
ODEME_YONTEM_CHOICES = [
    ('Nakit', 'Nakit'),
    ('BankHavaleEFT', 'Banka Havalesi/EFT'),
    ('Cek', 'Çek'),
    ('Senet', 'Senet'),
    ('Diger', 'Diğer'),
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
EFATURA_DURUM_CHOICES = [
    ('Taslak', 'Taslak'),
    ('Gonderildi', 'GİB\'e Gönderildi'),
    ('GIB Hata', 'GİB Hata'), # GİB'den dönen hatalar
    ('Aliciya Iletildi', 'Aliciya Iletildi'), # Alıcının posta kutusuna ulaştı
    ('Kabul Edildi', 'Alıcı Tarafından Kabul Edildi'),
    ('Reddedildi', 'Alıcı Tarafından Reddedildi'),
    ('Iptal Edildi', 'İptal Edildi'), # E-Fatura İptal / İptal Portalı Süreci
    ('Muhasebelestirildi', 'Muhasebeleştirildi'), # Modül 5 ile entegrasyon için
]

FATURA_YON_CHOICES = [
    ('Giden', 'Giden (Satış)'),
    ('Gelen', 'Gelen (Alış/Gider)'),
]

# Yeni eklendi
FIRMA_TIP_CHOICES = [
    ('Musteri', 'Müşteri (İş Veren)'),
    ('Tedarikci', 'Tedarikçi (Diğer Hizmetler)'),
    ('AracSahibi', 'Araç Sahibi (Tırcı)'), # Tırcıları ayrı bir tip olarak işaretleyelim
    ('Diger', 'Diğer'),
]

# Modül 1 & 5 için temel: Firmalar (Hem müşteriler hem de tedarikçiler olabilir)
class Firma(models.Model):
    firma_adi = models.CharField(max_length=200, verbose_name="Firma Adı")
    vkn_tckn = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="VKN/TCKN") # Vergi Kimlik No / TC Kimlik No
    firma_tipi = models.CharField(max_length=20, choices=FIRMA_TIP_CHOICES, default='Musteri', verbose_name="Firma Tipi") # Yeni alan
    adres = models.TextField(null=True, blank=True, verbose_name="Adres")
    telefon = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefon")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="Email")
    # is_musteri ve is_tedarikci alanları yerine firma_tipi kullanabiliriz. İsterseniz silebilirsiniz veya şimdilik durabilir.
    # is_musteri = models.BooleanField(default=True, verbose_name="Müşteri mi?")
    # is_tedarikci = models.BooleanField(default=False, verbose_name="Tedarikçi mi?")

    def __str__(self):
        return self.firma_adi

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmalar"

# Diğer mevcut modeller (AracSahibi, Arac, NakliyeKaydi, Atama) aşağıda devam ediyor...


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
# Modül 3 için: Belge Yönetimi
class IrsaliyeKaydi(models.Model):
    # Hangi nakliye kaydına ait?
    nakliye_kaydi = models.ForeignKey(NakliyeKaydi, on_delete=models.CASCADE, related_name='irsaliyeler', verbose_name="Nakliye Kaydı")
    irsaliye_no = models.CharField(max_length=100, verbose_name="İrsaliye Numarası")
    irsaliye_tarihi = models.DateField(verbose_name="İrsaliye Tarihi")
    duzenleyen_firma_adi = models.CharField(max_length=200, verbose_name="Düzenleyen Firma Adı") # Yük sahibi firma adı
    belge_dosyasi = models.FileField(upload_to='irsaliyeler/', null=True, blank=True, verbose_name="Belge Dosyası/Görseli") # Dosyaların nereye yükleneceği

    aciklamalar = models.TextField(null=True, blank=True, verbose_name="Açıklamalar")
    kayit_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    def __str__(self):
        return f"İrsaliye {self.irsaliye_no} ({self.nakliye_kaydi.takip_no})"

    class Meta:
        verbose_name = "İrsaliye Kaydı"
        verbose_name_plural = "İrsaliye Kayıtları"
        ordering = ['-irsaliye_tarihi']


class TeslimEvragi(models.Model):
    # Hangi nakliye kaydına ait?
    nakliye_kaydi = models.ForeignKey(NakliyeKaydi, on_delete=models.CASCADE, related_name='teslim_evraklari', verbose_name="Nakliye Kaydı")
    teslim_tarih_saat = models.DateTimeField(verbose_name="Teslim Tarih ve Saat")
    teslim_alan_adi = models.CharField(max_length=200, verbose_name="Teslim Alan Kişi/Firma Adı")
    belge_dosyasi = models.FileField(upload_to='teslim_evraklari/', null=True, blank=True, verbose_name="Belge Dosyası/Görseli") # Dosyaların nereye yükleneceği

    aciklamalar = models.TextField(null=True, blank=True, verbose_name="Açıklamalar")
    kayit_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    def __str__(self):
        return f"Teslim Evrağı ({self.nakliye_kaydi.takip_no})"

    class Meta:
        verbose_name = "Teslim Evrağı"
        verbose_name_plural = "Teslim Evrakları"
        ordering = ['-teslim_tarih_saat']
        # Modül 4 için: E-Fatura Kaydı (Giden ve Gelen)
class EFatura(models.Model):
    # Faturanın yönü (Giden mi, Gelen mi?)
    fatura_yonu = models.CharField(max_length=10, choices=FATURA_YON_CHOICES, verbose_name="Fatura Yönü")

    # Yasal Fatura Bilgileri
    fatura_uuid = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Fatura UUID") # GİB'den gelen/giden unique ID
    fatura_numarasi = models.CharField(max_length=50, verbose_name="Fatura Numarası") # Belge numarası
    fatura_tarihi = models.DateField(verbose_name="Fatura Tarihi")
    fatura_vadesi = models.DateField(null=True, blank=True, verbose_name="Fatura Vadesi")

    # Taraflar
    # Fatura Giden ise, kesen biziz (sistem kullanıcısı), alan Firma (Müşteri)
    # Fatura Gelen ise, kesen Firma (Tedarikci/AracSahibi), alan biziz (sistem kullanıcısı)
    # Basitlik için, faturayı kesen ve alan tarafların VKN/TCKN'lerini ve Adlarını tutalım.
    # İleride Firma modeli ile doğrudan ilişkilendirme yapılabilir (ForeignKey).
    # Şu an için direkt VKN/TCKN ve Ad soyad/unvan tutmak, gelen faturalarda tırcı/firma ayrımını kolaylaştırabilir.
    gonderen_vkn_tckn = models.CharField(max_length=20, verbose_name="Gönderen VKN/TCKN")
    gonderen_adi_unvani = models.CharField(max_length=200, verbose_name="Gönderen Adı/Unvanı")
    alan_vkn_tckn = models.CharField(max_length=20, verbose_name="Alan VKN/TCKN")
    alan_adi_unvani = models.CharField(max_length=200, verbose_name="Alan Adı/Unvanı")


    # Finansal Bilgiler
    mal_hizmet_toplami = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Mal/Hizmet Toplamı (KDV Hariç)")
    toplam_kdv = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Toplam KDV")
    toplam_tevkifat = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Toplam Tevkifat") # Varsa
    fatura_toplami = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fatura Toplamı (KDV Dahil)")
    odenecek_tutar = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ödenecek/Tahsil Edilecek Tutar") # Tevkifat vs. sonrası kalan

    # İlişkiler
    # Giden Fatura ise hangi Nakliye Kayıtları ile ilgili? (Birden çok olabilir)
    ilgili_nakliye_kayitlari = models.ManyToManyField(NakliyeKaydi, related_name='faturalar', blank=True, verbose_name="İlgili Nakliye Kayıtları (Giden Fatura İçin)")
    # Gelen Fatura ise hangi Atamalar ile ilgili? (Birden çok olabilir, özellikle tırcı faturası)
    ilgili_atamalar = models.ManyToManyField(Atama, related_name='gelen_faturalar', blank=True, verbose_name="İlgili Atamalar (Gelen Fatura İçin)")


    # E-Fatura Durum ve Dosya Bilgileri
    durum = models.CharField(max_length=50, choices=EFATURA_DURUM_CHOICES, default='Taslak', verbose_name="E-Fatura Durumu")
    xml_dosyasi = models.FileField(upload_to='efaturalar/xml/', null=True, blank=True, verbose_name="E-Fatura XML Dosyası")
    pdf_dosyasi = models.FileField(upload_to='efaturalar/pdf/', null=True, blank=True, verbose_name="E-Fatura PDF Dosyası") # GİB/Entegratör'den gelen görsel
    gib_yaniti_xml = models.FileField(upload_to='efaturalar/yanit/', null=True, blank=True, verbose_name="GİB Yanıt XML Dosyası") # Kabul/Red yanıtı vb.


    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    def __str__(self):
        yon = "Giden" if self.fatura_yonu == 'Giden' else "Gelen"
        return f"{yon} Fatura {self.fatura_numarasi} ({self.fatura_tarihi})"

    class Meta:
        verbose_name = "E-Fatura"
        verbose_name_plural = "E-Faturalar"
        ordering = ['-fatura_tarihi', '-olusturma_tarihi']
        # Fatura Numarası + Gönderen VKN/TCKN veya Alan VKN/TCKN kombinasyonu unique olabilir,
        # ancak basitlik için şimdilik sadece fatura_uuid'yi unique tuttuk.
        # Modül 5 için: Gider Kategorileri (Diğer Giderler için)
class GiderKategori(models.Model):
    ad = models.CharField(max_length=100, unique=True, verbose_name="Gider Kategorisi Adı")

    def __str__(self):
        return self.ad

    class Meta:
        verbose_name = "Gider Kategorisi"
        verbose_name_plural = "Gider Kategorileri"


# Modül 5 için: Diğer Giderler (E-Fatura ile belgelenmeyen veya farklı türdeki giderler)
class OtherGider(models.Model):
    kategori = models.ForeignKey(GiderKategori, on_delete=models.SET_NULL, null=True, blank=True, related_name='giderleri', verbose_name="Kategori")
    tutar = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tutar")
    tarih = models.DateField(verbose_name="Tarih")
    aciklama = models.TextField(verbose_name="Açıklama")
    belge_dosyasi = models.FileField(upload_to='diger_giderler/', null=True, blank=True, verbose_name="Belge (Makbuz vb.)") # Makbuz vb. belgesi

    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    def __str__(self):
        return f"Gider ({self.tarih}) - {self.tutar} TL"

    class Meta:
        verbose_name = "Diğer Gider"
        verbose_name_plural = "Diğer Giderler"
        ordering = ['-tarih']


# Modül 5 için: Tahsilat Kaydı (Firmalardan alınan ödemeler)
class Tahsilat(models.Model):
    firma = models.ForeignKey(Firma, on_delete=models.PROTECT, related_name='tahsilatlar', verbose_name="Tahsilat Yapılan Firma") # Kimden tahsilat yapıldı?
    ilgili_faturalar = models.ManyToManyField(EFatura, related_name='tahsilatlar', blank=True, verbose_name="İlgili Faturalar") # Hangi fatura/faturalarla ilgili?

    tutar = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tahsilat Tutarı")
    tarih = models.DateField(verbose_name="Tahsilat Tarihi")
    odeme_yontemi = models.CharField(max_length=50, choices=ODEME_YONTEM_CHOICES, verbose_name="Ödeme Yöntemi")
    aciklama = models.TextField(null=True, blank=True, verbose_name="Açıklama")

    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    def __str__(self):
        return f"Tahsilat ({self.tarih}) - {self.tutar} TL - {self.firma.firma_adi}"

    class Meta:
        verbose_name = "Tahsilat"
        verbose_name_plural = "Tahsilatlar"
        ordering = ['-tarih']


# Modül 5 için: Ödeme Kaydı (Tırcılara veya diğer tedarikçilere yapılan ödemeler)
class Odeme(models.Model):
    firma = models.ForeignKey(Firma, on_delete=models.PROTECT, related_name='odemeler', verbose_name="Ödeme Yapılan Firma/Tedarikçi") # Kime ödeme yapıldı?
    ilgili_faturalar = models.ManyToManyField(EFatura, related_name='odemeler', blank=True, verbose_name="İlgili Faturalar") # Hangi fatura/faturalarla ilgili? (Genellikle Gelen Faturalar)

    tutar = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ödeme Tutarı")
    tarih = models.DateField(verbose_name="Ödeme Tarihi")
    odeme_yontemi = models.CharField(max_length=50, choices=ODEME_YONTEM_CHOICES, verbose_name="Ödeme Yöntemi")
    aciklama = models.TextField(null=True, blank=True, verbose_name="Açıklama")

    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")


    def __str__(self):
        return f"Ödeme ({self.tarih}) - {self.tutar} TL - {self.firma.firma_adi}"

    class Meta:
        verbose_name = "Ödeme"
        verbose_name_plural = "Ödemeler"
        ordering = ['-tarih']