# Coverage Matrix

## Categories

- Prefix constraints (`__Host-`, `__Secure-`)
- SameSite behavior (`Strict`, `Lax`, `None`, omitted)
- Domain scope (`host-only` vs `domain`)
- Path scope (`/` vs nested path)
- Persistence lifecycle (`session`, `Max-Age`, `Expires`, deletion)

## Current status

- [x] Scenario metadata
- [x] Scenario set/clear endpoints
- [x] Browser-ground-truth assertions in docs
- [x] Standards baseline with technical acceptance rules
- [x] Implementation reference (source-backed API docs)
- [x] Automated endpoint smoke tests
- [x] End-to-end browser automation against extension popup
- [x] Chromium runtime extension popup (optional target)
