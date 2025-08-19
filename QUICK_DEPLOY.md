# 🚀 Hızlı Deployment Rehberi

## 📋 5 Dakikada Deployment

### 1. GitHub'a Push
```bash
# GitHub'da yeni repository oluşturun
# Sonra bu komutları çalıştırın:
git remote add origin https://github.com/KULLANICI_ADINIZ/dugun-drive.git
git branch -M main
git push -u origin main
```

### 2. Render.com'da Backend Deploy
1. [Render.com](https://render.com) → Sign Up (GitHub ile)
2. **New Web Service** → GitHub repo seçin
3. **Environment**: Python 3
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
6. **Environment Variables** ekleyin:
   - `GOOGLE_CREDENTIALS_FILE=credentials.json`
   - `GOOGLE_TOKEN_FILE=token.json`
7. **Files** sekmesinde `credentials.json` yükleyin
8. **Deploy** butonuna tıklayın
9. API URL'ini not edin: `https://your-app.onrender.com`

### 3. Netlify'da Frontend Deploy
1. [Netlify.com](https://netlify.com) → Sign Up (GitHub ile)
2. **New site from Git** → GitHub repo seçin
3. **Build settings**:
   - **Build command**: `echo "Static files ready"`
   - **Publish directory**: `app/static`
4. **Deploy site** butonuna tıklayın
5. Site URL'ini not edin: `https://your-site.netlify.app`

### 4. API URL Güncelleme
`app/static/index.html` dosyasında şu satırı bulun:
```javascript
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? '/api/v1/drive' 
    : 'https://your-app.onrender.com/api/v1/drive';  // Burayı güncelleyin
```

### 5. QR Kod Hazır!
- Netlify URL'inizi kopyalayın
- QR kod otomatik oluşacak
- İndirip bastırın

## 🎯 Sonuç
- **Frontend**: `https://your-site.netlify.app`
- **QR Kod**: Herhangi bir yerden erişilebilir
- **WiFi gerekmez**
- **Mobil uyumlu**

## 📱 Test
1. Netlify URL'ini test edin
2. QR kodu telefonla tarayın
3. Fotoğraf yükleyin
4. Google Drive'da kontrol edin

**Artık düğün misafirleriniz herhangi bir yerden anılarını yükleyebilir!** 🎉 