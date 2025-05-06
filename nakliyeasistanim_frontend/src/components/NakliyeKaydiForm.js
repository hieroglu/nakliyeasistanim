import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Nakliye Durumları için seçenek listesi (Modellerden gelmeli ama şimdilik manuel yazalım)
const NAKLIYE_STATUS_CHOICES = [
    { value: 'Yeni', label: 'Yeni Kayıt' },
    { value: 'Atandı', label: 'Araca Atandı' },
    { value: 'Yolda', label: 'Yolda' },
    { value: 'Teslim Edildi', label: 'Teslim Edildi' },
    { value: 'Faturalandı', label: 'Faturalandırıldı' },
    { value: 'Tahsil Edildi', label: 'Tahsil Edildi' },
    { value: 'Kapandı', label: 'Kapandı' },
    { value: 'İptal Edildi', label: 'İptal Edildi' },
];
// İleride bu veriler de backend'den çekilebilir veya sabit bir dosyada tutulabilir.


function NakliyeKaydiForm() {
  // Form alanları için state
  const [formData, setFormData] = useState({
    firma_id: '', // İlişkili firma ID'si
    takip_no: '',
    yuk_adi: '',
    nakliye_tipi: '',
    miktar: '',
    agirlik: '',
    hacim_ebat: '',
    yukleme_adresi: '',
    yukleme_tarih_saat: '',
    bosaltma_adresi: '',
    bosaltma_tarih_saat: '',
    anlasilan_bedel: '',
    ek_masraflar_firma: '',
    odeme_vadesi: '',
    aciklamalar: '',
    // Durum alanı backend tarafından otomatik 'Yeni' olarak atanabilir.
    // isterseniz formda da seçenek olarak sunabilirsiniz.
    // durum: 'Yeni',
  });

  // Firma seçimi için firmaları çekmemiz gerekiyor
  const [firmalar, setFirmalar] = useState([]);
  const [loadingFirmalar, setLoadingFirmalar] = useState(true);
  const [errorFirmalar, setErrorFirmalar] = useState(null);

  // Form gönderildikten sonra durum bilgisi
  const [submitStatus, setSubmitStatus] = useState(null); // 'success', 'error', null

  // Firmaları çekmek için useEffect (Component ilk yüklendiğinde)
  useEffect(() => {
    async function fetchFirmalar() {
      try {
        const response = await axios.get('/api/firmalar/');
        // Sadece işi veren firmaları (müşterileri) filtreleyebiliriz, Firma modelinde 'firma_tipi' eklemiştik
        // Eğer Firma modelinde firma_tipi kullanılıyorsa:
        // const musteriFirmalar = response.data.filter(f => f.firma_tipi === 'Musteri');
        // setFirmalar(musteriFirmalar);
        setFirmalar(response.data); // Şimdilik tüm firmaları listeyelim
        setLoadingFirmalar(false);
      } catch (error) {
        setErrorFirmalar(error);
        setLoadingFirmalar(false);
        console.error("Firmalar çekilirken hata oluştu:", error);
      }
    }
    fetchFirmalar();
  }, []); // Boş dependency array

  // Form alanları değiştiğinde state'i güncelle
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData, // Mevcut form datasını kopyala
      [name]: value, // Değişen alanı yeni değerle güncelle
    });
  };

  // Form gönderildiğinde
  const handleSubmit = async (e) => {
    e.preventDefault(); // Sayfanın yeniden yüklenmesini engelle

    // Göndermeden önce veri formatlarını kontrol etme (tarihler, sayılar)
    // Örneğin, tarih alanlarını Date objesine veya string formatına dönüştürmeniz gerekebilir
    // API'ye göndereceğiniz format DRF serializer'ınıza uygun olmalı.
    // Django DateTimeField için ISO 8601 formatı (YYYY-MM-DDTHH:MM:SSZ) genellikle uygundur.
    // DateField için YYYY-MM-DD.
    const dataToSend = {
        ...formData,
        // Tarih/Saat alanlarını uygun formata dönüştürme (örnek)
        // yukleme_tarih_saat: formData.yukleme_tarih_saat ? new Date(formData.yukleme_tarih_saat).toISOString() : null,
        // bosaltma_tarih_saat: formData.bosaltma_tarih_saat ? new Date(formData.bosaltma_tarih_saat).toISOString() : null,
        // Sayı alanlarını Number'a dönüştürme (input'tan string gelir)
        anlasilan_bedel: formData.anlasilan_bedel ? parseFloat(formData.anlasilan_bedel) : null,
        ek_masraflar_firma: formData.ek_masraflar_firma ? parseFloat(formData.ek_masraflar_firma) : null,
        agirlik: formData.agirlik ? parseFloat(formData.agirlik) : null,
        // İlişkili ID alanının Number olduğundan emin olun
        firma_id: formData.firma_id ? parseInt(formData.firma_id) : null,
    };


    try {
      // API'ye POST isteği gönderiyoruz
      const response = await axios.post('/api/nakliye-kayitlari/', dataToSend);

      console.log("Nakliye Kaydı başarıyla eklendi:", response.data);
      setSubmitStatus('success');
      // Formu temizle (isteğe bağlı)
      setFormData({
        firma_id: '', takip_no: '', yuk_adi: '', nakliye_tipi: '', miktar: '',
        agirlik: '', hacim_ebat: '', yukleme_adresi: '', yukleme_tarih_saat: '',
        bosaltma_adresi: '', bosaltma_tarih_saat: '', anlasilan_bedel: '',
        ek_masraflar_firma: '', odeme_vadesi: '', aciklamalar: '',
      });
      // Başarı mesajını 3 saniye sonra kaldır
      setTimeout(() => setSubmitStatus(null), 3000);

    } catch (error) {
      console.error("Nakliye Kaydı eklenirken hata oluştu:", error.response ? error.response.data : error.message);
      setSubmitStatus('error');
       // Hata mesajını 5 saniye sonra kaldır
      setTimeout(() => setSubmitStatus(null), 5000);
    }
  };

   if (loadingFirmalar) {
    return <div>Firmalar yükleniyor... (Nakliye kaydı eklemek için gerekli)</div>;
  }

  if (errorFirmalar) {
    return <div>Firmalar yüklenirken bir hata oluştu, nakliye kaydı eklenemiyor: {errorFirmalar.message}</div>;
  }


  return (
    <div>
      <h2>Yeni Nakliye Kaydı Ekle</h2>

      {/* Başarı veya hata mesajları */}
      {submitStatus === 'success' && <p style={{color: 'green'}}>Nakliye Kaydı başarıyla eklendi!</p>}
      {submitStatus === 'error' && <p style={{color: 'red'}}>Nakliye Kaydı eklenirken hata oluştu.</p>}


      <form onSubmit={handleSubmit}>
        {/* Firma Seçimi Dropdown */}
        <div>
          <label htmlFor="firma_id">İşi Veren Firma:</label>
          <select
            id="firma_id"
            name="firma_id"
            value={formData.firma_id}
            onChange={handleChange}
            required // Bu alan zorunlu
          >
            <option value="">-- Firma Seçin --</option>
            {firmalar.map(firma => (
              <option key={firma.id} value={firma.id}>
                {firma.firma_adi} ({firma.vkn_tckn})
              </option>
            ))}
          </select>
        </div>

        {/* Diğer Form Alanları */}
        <div>
          <label htmlFor="takip_no">Takip Numarası:</label>
          <input type="text" id="takip_no" name="takip_no" value={formData.takip_no} onChange={handleChange} required />
        </div>

         <div>
          <label htmlFor="yuk_adi">Yük Adı/Tanımı:</label>
          <input type="text" id="yuk_adi" name="yuk_adi" value={formData.yuk_adi} onChange={handleChange} required />
        </div>

        <div>
          <label htmlFor="nakliye_tipi">Nakliye Tipi:</label>
          <input type="text" id="nakliye_tipi" name="nakliye_tipi" value={formData.nakliye_tipi} onChange={handleChange} />
        </div>

        <div>
          <label htmlFor="miktar">Miktar:</label>
          <input type="text" id="miktar" name="miktar" value={formData.miktar} onChange={handleChange} />
        </div>

        <div>
          <label htmlFor="agirlik">Ağırlık (Ton):</label>
          <input type="number" step="0.01" id="agirlik" name="agirlik" value={formData.agirlik} onChange={handleChange} />
        </div>

        <div>
          <label htmlFor="hacim_ebat">Hacim/Ebat Bilgisi:</label>
          <input type="text" id="hacim_ebat" name="hacim_ebat" value={formData.hacim_ebat} onChange={handleChange} />
        </div>

        <div>
          <label htmlFor="yukleme_adresi">Yükleme Adresi:</label>
          <textarea id="yukleme_adresi" name="yukleme_adresi" value={formData.yukleme_adresi} onChange={handleChange} required />
        </div>

        <div>
          <label htmlFor="yukleme_tarih_saat">Yükleme Tarih ve Saat:</label>
          {/* datetime-local input türü hem tarih hem saat seçimi için uygundur */}
          <input type="datetime-local" id="yukleme_tarih_saat" name="yukleme_tarih_saat" value={formData.yukleme_tarih_saat} onChange={handleChange} required />
        </div>

        <div>
          <label htmlFor="bosaltma_adresi">Boşaltma Adresi:</label>
          <textarea id="bosaltma_adresi" name="bosaltma_adresi" value={formData.bosaltma_adresi} onChange={handleChange} required />
        </div>

        <div>
          <label htmlFor="bosaltma_tarih_saat">Boşaltma Tarih ve Saat:</label>
          {/* datetime-local input türü hem tarih hem saat seçimi için uygundur */}
          <input type="datetime-local" id="bosaltma_tarih_saat" name="bosaltma_tarih_saat" value={formData.bosaltma_tarih_saat} onChange={handleChange} required />
        </div>

        <div>
          <label htmlFor="anlasilan_bedel">Anlaşılan Nakliye Bedeli (TL):</label>
          <input type="number" step="0.01" id="anlasilan_bedel" name="anlasilan_bedel" value={formData.anlasilan_bedel} onChange={handleChange} required />
        </div>

         <div>
          <label htmlFor="ek_masraflar_firma">Ek Masraflar (Firmadan alınacak - TL):</label>
          <input type="number" step="0.01" id="ek_masraflar_firma" name="ek_masraflar_firma" value={formData.ek_masraflar_firma} onChange={handleChange} />
        </div>

        <div>
          <label htmlFor="odeme_vadesi">Ödeme Vadesi (Firmadan):</label>
          {/* date input türü sadece tarih seçimi için uygundur */}
          <input type="date" id="odeme_vadesi" name="odeme_vadesi" value={formData.odeme_vadesi} onChange={handleChange} />
        </div>

        <div>
          <label htmlFor="aciklamalar">Açıklamalar:</label>
          <textarea id="aciklamalar" name="aciklamalar" value={formData.aciklamalar} onChange={handleChange} />
        </div>

        {/* Durum alanı backend tarafından otomatik atandığı için forma eklemedik */}

        <button type="submit">Nakliye Kaydını Ekle</button>
      </form>
    </div>
  );
}

export default NakliyeKaydiForm;