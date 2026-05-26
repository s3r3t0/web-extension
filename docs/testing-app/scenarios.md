# Scenario Catalog

This page mirrors the scenario source of truth in `cookie_lab/scenarios.py`.

## Scenarios

| ID | Short description |
| --- | --- |
| [`SC01`](#sc01) | Valid `__Host-` cookie. |
| [`SC02`](#sc02) | Invalid `__Host-` cookie with `Domain`. |
| [`SC03`](#sc03) | Invalid `__Host-` cookie with non-root `Path`. |
| [`SC04`](#sc04) | Valid `__Secure-` cookie. |
| [`SC05`](#sc05) | Invalid `__Secure-` cookie without `Secure`. |
| [`SC06`](#sc06) | `SameSite=None` cookie with `Secure`. |
| [`SC07`](#sc07) | `SameSite=None` cookie without `Secure`. |
| [`SC08`](#sc08) | Explicit `SameSite=Lax`. |
| [`SC09`](#sc09) | Explicit `SameSite=Strict`. |
| [`SC10`](#sc10) | `SameSite` omitted (default behavior case). |
| [`SC11`](#sc11) | Domain-scoped cookie (`Domain=localtest.me`). |
| [`SC12`](#sc12) | Host-only cookie (no `Domain`). |
| [`SC13`](#sc13) | Root path cookie (`Path=/`). |
| [`SC14`](#sc14) | Nested path cookie (`Path=/admin`). |
| [`SC15`](#sc15) | Session cookie (no persistence attributes). |
| [`SC16`](#sc16) | Persistent cookie via `Max-Age`. |
| [`SC17`](#sc17) | Persistent cookie via `Expires`. |
| [`SC18`](#sc18) | Immediate expiry/deletion case. |

### `SC01` Valid `__Host-` cookie {#sc01}

- Expected result: `stored`, `host-only`, `session`.
- Focus: valid prefix contract (`Secure`, `Path=/`, no `Domain`).

### `SC02` Invalid `__Host-` with `Domain` {#sc02}

- Expected result: `rejected`.
- Focus: `__Host-` cookies must not carry a `Domain` attribute.

### `SC03` Invalid `__Host-` with non-root path {#sc03}

- Expected result: `rejected`.
- Focus: `__Host-` requires `Path=/`.

### `SC04` Valid `__Secure-` cookie {#sc04}

- Expected result: `stored`.
- Focus: secure prefix case with valid `Secure` attribute over HTTPS.

### `SC05` Invalid `__Secure-` without `Secure` {#sc05}

- Expected result: `rejected`.
- Focus: `__Secure-` requires `Secure`.

### `SC06` `SameSite=None` with `Secure` {#sc06}

- Expected result: `stored`.
- Focus: modern browser requirement `SameSite=None` + `Secure`.

### `SC07` `SameSite=None` without `Secure` {#sc07}

- Expected result: `rejected`.
- Focus: invalid SameSite/secure combination.

### `SC08` `SameSite=Lax` explicit {#sc08}

- Expected result: `stored`.
- Focus: explicit `Lax` control path.

### `SC09` `SameSite=Strict` explicit {#sc09}

- Expected result: `stored`.
- Focus: explicit `Strict` control path.

### `SC10` `SameSite` omitted {#sc10}

- Expected result: `stored`.
- Focus: default SameSite behavior in modern browsers.

### `SC11` Parent-domain cookie {#sc11}

- Expected result: `stored`, scope `domain`.
- Focus: cookie should be available across matching subdomains.

### `SC12` Host-only cookie {#sc12}

- Expected result: `stored`, scope `host-only`.
- Focus: no `Domain` attribute, not sent to sibling subdomains.

### `SC13` Path root cookie {#sc13}

- Expected result: `stored`, `path_scope=/`.
- Focus: root path matching behavior.

### `SC14` Path nested cookie {#sc14}

- Expected result: `stored`, `path_scope=/admin`.
- Focus: nested path subtree matching behavior.

### `SC15` Session cookie {#sc15}

- Expected result: `stored`, persistence `session`.
- Focus: no `Max-Age` and no `Expires`.

### `SC16` Persistent cookie via `Max-Age` {#sc16}

- Expected result: `stored`, persistence `persistent`.
- Focus: relative lifetime from `Max-Age`.

### `SC17` Persistent cookie via `Expires` {#sc17}

- Expected result: `stored`, persistence `persistent`.
- Focus: absolute UTC expiration date behavior.

### `SC18` Immediate expiry delete {#sc18}

- Expected result: `rejected`/not durable.
- Focus: `Max-Age=0` and past `Expires` deletion semantics.
