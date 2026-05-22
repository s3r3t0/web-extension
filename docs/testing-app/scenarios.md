# Scenario Catalog

This page mirrors the scenario source of truth in cookie_lab/scenarios.py.

## Implemented baseline scenarios

- SC01 valid __Host- cookie
- SC02 invalid __Host- with Domain
- SC03 invalid __Host- with non-root path
- SC04 valid __Secure- cookie
- SC05 invalid __Secure- without Secure
- SC06 SameSite=None with Secure
- SC07 SameSite=None without Secure
- SC08 SameSite=Lax explicit
- SC09 SameSite=Strict explicit
- SC10 SameSite omitted
- SC11 parent-domain cookie
- SC12 host-only cookie
- SC13 path root cookie
- SC14 path nested cookie
- SC15 session cookie
- SC16 persistent cookie via Max-Age
- SC17 persistent cookie via Expires
- SC18 immediate expiry delete
