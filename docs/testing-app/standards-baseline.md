# Standards Baseline

The testing app is a ground-truth oracle for browser cookie behavior.
Extension output is always compared against standards-based expected behavior.

## References

- [MDN Set-Cookie reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)
- [MDN cookie prefixes (`__Host-`, `__Secure-`)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#cookie_prefixes)
- [MDN SameSite semantics](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite)

## Acceptance principle

For each scenario, expected behavior must be defined by browser rules:

- Is the cookie stored or rejected?
- Is scope host-only or domain?
- Is persistence session or persistent?
- Which hosts and paths should receive the cookie?

Any extension output mismatch is treated as an extension bug candidate.

## Technical acceptance rules

### Prefix constraints

- `__Host-` cookies must include `Secure`, must include `Path=/`, and must not include `Domain`.
- `__Secure-` cookies must include `Secure`.
- Violations are expected to result in `storage=rejected`.

### SameSite constraints

- `SameSite=None` requires `Secure` in modern browser engines.
- `SameSite=Lax` and `SameSite=Strict` are valid explicit states.
- Omitted `SameSite` is treated as a default equivalent to `Lax` in current major browsers.

### Domain scope constraints

- Missing `Domain` implies host-only scope.
- Present `Domain` implies domain-scoped cookie delivery to matching subdomains.
- Domain scope expectations are evaluated against both `app.localtest.me` and `api.localtest.me`.

### Path scope constraints

- `Path=/` should match root and nested routes.
- `Path=/admin` should match only `/admin` subtree routes.
- Path behavior checks should include route-level verification where applicable (for example, `GET /admin`).

### Persistence constraints

- `Max-Age` or `Expires` defines persistent lifetime.
- No `Max-Age` and no `Expires` means session cookie.
- `Max-Age=0` or past `Expires` is a deletion/expiry case and should not produce durable storage.
- If both are present, browser precedence rules apply and should be interpreted according to standards behavior.

## Scenario evaluation checklist

For each scenario:

1. Compare app metadata from `GET /api/scenarios` with expectations in `browser_expectation`.
2. Validate cookie result in browser tools: existence, `Domain`, `Path`, `Secure`, `HttpOnly`, `SameSite`, and expiry fields.
3. Confirm scope behavior by checking host transitions (`app.localtest.me` vs `api.localtest.me`) and path transitions (`/` vs `/admin`).
4. Compare extension output modes (flags, parent-domain, persistent) with `extension_expectation`.
5. Record any mismatch as a bug candidate with scenario ID and observed browser/version context.
