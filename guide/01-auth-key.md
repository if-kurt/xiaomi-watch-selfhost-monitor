# 1 · Getting the auth key

Xiaomi wearables only accept a Bluetooth session from a client that proves it
knows the watch's **auth key**: a 32-character hex string that Mi Fitness
creates when the watch is paired and stores in your Xiaomi cloud account.
AstroBox (and Gadgetbridge) need this key to talk to the watch.

> 🔐 **Treat the auth key like a password.** Anyone who has it and is within
> Bluetooth range can connect to your watch. Don't paste it into issues,
> screenshots, chats or commits.

## Option A — Xiaomi-cloud-tokens-extractor (recommended)

[Xiaomi-cloud-tokens-extractor](https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor)
by PiotrMachowski logs in to your Xiaomi account and lists the devices bound to
it, including their tokens/keys.

### 1. Run the tool

Pick one:

- **Windows** — download `token_extractor.exe` from the project's
  [releases](https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor/releases)
  and run it.
- **Linux / macOS**
  ```bash
  bash <(curl -L https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor/raw/master/run.sh)
  ```
- **Manual (Python)** — download `token_extractor.zip` from the releases, then:
  ```bash
  cd token_extractor
  pip3 install -r requirements.txt
  python3 token_extractor.py
  ```

### 2. Log in with a QR code

When asked how to log in, choose **QR code**. Scan it with an app that is
signed in to the **same Xiaomi account** the watch is bound to, and approve
the login.

QR login avoids typing your password into the tool and also avoids Xiaomi's
2FA limit (only a few verification codes per day, depending on region).

### 3. Choose the server region

Enter the region your account uses (for example `de` for Europe, `sg`,
`us`, `cn`), or leave it empty to search all regions.

### 4. Find the watch and copy its TOKEN

The tool prints every device on the account. Find your watch; its **TOKEN**
field is the auth key. Output looks roughly like this (illustrative, all values
masked):

```
   ---------
   NAME:     Xiaomi Watch S4
   ID:       000000000
   MAC:      AA:BB:CC:DD:EE:FF
   TOKEN:    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   MODEL:    xiaomi.watch.xxxxx
   ---------
```

Check that the value is exactly **32 hex characters** (`0-9`, `a-f`). Copy it
into a password manager — not into a file inside this repo.

## Option B — AstroBox's built-in Xiaomi account sync

AstroBox can also sign in to your Xiaomi account itself and import the device
(and its key) without you ever seeing it: *Settings → More settings → Xiaomi
account → Log in*. This is the simpler path if you only use AstroBox. Option A
is still useful when you need the key for Gadgetbridge, or want to keep the
Xiaomi login out of the bridge app.

## Warning: the key changes when you unpair

The auth key is generated **at pairing time**. If you unpair / reset the watch
in Mi Fitness and pair it again, Xiaomi issues a **new key** and the old one
stops working. After any re-pair:

1. Run the extractor again and get the new TOKEN.
2. Update the key in AstroBox (remove the saved device and add it again).

This is also the fix if you think the key leaked: unbind in Mi Fitness, pair
again, and the leaked key becomes useless.

## Keeping it out of git

The repo's `.gitignore` ignores files named `auth_key*`, `authkey*`,
`*secret*`, `*token*`, `*.key` and `*.pem`. If you must keep the key in a file
next to the project, use one of those names — but a password manager is better.

---

Next: [2 · AstroBox + FetchBridge](02-astrobox-bridge.md)
