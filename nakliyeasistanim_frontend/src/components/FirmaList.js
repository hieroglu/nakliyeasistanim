import React, { useState, useEffect } from 'react';
import axios from 'axios'; // axios'u import ettik

function FirmaList() {
  // Firmaların listesini tutacak state değişkeni
  const [firmalar, setFirmalar] = useState([]);
  // Veri yüklenirken durumu belirtmek için loading state'i
  const [loading, setLoading] = useState(true);
  // Hata durumunu tutacak state
  const [error, setError] = useState(null);

  // Component ilk yüklendiğinde (mount olduğunda) çalışacak useEffect hook'u
  useEffect(() => {
    // API'den veri çekme işlemini async bir fonksiyon içinde yapıyoruz
    async function fetchFirmalar() {
      try {
        // Backend API'ye GET isteği gönderiyoruz
        // package.json'daki proxy ayarı sayesinde sadece '/api/firmalar/' yazmamız yeterli
        const response = await axios.get('/api/firmalar/');
        // Gelen veriyi state'e kaydediyoruz
        setFirmalar(response.data);
        setLoading(false); // Yükleme bitti
      } catch (error) {
        // Hata oluşursa state'e kaydediyoruz
        setError(error);
        setLoading(false); // Yükleme bitti (hata ile)
        console.error("Firmalar çekilirken hata oluştu:", error);
      }
    }

    fetchFirmalar(); // Fonksiyonu çağırarak veri çekme işlemini başlatıyoruz

    // Boş dependency array [] sayesinde bu useEffect sadece component ilk mount olduğunda çalışır
  }, []);

  // Yükleme durumunu göster
  if (loading) {
    return <div>Firmalar yükleniyor...</div>;
  }

  // Hata durumunu göster
  if (error) {
    return <div>Firmalar yüklenirken bir hata oluştu: {error.message}</div>;
  }

  // Firmalar yüklendiğinde listeyi göster
  return (
    <div>
      <h2>Firma Listesi</h2>
      {/* Eğer hiç firma yoksa mesaj göster */}
      {firmalar.length === 0 ? (
          <p>Henüz firma kaydı bulunmamaktadır. Lütfen admin panelinden ekleyiniz.</p>
      ) : (
        <ul>
          {/* firmalar state'indeki her bir firma için bir liste öğesi oluştur */}
          {firmalar.map(firma => (
            <li key={firma.id}>
              {firma.firma_adi} ({firma.vkn_tckn})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default FirmaList; // Component'i dışa aktarıyoruz