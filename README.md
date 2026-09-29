# ViralBot MVP 2

Telefon üzerinden yönetilecek Türkçe YouTube Shorts otomasyonunun çalışan MVP'si.

## Replit Secrets
Şunları Replit Secrets'a ekle:
- `SECRET_KEY` = rastgele uzun bir değer
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI` = Replit uygulamanın HTTPS adresi + `/oauth/callback`

Google Cloud'da YouTube Data API v3'ü etkinleştir ve Web application OAuth client oluştur. Authorized redirect URI olarak aynı callback adresini ekle.

## Çalıştır
`pip install -r requirements.txt`
`python app.py`

## Akış
1. Uygulamayı aç.
2. "Google ile YouTube'u Bağla"ya bas.
3. Google izinlerini onayla.
4. MP4 seç, başlık gir.
5. YouTube'a yükle.

YouTube API `videos.insert` kullanılır. Yeni/doğrulanmamış API projelerinde yüklenen videoların gizli modda kısıtlanabilmesi YouTube tarafından belirtilmektedir; API projesi doğrulaması gerekebilir.
