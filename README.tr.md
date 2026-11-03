<div align="center">

# ⌚ Xiaomi Watch Self-Host Monitor

### Kendi sunucularınızın durumunu Xiaomi (HyperOS) saatinizin ekranından izleyin

[English](README.md) · [Türkçe](README.tr.md)

HyperOS kapalı bir sistemdir — saate normalde üçüncü parti uygulama yüklenemez.
Bu depo, saatte kendi **Vela quick-app**'inizi çalıştırmanın ve ona
**AstroBox köprüsü** üzerinden internet erişimi vermenin **uçtan uca** yolunu
gösterir. Örnek uygulama **Nabız**, sunucularınızın `/health` uçlarını yoklar,
durumlarını renkli gösterir ve bir servis çöktüğünde bileğinizi titretir.

</div>

---

> ⚠️ **Eğitim amaçlıdır.** Yalnızca **kendi** cihazınız ve **kendi**
> sunucularınızla kullanın. Tersine mühendislik adımları birlikte çalışabilirlik
> içindir. Bu depo hiçbir gizli anahtar, cihaz kimliği ya da kişisel veri içermez.

## 📸 Nabız — ekran görüntüleri

<!-- Gerçek görselleri docs/ klasörüne ekleyip bu yer tutucuları değiştirin -->

| Tümü sağlıklı | Bir servis kapalı |
|:---:|:---:|
| ![saglikli](docs/screen-healthy.jpg) | ![kapali](docs/screen-down.jpg) |

## ✨ Özellikler

- **Gerçek sağlık kontrolü** — yalnızca "site açılıyor mu" değil; `/health`
  ucunuzdaki JSON'u okur. İki şema otomatik algılanır:
  - `{"ready":true,"database":true,"relay_server":true,...}` (bileşen bazlı)
  - `{"status":"ok","version":"...","time":"..."}` (durum + sürüm + tazelik)
- **Titreşimli uyarı** — bir servis çöktüğünde (4 darbe) ve toparlandığında
  (2 darbe) bilek titrer. Yalnızca durum *değiştiğinde*; spam yok.
- **Yanlış alarm koruması** — tek hatada değil, ancak ardışık N hatadan sonra
  "kapalı" der.
- **Tazelik denetimi** — `time` alanı eskiyse "şüpheli" gösterir (önbellekten
  gelmiş olabilecek yanıt).
- **N servis** — `config.js`'e yazdığınız kadar servisi izler.
- **Dokununca anında yenilenir**, her 30 sn'de bir otomatik yenilenir.
- **Tamamen yerel** — veri yalnızca saatiniz ↔ telefon ↔ sunucunuz arasında akar.

## 🧩 Nasıl çalışır?

```
┌──────────────┐    BLE/SPP     ┌───────────────┐    internet    ┌─────────────┐
│ Xiaomi Watch │ ─────────────> │    Telefon    │ ─────────────> │  Sunucunuz  │
│ (Nabız app)  │    AstroBox    │  FetchBridge  │                │   /health   │
│   fetch()    │ <───────────── │    (köprü)    │ <───────────── │             │
└──────────────┘                └───────────────┘                └─────────────┘
```

HyperOS saatler internete doğrudan çıkamaz (Wi-Fi quick-app'lere açık değildir),
bu yüzden tüm trafik telefon köprüsünden geçer. Bu köprüyü AstroBox'ın
**FetchBridge** eklentisi kurar; saatteki `system.fetch` çağrısı telefonun
internetini kullanır.

## 🚀 Kurulum (özet)

Tüm adımlar için **[guide/](guide/)** klasörüne bakın. Kısaca:

1. **AstroBox**'ı kurun ([astrobox.online](https://astrobox.online)) ve saati
   bağlayın (auth key gerekir — nasıl alınacağı rehberde anlatılır).
2. AstroBox'tan **FetchBridge** eklentisini kurun ve uygulamanız için
   "dinleme"yi (listen) açın.
3. Bu depoyu derleyin:
   ```bash
   cd app
   cp src/config.example.js src/config.js   # kendi servislerinizi yazın
   python3 tools-make-logo.py                # logoyu üretin
   npm install && npm run build              # .rpk üretir
   ```
4. Üretilen `.rpk`'yı AstroBox (veya Gadgetbridge) ile saate yükleyin.

## ⚙️ Yapılandırma

`app/src/config.js` (örnekten kopyalanır; depoya gönderilmez):

```js
export var SERVICES = [
  { name: 'Servis A', url: 'https://example.com/health/ready' },
  { name: 'Servis B', url: 'https://api.example.org/health' }
]
export var INTERVAL_MS = 30000     // kontrol aralığı
export var FAIL_THRESHOLD = 2      // kaç ardışık hatada "kapalı"
```

Health ucunuzun `200 + JSON` dönmesi yeterlidir. Örnek bir (nginx) uç için
[guide/health-endpoint.md](guide/health-endpoint.md) dosyasına bakın.

## 🛠️ Gereksinimler

| Ne | Neden |
|---|---|
| Xiaomi HyperOS saat (ör. Watch S4, Redmi Watch 6) | hedef cihaz |
| Android telefon | köprü (FetchBridge burada çalışır) |
| AstroBox + FetchBridge | sideload + internet köprüsü |
| Node.js | `npm run build` (Vela aiot-toolkit) |

## 📂 Depo yapısı

```
├── app/                       Nabız uygulaması (Vela quick-app)
│   ├── src/
│   │   ├── config.example.js  ← kopyalayıp config.js yapın
│   │   ├── manifest.json
│   │   ├── common/logo.png    ← tools-make-logo.py üretir
│   │   └── pages/index/index.ux
│   └── tools-make-logo.py
├── guide/                     Uçtan uca rehber (auth key, köprü, derleme)
└── docs/                      Ekran görüntüleri
```

## 📄 Lisans

MIT — bkz. [LICENSE](LICENSE).

## 🙏 Teşekkürler

- [AstroBox](https://github.com/AstralSightStudios/AstroBox-NG) — sideload + köprü
- [Gadgetbridge](https://gadgetbridge.org) — alternatif sideload/bağlantı
- Xiaomi Vela quick-app topluluğu
