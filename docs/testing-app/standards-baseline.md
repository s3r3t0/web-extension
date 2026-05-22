# Standards Baseline

The testing app is a ground-truth oracle for browser cookie behavior. Extension output is always compared against standards-based expected behavior.

## References

- RFC 6265 and browser-compatible cookie behavior
- MDN cookie guidance

## Acceptance principle

For each scenario, expected behavior must be defined by browser rules:

- Is the cookie stored or rejected?
- Is it host-only or domain-scoped?
- Is it session or persistent?
- Which paths and hosts should receive it?

Any extension output mismatch is treated as an extension bug candidate.
