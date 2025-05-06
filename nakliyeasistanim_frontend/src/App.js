import React from 'react';
// import './App.css'; // Varsayılan CSS

import FirmaList from './components/FirmaList';
// Yeni component'leri import ediyoruz
import NakliyeKaydiList from './components/NakliyeKaydiList';
import NakliyeKaydiForm from './components/NakliyeKaydiForm';


function App() {
  return (
    <div className="App">
      <header className="App-header" style={{ backgroundColor: '#282c34', minHeight: '10vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontSize: 'calc(10px + 2vmin)', color: 'white' }}>
        <h1>Nakliye Asistanım</h1>
      </header>
      <main style={{ padding: '20px' }}>
         {/* Component'leri buraya ekliyoruz */}
        <FirmaList /> {/* Firma Listesi */}
        <hr style={{ margin: '40px 0'}}/> {/* Ayırıcı çizgi */}
        <NakliyeKaydiList /> {/* Nakliye Kayıtları Listesi */}
         <hr style={{ margin: '40px 0'}}/> {/* Ayırıcı çizgi */}
        <NakliyeKaydiForm /> {/* Yeni Nakliye Kaydı Formu */}
      </main>
    </div>
  );
}

export default App;