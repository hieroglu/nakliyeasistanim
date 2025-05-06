import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function NakliyeKaydiList() {
  const [nakliyeler, setNakliyeler] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // useNavigate, yönlendirme için kullanılır

   const handleDelete = async (id) => {
      // Kullanıcıdan onay al (isteğe bağlı ama önerilir)
      const isConfirmed = window.confirm("Bu nakliye kaydını silmek istediğinizden emin misiniz?");
      if (!isConfirmed) {
          return; // Kullanıcı iptal ettiyse işlemi durdur
      }

      try {
          // API'ye DELETE isteği gönder
          await axios.delete(`/api/nakliye-kayitlari/${id}/`);

          // Silme başarılı olursa, frontend listeyi güncelle
          // Silinen öğeyi state'ten filtreleyerek yeni bir liste oluştur
          setNakliyeler(nakliyeler.filter(nakliye => nakliye.id !== id));
          console.log(`Nakliye kaydı (ID: ${id}) başarıyla silindi.`);
          // Başarı mesajı gösterebilirsiniz
      } catch (error) {
          console.error(`Nakliye kaydı (ID: ${id}) silinirken hata oluştu:`, error.response ? error.response.data : error.message);
          // Hata mesajı gösterebilirsiniz
      }
  };

  // ... (Loading/Error durumları)



  useEffect(() => {
    async function fetchNakliyeler() {
      try {
        // Nakliye Kayıtları API endpoint'ine GET isteği
        const response = await axios.get('/api/nakliye-kayitlari/');
        // Gelen veriyi state'e kaydediyoruz
        setNakliyeler(response.data);
        setLoading(false);
      } catch (error) {
        setError(error);
        setLoading(false);
        console.error("Nakliye kayıtları çekilirken hata oluştu:", error);
      }
    }

    fetchNakliyeler();
  }, []); // Boş dependency array, sadece ilk render'da çalışır

  if (loading) {
    return <div>Nakliye kayıtları yükleniyor...</div>;
  }

  if (error) {
    return <div>Nakliye kayıtları yüklenirken bir hata oluştu: {error.message}</div>;
  }

  return (
    <div>
      <h2>Nakliye Kayıtları Listesi</h2>
      {/* Eğer nakliye kaydı yoksa paragrafı göster, varsa tabloyu göster */}
      {nakliyeler.length === 0 ? (
          <p>Henüz nakliye kaydı bulunmamaktadır.</p>
      ) : (
        // PROBLEM YARATAN YORUM SATIRI BURADAN KALDIRILDI
        <table>
              <thead>
      <tr>
        <th>Takip No</th>
        <th>Firma</th>
        <th>Yük</th>
        <th>Anlaşılan Bedel</th>
        <th>Durum</th>
        <th>Oluşturma Tarihi</th>
        <th>İşlemler</th> {/* Yeni sütun */}
      </tr>
    </thead>
    <tbody>
      {nakliyeler.map(nakliye => (
        <tr key={nakliye.id}>
          <td>{nakliye.takip_no}</td>
          <td>{nakliye.firma ? nakliye.firma.firma_adi : 'Bilinmiyor'}</td>
          <td>{nakliye.yuk_adi}</td>
          <td>{nakliye.anlasilan_bedel} TL</td>
          <td>{nakliye.durum}</td>
          <td>{new Date(nakliye.olusturma_tarihi).toLocaleDateString()}</td>
          <td>
            {/* Düzenle Butonu - İlgili nakliye kaydının düzenleme sayfasına yönlendirecek */}
            {/* URL yapısı: /nakliyeler/:id/duzenle */}
            <button onClick={() => navigate(`/nakliyeler/${nakliye.id}/duzenle`)} style={{ marginRight: '10px' }}>Düzenle</button>
            {/* Sil Butonu - handle Sil fonksiyonunu çağıracak */}
            <button onClick={() => handleDelete(nakliye.id)}>Sil</button>
          </td> {/* İşlemler sütunu içeriği */}
        </tr>
      ))}
    </tbody>
        </table>
      )}
    </div>
  );
}

export default NakliyeKaydiList;