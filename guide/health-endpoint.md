# Health endpoint

Nabız needs one URL per service that returns **HTTP 200 with a JSON body**.
It auto-detects two JSON shapes. This page shows exactly how each response is
interpreted, plus nginx examples.

## How Nabız reads a response

| Response | Shown on the watch | Color |
|---|---|---|
| Non-2xx status (e.g. 404, 502) | `KAPALI (<code>)` | red* |
| Request failed (no network, DNS, TLS, timeout) | `KAPALI` | red* |
| 2xx but body isn't JSON | `KAPALI (yanit?)` | red* |
| Schema A, all components true | `SAĞLIKLI ✓ · <ms> ms` | green |
| Schema A, something false | `SORUN: DB Relay ID` (failing parts) | red* |
| Schema B, `status: "ok"`, fresh | `AYAKTA · v<version> · <ms> ms` | green |
| Schema B, `status: "ok"`, `time` older than 5 min | `AYAKTA (eski?)` | amber |
| Schema B, any other `status` | `SORUN (status)` | red* |
| Any other JSON object | `AYAKTA` | green |

\* A service only turns red after `FAIL_THRESHOLD` consecutive failures
(default 2). Before that it shows `kontrol… (1/2)` in amber.

## Schema A: component-based (`ready`)

Detected when the JSON has a `ready` key.

```json
{"ready":true,"database":true,"relay_server":true,"id_server":true}
```

Nabız treats the service as healthy only if `ready` is true **and** all three
component fields are true:

| Field | Label when false or missing |
|---|---|
| `database` | `DB` |
| `relay_server` | `Relay` |
| `id_server` | `ID` |

A missing field counts as false. If your service has different components,
either report these three keys or use Schema B. (The field names match a
typical relay/ID server setup; adapt `_evaluate()` in
`app/src/pages/index/index.ux` if you need other names.)

## Schema B: status-based (`status`)

Detected when the JSON has a `status` key (and no `ready` key).

```json
{"status":"ok","version":"1.4.2","time":"2026-01-01T12:00:00+00:00"}
```

- `status` must be exactly `"ok"`.
- `version` is optional; if present it is shown as `v1.4.2`.
- `time` is optional; if present it must be something `Date.parse()`
  understands (ISO 8601 is safest). If it differs from the watch's clock by
  more than **5 minutes**, the service is shown as suspicious (`AYAKTA (eski?)`)
  — this catches a cache or proxy serving an old response.

## nginx examples

### Static responses (proves nginx and TLS are up)

```nginx
server {
    listen 443 ssl;
    server_name example.com;
    # ssl_certificate / ssl_certificate_key ...

    # Schema A
    location = /health/ready {
        default_type application/json;
        add_header Cache-Control "no-store" always;
        return 200 '{"ready":true,"database":true,"relay_server":true,"id_server":true}';
    }

    # Schema B — $time_iso8601 is filled in by nginx on every request
    location = /health {
        default_type application/json;
        add_header Cache-Control "no-store" always;
        return 200 '{"status":"ok","version":"1.0.0","time":"$time_iso8601"}';
    }
}
```

A static `return` only tells you that nginx itself answers. For a real check,
let the application produce the JSON (querying its database, workers, etc.)
and proxy to it:

### Proxying to the application's own health check

```nginx
location = /health/ready {
    proxy_pass http://127.0.0.1:8080/health/ready;
    proxy_set_header Host $host;
    proxy_read_timeout 5s;
    add_header Cache-Control "no-store" always;
}
```

### Why `Cache-Control: no-store`

Health responses must never be cached — by nginx, a CDN, or anything in
between. A cached `{"status":"ok"}` would keep the watch green while the
service is down. `no-store` tells every cache not to keep the response, and
the `always` flag makes nginx send the header on error responses too.
Schema B's `time` field is the second line of defense: a cached body shows up
as stale.

## Test it

```bash
curl -si https://example.com/health/ready
```

Expect `HTTP/… 200`, `Content-Type: application/json`,
`Cache-Control: no-store`, and the JSON body. If `curl` gets that, Nabız will
too (as long as FetchBridge is listening).

## Security notes

- Return only booleans, a version and a timestamp — no hostnames, internal
  IPs, stack traces or error messages.
- The endpoint is public; if you don't want it to be, put it on a hard-to-guess
  path. Nabız can't send custom auth headers in its current form.
