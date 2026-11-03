# 3 · Build & deploy

Nabız is a **Vela JS quick-app**. It is built with Xiaomi's
[AIoT-toolkit](https://iot.mi.com/vela/quickapp/en/tools/toolkit/start.html)
into an `.rpk` package, which you then sideload onto the watch.

## Prerequisites

| Tool | Used for |
|---|---|
| Node.js (current LTS) + npm | installing and running AIoT-toolkit 2.x |
| Python 3 + Pillow (`pip install pillow`) | generating the app icon |

AIoT-toolkit is installed as a dev dependency by `npm install`; you don't need
a global install.

## 1. Get the code

```bash
git clone https://github.com/<you>/xiaomi-watch-selfhost-monitor.git
cd xiaomi-watch-selfhost-monitor/app
```

## 2. Create your config.js

The app imports `src/config.js`, which is **not** in the repo. Create it from
the example and list your own services:

```bash
cp src/config.example.js src/config.js
```

```js
export var SERVICES = [
  { name: 'Service A', url: 'https://example.com/health/ready' },
  { name: 'Service B', url: 'https://api.example.org/health' }
]
export var INTERVAL_MS = 30000     // check interval
export var FAIL_THRESHOLD = 2      // failures before "down"
```

- `name` is shown on the watch — keep it short (about 12 characters fit).
- `url` must return `200 + JSON`; see [health-endpoint.md](health-endpoint.md).
- Use HTTPS with a valid public certificate; the request is executed on the
  phone and goes out over its connection.

`config.js` is gitignored. Your URLs end up inside the built `.rpk`, so don't
publish the `.rpk` either (`*.rpk` is gitignored too).

## 3. Generate the icon

`manifest.json` points to `/common/logo.png`. Generate it:

```bash
python3 tools-make-logo.py      # writes src/common/logo.png
```

## 4. Build

```bash
npm install
npm run build                   # runs AIoT-toolkit: aiot build
```

The build produces an `.rpk` named after the package
(`com.example.nabiz…rpk`), typically under `dist/`.

For a release build, AIoT-toolkit's `aiot release` signs the package with
keys from the `sign/` directory. That directory is gitignored — **never commit
signing keys**.

### Changing the package name

`com.example.nabiz` is a placeholder. If you publish your own fork, change
`"package"` in `src/manifest.json` (e.g. `io.github.<you>.nabiz`) and bump
`versionCode` on every release.

## 5. Install on the watch

**With AstroBox** (watch connected as in [step 2](02-astrobox-bridge.md)):
open the install / resources section, choose *install from file*, and pick
the `.rpk`. Wait for the transfer to finish; Nabız appears in the watch's app
list.

**With Gadgetbridge** (alternative): with the watch connected to
Gadgetbridge, open the `.rpk` with Gadgetbridge's file installer and confirm.
Gadgetbridge supports installing quick-app (`.rpk`) packages on Xiaomi
watches that use the protobuf protocol. Gadgetbridge doesn't provide the
FetchBridge internet bridge, so for a working Nabız you still need AstroBox
for step 6.

## 6. Turn on the bridge

Go back to [step 2 · section 4](02-astrobox-bridge.md#4-install-fetchbridge-and-listen-for-your-app)
and tap **Listen** for Nabız in FetchBridge. Then open the app on the watch.

## Updating

Edit `src/config.js` (or the code), bump `versionCode` in `manifest.json`,
rebuild, and install the new `.rpk` the same way.

## Troubleshooting

| Problem | Fix |
|---|---|
| Build error about `../../config.js` | You skipped step 2 — create `src/config.js`. |
| Build error / missing icon | Run `python3 tools-make-logo.py` (step 3). |
| `ModuleNotFoundError: PIL` | `pip install pillow` |
| App installs but every row shows `KAPALI` | FetchBridge isn't listening for the app — step 6. |
| A row shows `KAPALI (404)` / `KAPALI (5xx)` | The URL is wrong or the server is really down; open it in a browser. |
| A row shows `KAPALI (yanit?)` | The endpoint returned 200 but not JSON. |

---

Previous: [2 · AstroBox + FetchBridge](02-astrobox-bridge.md) · Server side: [health-endpoint.md](health-endpoint.md)
