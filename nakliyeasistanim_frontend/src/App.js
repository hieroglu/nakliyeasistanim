import React from 'react';
// Varsayılan React CSS'ini isterseniz silebilirsiniz
// import './App.css';

// Oluşturduğumuz FirmaList component'ini import ediyoruz
import FirmaList from './components/FirmaList';

function App() {
  return (
    <div className="App">
      <header className="App-header" style={{ backgroundColor: '#282c34', minHeight: '10vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontSize: 'calc(10px + 2vmin)', color: 'white' }}>
        <h1>Nakliye Asistanım</h1>
      </header>
      <main style={{ padding: '20px' }}>
         {/* FirmaList component'ini buraya ekliyoruz */}
        <FirmaList />
      </main>
    </div>
  );
}

export default App;