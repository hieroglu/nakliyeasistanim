import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios'; // axios'u import ettik

// Auth Context'i oluşturuyoruz
const AuthContext = createContext(null);

// Context Provider Component'i
export const AuthProvider = ({ children }) => {
  // Kullanıcı bilgisi ve token'lar için state'ler
  // Başlangıçta Local Storage'dan token'ları okumaya çalışıyoruz
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null
  );
  const [user, setUser] = useState(() =>
    localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')).user : null
  );
  const [loading, setLoading] = useState(true); // Token'ları kontrol ederken yükleme durumu

  // axios default header'ına token'ı eklemek için interceptor kullanalım veya default header'ı ayarlayalım
  // Context provider yüklendiğinde veya token değiştiğinde çalışacak
  useEffect(() => {
    if (authTokens) {
      // Eğer token varsa, axios'un default header'ına ekle
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + authTokens.access;
      // Kullanıcı bilgisini de token'dan çözerek alabiliriz (opsiyonel, şimdilik token içindeki user bilgisini kullanalım)
      // const decodedUser = jwtDecode(authTokens.access); // jwt-decode kütüphanesi gerekebilir
      // setUser({ name: decodedUser.username, id: decodedUser.user_id }); // user bilgisini state'e kaydet

      // Local Storage'a kaydet
      localStorage.setItem('authTokens', JSON.stringify(authTokens));
      localStorage.setItem('user', JSON.stringify(authTokens.user)); // user bilgisini ayrıca kaydet

    } else {
      // Token yoksa default header'dan Authorization'ı kaldır
      delete axios.defaults.headers.common['Authorization'];
      // Local Storage'dan temizle
      localStorage.removeItem('authTokens');
      localStorage.removeItem('user');
    }
    setLoading(false); // Yükleme tamamlandı
  }, [authTokens]); // authTokens state'i değiştiğinde bu effect tekrar çalışır


  // Login fonksiyonu
  const loginUser = async (username, password) => {
    try {
      const response = await axios.post('/api/token/', {
        username,
        password,
      });

      if (response.status === 200) {
        // Tokenları ve kullanıcı bilgisini alıp state'e ve Local Storage'a kaydet
        const tokens = response.data;
        // user bilgisini simplejwt varsayılan olarak token içine koymaz,
        // bu yüzden backend'deki TokenObtainPairSerializer'ı özelleştirmek gerekir.
        // Şimdilik user bilgisini hardcode edelim veya token payload'undan çekelim (karmaşık olabilir).
        // En basit haliyle, login başarılı ise kullanıcıyı 'logged in' olarak işaretleyelim.
        // setUser({ username: username }); // Örnek kullanıcı objesi

        // SimpleJWT token payload'unda user_id bilgisini taşır. İsterseniz buradan alabilirsiniz.
        // import jwt_decode from 'jwt-decode'; // jwt-decode kütüphanesi gerekli
        // const decodedToken = jwt_decode(tokens.access);
        // setUser({ user_id: decodedToken.user_id, username: username });

        // Basitlik için şimdilik sadece tokenları set edip, user bilgisini de tokenlardan alalım (varsa)
        setAuthTokens(tokens);
         if (tokens.user) { // Eğer backend token içinde user gönderiyorsa
             setUser(tokens.user);
         } else { // Yoksa sadece username'i kaydedelim
             setUser({ username: username });
         }


        // useEffect handle edecek Local Storage'ı güncellemeyi
        return { success: true }; // Başarılı olduğunu belirt
      } else {
         // Hata durumunu yönet
         console.error("Login başarısız:", response.status);
         return { success: false, error: 'Login başarısız. Lütfen kullanıcı adı ve şifrenizi kontrol edin.' };
      }
    } catch (error) {
      console.error("Login sırasında API hatası:", error.response ? error.response.data : error.message);
      return { success: false, error: error.response ? error.response.data.detail || 'Login sırasında bir hata oluştu.' : 'Login sırasında bir hata oluştu.' };
    }
  };

  // Logout fonksiyonu
  const logoutUser = () => {
    setAuthTokens(null); // Tokenları temizle
    setUser(null); // Kullanıcı bilgisini temizle
    // useEffect handle edecek Local Storage'ı temizlemeyi
  };

  // Token yenileme fonksiyonu (Opsiyonel, useEffect içinde periyodik çalışabilir veya istek başarısız olunca denenir)
  const updateToken = async () => {
    if (!authTokens?.refresh) { // Refresh token yoksa
        setLoading(false);
        return;
    }

    try {
        const response = await axios.post('/api/token/refresh/', {
            refresh: authTokens.refresh
        });

        if (response.status === 200) {
            const newTokens = response.data;
             // Backend yeni refresh token gönderiyorsa (ROTATE_REFRESH_TOKENS: True ise)
            const updatedTokens = { ...newTokens, refresh: newTokens.refresh || authTokens.refresh };
            setAuthTokens(updatedTokens);
             if (newTokens.user) { // Eğer backend yeni token içinde user gönderiyorsa
                 setUser(newTokens.user);
             } else { // Yoksa eski user bilgisini koru veya token payload'dan çek
                 // import jwt_decode from 'jwt-decode'; // jwt-decode kütüphanesi gerekli
                 // const decodedToken = jwt_decode(newTokens.access);
                 // setUser({ user_id: decodedToken.user_id, username: decodedToken.username }); // username payload'da yoksa
                 // Şimdilik eski user bilgisini koruyalım
             }
        } else {
            // Refresh başarısız olursa (refresh token süresi dolmuş vb.) logout yap
            console.error("Token yenileme başarısız:", response.status);
            logoutUser();
        }
    } catch (error) {
        console.error("Token yenileme sırasında API hatası:", error.response ? error.response.data : error.message);
        // Hata durumunda da logout yap
        logoutUser();
    } finally {
        setLoading(false); // Yükleme tamamlandı
    }
  };

    // Component yüklendiğinde refresh token ile access token'ı yenilemeye çalış
    // Bu, tarayıcı kapatılıp açıldığında kullanıcının login kalmasını sağlar.
    useEffect(() => {
      if(authTokens){ // Eğer Local Storage'da token varsa
           const tokenRefreshInterval = 1000 * 60 * 4; // Örneğin 4 dakikada bir yenile (Access token ömründen kısa)
           const interval = setInterval(() => {
               updateToken();
           }, tokenRefreshInterval);
           return () => clearInterval(interval); // Component unmount olunca interval'ı temizle
      } else {
          setLoading(false); // Eğer token yoksa yükleme zaten bitti
      }

    }, [authTokens]); // authTokens değiştiğinde interval'ı yeniden kur


  // Context değeri: Login durumu, kullanıcı bilgisi ve login/logout fonksiyonları
  const contextData = {
    user: user,
    authTokens: authTokens,
    loginUser: loginUser,
    logoutUser: logoutUser,
  };

    // Eğer tokenları kontrol ederken yükleme yapılıyorsa (sayfa ilk açıldığında)
    // Yükleme durumu, kullanıcı arayüzünde bir loading spinner göstermek için kullanılabilir
   if (loading) {
       return <div>Yükleniyor...</div>; // veya daha iyi bir loading component'i
   }


  return (
    <AuthContext.Provider value={contextData}>
      {children} {/* Provider içindeki component'ler (App) */}
    </AuthContext.Provider>
  );
};

// Context Hook'u: Component'lerin Context'e erişmesini sağlar
export const useAuth = () => {
  return useContext(AuthContext);
};