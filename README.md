# Google Drive API Backend

Bu proje, Google Drive entegrasyonu için Python backend API'sidir. Katmanlı mimari (Core, Service, Manager, Router) kullanılarak geliştirilmiştir.

## Proje Yapısı

```
dugun_drive/
├── app/
│   ├── core/           # Temel sınıflar ve yardımcılar
│   │   ├── __init__.py
│   │   ├── config.py   # Uygulama konfigürasyonu
│   │   ├── exceptions.py # Özel exception sınıfları
│   │   └── models.py   # Veri modelleri
│   ├── service/        # İş mantığı katmanı
│   │   ├── __init__.py
│   │   └── google_drive_service.py # Google Drive servisi
│   ├── manager/        # İş mantığı koordinasyonu
│   │   ├── __init__.py
│   │   └── google_drive_manager.py # Google Drive yöneticisi
│   ├── router/         # API endpoint'leri
│   │   ├── __init__.py
│   │   └── google_drive_router.py # Google Drive router'ı
│   ├── __init__.py
│   └── main.py         # Ana uygulama
├── requirements.txt    # Python bağımlılıkları
├── env.example        # Örnek environment değişkenleri
└── README.md          # Bu dosya
```

## Katmanlı Mimari

### Core Katmanı
- **Erişim**: Hiçbir katmana erişmez
- **İçerik**: Konfigürasyon, modeller, exception'lar
- **Dosyalar**: `config.py`, `models.py`, `exceptions.py`

### Service Katmanı
- **Erişim**: Sadece Core katmanına erişir
- **İçerik**: Google Drive API işlemleri
- **Dosyalar**: `google_drive_service.py`

### Manager Katmanı
- **Erişim**: Service ve Core katmanlarına erişir
- **İçerik**: İş mantığı koordinasyonu
- **Dosyalar**: `google_drive_manager.py`

### Router Katmanı
- **Erişim**: Manager ve Core katmanlarına erişir
- **İçerik**: API endpoint'leri
- **Dosyalar**: `google_drive_router.py`

## Kurulum

1. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

2. **Google Drive API kimlik bilgilerini hazırlayın:**
   - Google Cloud Console'da bir proje oluşturun
   - Google Drive API'yi etkinleştirin
   - OAuth 2.0 kimlik bilgileri oluşturun
   - `credentials.json` dosyasını proje kök dizinine yerleştirin

3. **Environment değişkenlerini ayarlayın:**
```bash
cp env.example .env
# .env dosyasını düzenleyin
```

## Çalıştırma

```bash
# Geliştirme sunucusunu başlatın
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Veya doğrudan main.py ile
python app/main.py
```

## API Endpoint'leri

### Dosya Yükleme
```
POST /api/v1/drive/upload
```

### Dosya Listesi
```
GET /api/v1/drive/files?page_size=10&page_token=...
```

### Dosya Bilgisi
```
GET /api/v1/drive/files/{file_id}
```

### Dosya Silme
```
DELETE /api/v1/drive/files/{file_id}
```

### Dosya İndirme
```
GET /api/v1/drive/files/{file_id}/download
```

### Dosya Arama
```
GET /api/v1/drive/search?query=test&page_size=10
```

### Sağlık Kontrolü
```
GET /api/v1/drive/health
```

## API Dokümantasyonu

Uygulama çalıştıktan sonra aşağıdaki adreslerden API dokümantasyonuna erişebilirsiniz:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Özellikler

- ✅ Katmanlı mimari (Core, Service, Manager, Router)
- ✅ Google Drive API entegrasyonu
- ✅ Dosya yükleme/indirme
- ✅ Dosya listeleme ve arama
- ✅ Dosya silme
- ✅ Hata yönetimi
- ✅ CORS desteği
- ✅ API dokümantasyonu
- ✅ Health check endpoint'i

## Güvenlik

- OAuth 2.0 kimlik doğrulama
- CORS koruması
- Hata mesajlarında hassas bilgi sızıntısı yok
- Dosya boyutu sınırlamaları

## Geliştirme

### Yeni özellik ekleme:
1. Core katmanında gerekli modelleri tanımlayın
2. Service katmanında iş mantığını implement edin
3. Manager katmanında koordinasyonu sağlayın
4. Router katmanında endpoint'leri ekleyin

### Test:
```bash
# Test çalıştırma (test dosyaları eklendikten sonra)
python -m pytest
``` 