# Benim Kütüphanem

Kitaplarımı ve okuma durumlarını takip etmek için geliştirdiğim web tabanlı kişisel kütüphane uygulaması.

## Özellikler

- Kitapları listeleme
- Kitap adına ve yazara göre arama
- Okuma durumuna göre filtreleme
- A-Z ve Z-A sıralama
- Yeni kitap ekleme
- Kitap bilgilerini düzenleme
- Okuma durumunu güncelleme
- Kitap silme
- Yönetici şifresiyle değişiklikleri koruma

## Kullanılan Teknolojiler

- HTML
- CSS
- JavaScript
- Python
- FastAPI
- SQLite
- Docker

## Yerel Olarak Çalıştırma

```powershell
$env:KUTUPHANE_ADMIN_SIFRE = "yonetici-sifreniz"
python -m uvicorn api:app --reload --app-dir icerik
```

Uygulama yerel olarak şu adreste açılır:

```text
http://127.0.0.1:8000
```

## Docker ile Çalıştırma

```powershell
docker build -t benim-kutuphanem:1.0 .
docker run -p 8001:8000 --env "KUTUPHANE_ADMIN_SIFRE=yonetici-sifreniz" benim-kutuphanem:1.0
```

Docker üzerinden çalıştırılan uygulama:

```text
http://127.0.0.1:8001
```

## Canlı Uygulama

Canlı bağlantı, dağıtım işlemi tamamlandıktan sonra buraya eklenecektir.