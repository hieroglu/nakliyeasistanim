import React from 'react';
// import './App.css';

// Router component'leri
import { Routes, Route, Link, Navigate, Outlet } from 'react-router-dom';

// Oluşturduğumuz Component'ler
import FirmaList from './components/FirmaList';
import NakliyeKaydiList from './components/NakliyeKaydiList';
import NakliyeKaydiForm from './components/NakliyeKaydiForm';
import LoginForm from './components/LoginForm';

// Auth Hook'u
import { useAuth } from './context/AuthContext';

// --- ProtectedRoute Component'i ---
// Kullanıcının login olup olmadığını kontrol eder ve login değilse /login sayfasına yönlendirir
const ProtectedRoute = ({ children, ...rest }) => {
    const { user } = useAuth(); // AuthContext'ten kullanıcı bilgisini al

    if (!user) {
        // Eğer kullanıcı login değilse, login sayfasına yönlendir
        return <Navigate to="/login" replace={true} />;
    }

    // Eğer kullanıcı login ise, child component'leri (yani Route'un element/children'ı) göster
    return children ? children : <Outlet />; // Outlet, nested route'lar için kullanılır, şimdilik children yeterli
};


function App() {
  const { user, logoutUser } = useAuth(); // AuthContext'ten kullanıcı ve logout fonksiyonunu al

  return (
    <div className="App">
      <header className="App-header" style={{ backgroundColor: '#282c34', minHeight: '10vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontSize: 'calc(10px + 2vmin)', color: 'white' }}>
        <h1>Nakliye Asistanım</h1>
        {/* Eğer kullanıcı login ise kullanıcı adını ve logout butonunu göster */}
        {user ? (
          <div style={{ fontSize: '0.8em', marginTop: '10px' }}>
            Hoş geldiniz, {user.username}!
             {/* Navigasyon Linkleri */}
             <nav style={{ marginTop: '10px' }}>
                 <Link to="/" style={{ color: 'white', marginLeft: '10px', textDecoration: 'none' }}>Anasayfa</Link> |
                 <Link to="/firmalar" style={{ color: 'white', marginLeft: '10px', textDecoration: 'none' }}>Firmalar</Link> |
                 <Link to="/nakliyeler" style={{ color: 'white', marginLeft: '10px', textDecoration: 'none' }}>Nakliyeler</Link> |
                 <Link to="/nakliyeler/yeni" style={{ color: 'white', marginLeft: '10px', textDecoration: 'none' }}>Yeni Nakliye</Link>
                 {/* İleride diğer linkler buraya eklenecek */}
             </nav>
            <button onClick={logoutUser} style={{ marginLeft: '10px', padding: '5px 10px', cursor: 'pointer' }}>Çıkış Yap</button>
          </div>
        ) : (
           <div style={{ fontSize: '0.8em', marginTop: '10px' }}>
             Lütfen Giriş Yapın
           </div>
        )}
      </header>

      <main style={{ padding: '20px' }}>
        {/* Routes component'i, hangi Route'un mevcut URL ile eşleştiğini belirler */}
        <Routes>
          {/* Login sayfası - Login değilse gösterilir */}
          <Route path="/login" element={user ? <Navigate to="/" /> : <LoginForm />} />

          {/* Korumalı Rotalar - ProtectedRoute içine alınır */}
          {/* Anasayfa (Login olduktan sonra yönlenilen yer) */}
          <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} /> {/* Anasayfa için ayrı bir component */}

          {/* Firma Listesi Sayfası */}
          <Route path="/firmalar" element={<ProtectedRoute><FirmaList /></ProtectedRoute>} />

          {/* Nakliye Kayıtları Listesi Sayfası */}
          <Route path="/nakliyeler" element={<ProtectedRoute><NakliyeKaydiList /></ProtectedRoute>} />

          {/* Yeni Nakliye Kaydı Ekleme Sayfası (Mevcut) */}
          <Route path="/nakliyeler/yeni" element={<ProtectedRoute><NakliyeKaydiForm /></ProtectedRoute>} />

          {/* Mevcut Nakliye Kaydını Düzenleme Sayfası (YENİ) */}
          {/* Dikkat: :id dinamik bir parametredir. NakliyeKaydiForm componenti burada yeniden kullanılacak */}
          <Route path="/nakliyeler/:id/duzenle" element={<ProtectedRoute><NakliyeKaydiForm /></ProtectedRoute>} />


          {/* İleride diğer sayfalar buraya eklenecek */}

          {/* Eşleşmeyen tüm yollar için 404 sayfası (Opsiyonel) */}
          {/* <Route path="*" element={<div>Sayfa Bulunamadı (404)</div>} /> */}
        </Routes>
      </main>
    </div>
  );
}

// Anasayfa için basit bir component (Opsiyonel, App içinde de gösterilebilir)
function HomePage() {
    return (
        <div>
            <h2>Anasayfa</h2>
            <p>Hoş geldiniz! Lütfen yukarıdaki menüden işlem yapmak istediğiniz bölümü seçin.</p>
             {/* Buraya belki özet bilgiler veya duyurular eklenebilir */}
        </div>
    );
}


export default App;