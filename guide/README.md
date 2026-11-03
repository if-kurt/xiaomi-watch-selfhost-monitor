# 📘 Guide — from a closed watch to a working Nabız

This guide walks through the whole chain, in order:

```
Xiaomi cloud ──> auth key ──> AstroBox (watch connected) ──> FetchBridge (internet)
                                                         └─> .rpk installed (Nabız)
```

## Steps

| # | Step | What you end up with | File |
|:-:|---|---|---|
| 1 | Get the auth key | The watch's 32-character auth key | [01-auth-key.md](01-auth-key.md) |
| 2 | Connect AstroBox + FetchBridge | Watch connected to AstroBox, internet bridge ready | [02-astrobox-bridge.md](02-astrobox-bridge.md) |
| 3 | Build & deploy | `.rpk` built from this repo and installed on the watch | [03-build-deploy.md](03-build-deploy.md) |
| — | Health endpoint (server side) | A `/health` URL that Nabız can read | [health-endpoint.md](health-endpoint.md) |

Steps 2 and 3 meet in the middle: FetchBridge can only "listen" for an app that
is already installed on the watch, so you will come back to step 2 once after
installing the `.rpk` in step 3.

## Before you start

- A Xiaomi HyperOS watch that is already paired with **Mi Fitness** on your
  phone (this is what registers it in the Xiaomi cloud).
- The Xiaomi account that watch is bound to.
- An Android phone (it runs AstroBox and the FetchBridge plugin).
- A computer with **Node.js** and **Python 3** for building.
- At least one server with an HTTPS health URL that returns `200 + JSON`.

## Conventions used in this guide

All identifiers in these documents are **placeholders**. Never replace them
with real values in anything you commit or post publicly:

| Kind | Placeholder |
|---|---|
| Auth key | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| Bluetooth MAC | `AA:BB:CC:DD:EE:FF` |
| Device ID / serial | `000000000` |
| Server URL | `https://example.com/...` |

The repo's [`.gitignore`](../.gitignore) already excludes key files, signing
keys, Bluetooth logs, built `.rpk` packages and your local `config.js`.

## Quick troubleshooting

| Symptom | Most likely cause | See |
|---|---|---|
| AstroBox can't connect / keeps dropping | Wrong auth key, or Mi Fitness holding the Bluetooth channel | [01](01-auth-key.md), [02](02-astrobox-bridge.md#5-mi-fitness-and-the-spp-channel) |
| Every service shows `KAPALI` immediately | FetchBridge not listening for the app | [02](02-astrobox-bridge.md#4-install-fetchbridge-and-listen-for-your-app) |
| One service shows `SORUN: DB Relay ID` | Your `/health/ready` JSON is missing component fields | [health-endpoint.md](health-endpoint.md#schema-a-component-based-ready) |
| Build fails on `config.js` | You didn't copy `config.example.js` | [03](03-build-deploy.md#2-create-your-configjs) |
