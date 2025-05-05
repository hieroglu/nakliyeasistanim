from django.contrib import admin
from .models import Firma, AracSahibi, Arac, NakliyeKaydi, Atama

# Modelleri yönetim paneline kaydediyoruz
admin.site.register(Firma)
admin.site.register(AracSahibi)
admin.site.register(Arac)
admin.site.register(NakliyeKaydi)
admin.site.register(Atama)