# Düğün Drive - Deployment Talimatları

## 🚀 Production Deployment

Bu uygulama iki parçadan oluşur:
1. **Backend API** (Render.com)
2. **Frontend** (Netlify)

## 📋 Adım 1: Backend API (Render.com)

### 1. Render.com'da Hesap Oluşturun
- [Render.com](https://render.com) adresine gidin
- GitHub hesabınızla giriş yapın

### 2. Yeni Web Service Oluşturun
- **New Web Service** butonuna tıklayın
- GitHub repository'nizi seçin
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

### 3. Environment Variables Ekleme
Render.com dashboard'da **Environment** sekmesine gidin ve şunları ekleyin:

```
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json
```

### 4. Google Drive Credentials Ekleme
- **Files** sekmesine gidin
- `credentials.json` dosyasını yükleyin (Google Cloud Console'dan indirdiğiniz)

### 5. Deploy Edin
- **Deploy** butonuna tıklayın
- API URL'inizi not edin: `https://your-app-name.onrender.com`

## 📋 Adım 2: Frontend (Netlify)

### 1. Netlify'da Hesap Oluşturun
- [Netlify.com](https://netlify.com) adresine gidin
- GitHub hesabınızla giriş yapın

### 2. Yeni Site Oluşturun
- **New site from Git** butonuna tıklayın
- GitHub repository'nizi seçin
- **Build settings**:
  - **Build command**: `echo "Static files ready"`
  - **Publish directory**: `app/static`

### 3. Deploy Edin
- **Deploy site** butonuna tıklayın
- Site URL'inizi not edin: `https://your-site-name.netlify.app`

## 🔧 Konfigürasyon

### API URL Güncelleme
Frontend'de API URL'ini güncelleyin:

```javascript
// app/static/index.html dosyasında
const API_BASE = 'https://your-app-name.onrender.com/api/v1/drive';
```

### CORS Ayarları
Backend'de CORS ayarlarını güncelleyin:

```python
# app/core/config.py dosyasında
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "https://your-site-name.netlify.app",  # Netlify URL'inizi ekleyin
]
```

## 🌐 Sonuç

Deployment tamamlandıktan sonra:
- **Frontend**: `https://your-site-name.netlify.app`
- **Backend API**: `https://your-app-name.onrender.com`
- **QR Kod**: Netlify URL'ini kullanarak oluşturun

## 📱 Mobil Erişim

Artık herhangi bir cihazdan:
- **QR kod ile** erişilebilir
- **WiFi gerekmez**
- **Herhangi bir yerden** kullanılabilir

## 🔍 Test Etme

1. Netlify URL'inizi test edin
2. QR kodu oluşturun ve test edin
3. Google Drive entegrasyonunu test edin
4. Mobil cihazlardan test edin

## 🆘 Sorun Giderme

### API Bağlantı Hatası
- CORS ayarlarını kontrol edin
- API URL'ini doğru güncellediğinizden emin olun

### Google Drive Hatası
- Credentials dosyasının doğru yüklendiğinden emin olun
- Environment variables'ları kontrol edin

### Netlify Build Hatası
- Build command'in doğru olduğundan emin olun
- Publish directory'nin doğru olduğundan emin olun 