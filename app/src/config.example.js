// Nabız yapılandırması — ÖRNEK.
// Bu dosyayı config.js olarak kopyalayıp kendi servislerinizi yazın:
//   cp config.example.js config.js
// config.js .gitignore'dadır; gerçek URL'leriniz depoya gönderilmez.
//
// Her servis için: ad (ekranda görünür) ve health/durum URL'si.
// İki şema desteklenir:
//   - {"ready":true,"database":true,...}        (bileşen bazlı)
//   - {"status":"ok","version":"...","time":""} (durum + sürüm)
// Şema otomatik algılanır; sadece 200 + JSON dönen bir uç yeterlidir.

export var SERVICES = [
  { name: 'Servis A', url: 'https://example.com/health/ready' },
  { name: 'Servis B', url: 'https://api.example.org/health' }
]

// Kontrol aralığı (ms) ve "kapalı" demeden önceki ardışık hata sayısı.
export var INTERVAL_MS = 30000
export var FAIL_THRESHOLD = 2
