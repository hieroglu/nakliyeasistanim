import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext'; // useAuth hook'unu import ettik

function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState(null); // Login hatası için state

  // useAuth hook'unu kullanarak AuthContext'e erişiyoruz
  const { loginUser } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoginError(null); // Önceki hatayı temizle

    // loginUser fonksiyonunu çağırıyoruz
    const result = await loginUser(username, password);

    if (result.success) {
      // Login başarılı, AuthContext state'leri güncellendi.
      // Burada yönlendirme (routing kullanıyorsanız) yapabilirsiniz veya
      // login durumuna göre component'ler otomatik render olacaktır.
      console.log("Login Başarılı!");
      // Formu temizle (isteğe bağlı)
      setUsername('');
      setPassword('');
    } else {
      // Login başarısız, hata mesajını göster
      console.error("Login Hatası:", result.error);
      setLoginError(result.error);
    }
  };

  return (
    <div>
      <h2>Kullanıcı Girişi</h2>
      {loginError && <p style={{ color: 'red' }}>{loginError}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Kullanıcı Adı:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Şifre:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Giriş Yap</button>
      </form>
    </div>
  );
}

export default LoginForm;