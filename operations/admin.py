from django.contrib import admin
# Mevcut import listesine yenilerini ekleyin:
from .models import (
    Firma, AracSahibi, Arac, NakliyeKaydi, Atama,
    IrsaliyeKaydi, TeslimEvragi, EFatura,
    GiderKategori, OtherGider, Tahsilat, Odeme
)
# Modelleri yönetim paneline kaydediyoruz
admin.site.register(Firma)
admin.site.register(AracSahibi)
admin.site.register(Arac)
admin.site.register(NakliyeKaydi)
admin.site.register(Atama)
admin.site.register(IrsaliyeKaydi) # Yeni
admin.site.register(TeslimEvragi) # Yeni
admin.site.register(EFatura) # Yeni
admin.site.register(GiderKategori) # Yeni
admin.site.register(OtherGider) # Yeni
admin.site.register(Tahsilat) # Yeni
admin.site.register(Odeme) # Yeni