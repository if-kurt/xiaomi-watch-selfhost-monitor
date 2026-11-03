# 2 · AstroBox + FetchBridge

[AstroBox](https://github.com/AstralSightStudios/AstroBox-NG) is an
independent, open-source reimplementation of the Bluetooth protocol Xiaomi
Vela wearables use. It lets you install third-party quick-apps and, through
plugins, extend what the watch can do. **FetchBridge** is the plugin that
gives quick-apps internet access by relaying their `system.fetch` calls
through the phone.

> AstroBox is not made, authorized or supported by Xiaomi.

## 1. Install AstroBox

Download it from [astrobox.online](https://astrobox.online) or from the
[GitHub releases](https://github.com/AstralSightStudios/AstroBox-NG/releases)
(Windows, Linux, Android; iOS via the App Store).

For Nabız, install it **on the Android phone**: the phone is what stays near
the watch and provides the internet connection. On Android, also exempt
AstroBox from battery optimization so the bridge keeps running in the
background.

## 2. Put the watch in pairing mode

On the watch, open the settings page for your device / system (where restart
and power-off usually are) and tap **Connect new phone** (the exact wording
varies by model and firmware). Confirm, and wait until the watch shows its
connection screen.

## 3. Connect the watch in AstroBox

1. Open the device list in AstroBox (on mobile: tap the device card at the
   bottom, then the switch button).
2. Select your watch.
3. Enter the auth key from [step 1](01-auth-key.md)
   (`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`) — or use the Xiaomi account sync
   described there.
4. When the watch vibrates, confirm on the watch (blue check mark).
5. Accept the system Bluetooth pairing prompt on the phone
   (*Pair & connect*; on Android it may arrive as a notification).

AstroBox now shows the watch as connected (`AA:BB:CC:DD:EE:FF` in the device
details).

## 4. Install FetchBridge and listen for your app

1. In AstroBox, open **Plugins → Plugin Market**.
2. Find **FetchBridge** and install it. Restart AstroBox when prompted.
3. Open **Plugins → FetchBridge** and check that it sees the watch as paired.
4. Scroll to the list of apps and find **Nabız** (`com.example.nabiz`, or your
   own package name if you changed it in `manifest.json`).
5. Tap **Listen**. A success indicator confirms it is active.

The app has to be on the watch before it appears in this list. If you haven't
installed Nabız yet, do [step 3](03-build-deploy.md) first and come back here.

From now on, every `fetch()` Nabız makes is carried over Bluetooth to the
phone, executed there, and the response is sent back to the watch. Keep
AstroBox running (and the phone within Bluetooth range) while you use the app.

## 5. Mi Fitness and the SPP channel

The watch talks to its companion app over a **classic Bluetooth SPP**
channel, and in practice only one app can hold it at a time. If Mi Fitness is
running on the same phone, it competes with AstroBox for that channel.
Typical symptoms:

- AstroBox hangs on "connecting" or drops the connection after a few seconds.
- Nabız works, then suddenly every service shows `KAPALI` (the bridge lost the
  channel to Mi Fitness).

What to do:

- While you use AstroBox / FetchBridge, **force-stop Mi Fitness**
  (*Android Settings → Apps → Mi Fitness → Force stop*) and keep it from
  running in the background.
- Open Mi Fitness again only when you want to sync health data, then
  reconnect AstroBox afterwards.
- **Don't unpair** the watch in Mi Fitness to "fix" a conflict — that issues a
  new auth key (see [step 1](01-auth-key.md#warning-the-key-changes-when-you-unpair)).

## 6. Check that the bridge works

Open Nabız on the watch and tap the screen. Within a few seconds each row
should turn green (`SAĞLIKLI ✓` or `AYAKTA`). If every row shows `KAPALI`
right away, the request never left the watch: re-check step 4 (Listen) and
step 5 (Mi Fitness).

---

Previous: [1 · Auth key](01-auth-key.md) · Next: [3 · Build & deploy](03-build-deploy.md)
