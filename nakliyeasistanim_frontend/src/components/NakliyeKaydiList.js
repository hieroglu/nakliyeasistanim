import React, { useState, useEffect } from 'react';
import axios from 'axios';

function NakliyeKaydiList() {
  const [nakliyeler, setNakliyeler] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
              {/* İleride detay/düzenle butonları eklenebilir */}
            </tr>
          </thead>
          <tbody>
            {nakliyeler.map(nakliye => (
              <tr key={nakliye.id}>
                <td>{nakliye.takip_no}</td>
                {/* firma ilişkisi detail geldiği için firma.firma_adi diyebiliriz */}
                <td>{nakliye.firma ? nakliye.firma.firma_adi : 'Bilinmiyor'}</td>
                <td>{nakliye.yuk_adi}</td>
                <td>{nakliye.anlasilan_bedel} TL</td>
                <td>{nakliye.durum}</td>
                <td>{new Date(nakliye.olusturma_tarihi).toLocaleDateString()}</td> {/* Tarihi formatlayalım */}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default NakliyeKaydiList;