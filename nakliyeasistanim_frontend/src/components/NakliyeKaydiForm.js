import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

// ... (NAKLIYE_STATUS_CHOICES - still here for form if needed, though backend handles default)

function NakliyeKaydiForm() {
  const { id } = useParams(); // URL'den 'id' parametresini al (düzenleme için)
  const navigate = useNavigate(); // Yönlendirme için

  // Form alanları için state - ID'ye göre başlangıç değerleri ayarlanacak
  const [formData, setFormData] = useState({
    firma_id: '',
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
  });

  // Firma seçimi dropdown'ı için firmalar state'i
  const [firmalar, setFirmalar] = useState([]);

  // Genel yükleme ve hata state'leri (hem firmalar hem nakliye detayı için)
  const [loading, setLoading] = useState(true); // Başlangıçta yükleniyor
  const [error, setError] = useState(null);

  // Form gönderildikten sonra durum bilgisi
  const [submitStatus, setSubmitStatus] = useState(null); // 'success', 'error', null

  // Verileri çekme useEffect'i (Firmaları ve eğer düzenleme modu ise nakliye detayını çeker)
  useEffect(() => {
    async function fetchData() {
        try {
            // 1. Firmaları Çek
            const firmalarResponse = await axios.get('/api/firmalar/');
            setFirmalar(firmalarResponse.data);

            // 2. Eğer düzenleme modu ise (ID varsa) Nakliye Detayını Çek
            if (id) {
                const nakliyeResponse = await axios.get(`/api/nakliye-kayitlari/${id}/`);
                const nakliyeData = nakliyeResponse.data;

                // API'den gelen veriyi form state'ine uygun hale getir ve set et
                setFormData({
                    firma_id: nakliyeData.firma ? nakliyeData.firma.id : '',
                    takip_no: nakliyeData.takip_no || '',
                    yuk_adi: nakliyeData.yuk_adi || '',
                    nakliye_tipi: nakliyeData.nakliye_tipi || '',
                    miktar: nakliyeData.miktar || '',
                    agirlik: nakliyeData.agirlik || '',
                    hacim_ebat: nakliyeData.hacim_ebat || '',
                    yukleme_adresi: nakliyeData.yukleme_adresi || '',
                    // Tarih/Saat dönüşümleri: ISO string -> YYYY-MM-DDTHH:MM (datetime-local input formatı)
                    yukleme_tarih_saat: nakliyeData.yukleme_tarih_saat ? new Date(nakliyeData.yukleme_tarih_saat).toISOString().slice(0, 16) : '',
                    bosaltma_adresi: nakliyeData.bosaltma_adresi || '',
                    bosaltma_tarih_saat: nakliyeData.bosaltma_tarih_saat ? new Date(nakliyeData.bosaltma_tarih_saat).toISOString().slice(0, 16) : '',
                    // Sayı alanları (API number/string dönebilir, input string bekler veya number type ile number dönebilir)
                    anlasilan_bedel: nakliyeData.anlasilan_bedel || '',
                    ek_masraflar_firma: nakliyeData.ek_masraflar_firma || '',
                    agirlik: nakliyeData.agirlik || '',
                    // Tarih dönüşümü: YYYY-MM-DD (API formatı) -> YYYY-MM-DD (date input formatı)
                    odeme_vadesi: nakliyeData.odeme_vadesi || '', // API YYYY-MM-DD formatında geliyorsa direkt kullanılabilir
                    aciklamalar: nakliyeData.aciklamalar || '',
                });
            }

            setLoading(false); // Tüm veriler çekildi (veya çekilmeye çalışıldı)
        } catch (err) {
            setError(err); // Hata durumunda genel hata state'ini ayarla
            setLoading(false);
            console.error("Form verileri çekilirken hata oluştu:", err.response ? err.response.data : err.message);
        }
    }

    fetchData();
     // id değiştiğinde veya component mount olduğunda çalışsın.
     // firmalar state'i burada dependency olmamalı yoksa infinite loop olabilir eğer firma çekme bu state'i tetiklerse.
     // Sadece id'ye bağımlı olması yeterli, firmalar ilk yüklemede çekilir.
  }, [id]); // Dependency array: ID değiştiğinde bu effect tekrar çalışır

  // Form alanları değiştiğinde state'i güncelle
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  // Form gönderildiğinde
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitStatus(null);

    // API'ye gönderilecek datayı hazırla (Sayı ve Tarih/Saat dönüşümleri)
    // Backend serializer'ının beklediği formatlara UYMALIDIR
    const dataToSend = {
        ...formData,
         // Sayı dönüşümleri: String -> Number (Boş string parseFloat ile NaN olur, kontrol etmeli)
        anlasilan_bedel: formData.anlasilan_bedel ? parseFloat(formData.anlasilan_bedel) : null,
        ek_masraflar_firma: formData.ek_masraflar_firma ? parseFloat(formData.ek_masraflar_firma) : null,
        agirlik: formData.agirlik ? parseFloat(formData.agirlik) : null,
         // Firma ID'si dönüşümü: String -> Number
        firma_id: formData.firma_id ? parseInt(formData.firma_id) : null,
         // Tarih/Saat dönüşümleri: YYYY-MM-DDTHH:MM -> ISO 8601 String (YYYY-MM-DDTHH:MM:SS.sssZ)
         // Backend DateTimeField genellikle ISO string kabul eder.
         // Eğer input boşsa null göndermek önemlidir.
        yukleme_tarih_saat: formData.yukleme_tarih_saat ? new Date(formData.yukleme_tarih_saat).toISOString() : null,
        bosaltma_tarih_saat: formData.bosaltma_tarih_saat ? new Date(formData.bosaltma_tarih_saat).toISOString() : null,
        // Ödeme vadesi dönüşümü: YYYY-MM-DD (date input) -> YYYY-MM-DD String (API DateField için)
        // date input zaten doğru formatı veriyorsa dokunmaya gerek yok
        odeme_vadesi: formData.odeme_vadesi || null, // Boşsa null gönder
        aciklamalar: formData.aciklamalar || null, // Boşsa null gönder (TextField null=True ise)
        hacim_ebat: formData.hacim_ebat || null,
        nakliye_tipi: formData.nakliye_tipi || null,
        miktar: formData.miktar || null,
    };


    try {
        // Eğer ID varsa (düzenleme modu) PUT isteği gönder
        if (id) {
            await axios.put(`/api/nakliye-kayitlari/${id}/`, dataToSend);
            console.log("Nakliye Kaydı başarıyla güncellendi.");
            setSubmitStatus('success');
            // Güncelleme sonrası listeleme sayfasına yönlendir
            // Küçük bir gecikme ekleyelim ki kullanıcı mesajı görebilsin
            setTimeout(() => navigate('/nakliyeler'), 1000);

        } else {
            // ID yoksa (yeni kayıt modu) POST isteği gönder
            await axios.post('/api/nakliye-kayitlari/', dataToSend);
            console.log("Nakliye Kaydı başarıyla eklendi.");
            setSubmitStatus('success');
             // Formu temizle
             setFormData({
                firma_id: '', takip_no: '', yuk_adi: '', nakliye_tipi: '', miktar: '',
                agirlik: '', hacim_ebat: '', yukleme_adresi: '', yukleme_tarih_saat: '',
                bosaltma_adresi: '', bosaltma_tarih_saat: '', anlasilan_bedel: '',
                ek_masraflar_firma: '', odeme_vadesi: '', aciklamalar: '',
            });
            // Başarı mesajını 3 saniye sonra kaldır
            setTimeout(() => setSubmitStatus(null), 3000);
        }

    } catch (err) {
        console.error("Nakliye Kaydı işlemi (ekleme/güncelleme) sırasında hata oluştu:", err.response ? err.response.data : err.message);
        setError(err); // Hata durumunda genel hata state'ini ayarla
        setSubmitStatus('error');
         // Hata mesajını 5 saniye sonra kaldır
        setTimeout(() => setSubmitStatus(null), 5000);
    }
  };

   // Eğer veriler çekilirken yükleme yapılıyorsa yükleme mesajı göster
   if (loading) {
       return <div>Yükleniyor...</div>;
   }

   // Eğer veri çekme sırasında hata oluştuysa hata mesajı göster
   if (error) {
       return <div>Veri çekilirken bir hata oluştu: {error.message}</div>;
   }


  return (
    <div>
      {/* Başlık ID'ye göre değişsin */}
      <h2>{id ? 'Nakliye Kaydını Düzenle' : 'Yeni Nakliye Kaydı Ekle'}</h2>

      {/* Başarı veya hata mesajları */}
      {submitStatus === 'success' && <p style={{color: 'green'}}>İşlem başarıyla tamamlandı!</p>} {/* Mesajı genel yaptık */}
      {submitStatus === 'error' && <p style={{color: 'red'}}>İşlem sırasında hata oluştu. {error?.message}</p>} {/* Hata mesajını göster */}


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
            {/* Firmalar yüklenmiş olmalı çünkü loading kontrolünden geçtik */}
            {firmalar.map(firma => (
              <option key={firma.id} value={firma.id}>
                {firma.firma_adi} ({firma.vkn_tckn})
              </option>
            ))}
          </select>
        </div>

        {/* Diğer Form Alanları (Önceki kodla aynı) */}
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

        <button type="submit">{id ? 'Güncelle' : 'Ekle'}</button> {/* Buton yazısı moda göre değişsin */}
        {id && <button type="button" onClick={() => navigate('/nakliyeler')} style={{ marginLeft: '10px' }}>İptal</button>} {/* Düzenleme modundaysa İptal butonu */}
      </form>
    </div>
  );
}

export default NakliyeKaydiForm;