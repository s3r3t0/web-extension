# Extension Architecture

## Goal

The extension extracts cookie metadata from the active tab context and renders output for security reporting.

## Main runtime components

- Manifest and permissions in src/manifest.json
- Popup UI in src/popup/sereto.html
- Cookie retrieval and formatting logic in src/popup/sereto.js

## Data flow

1. User opens popup.
2. Extension reads active tab URL.
3. Extension retrieves cookies for relevant domain.
4. Cookies are transformed into one of three output modes:
   - Flags
   - Parent-domain cookies
   - Persistent cookies
5. Formatted output is shown in the textarea and can be copied.

## Known risk areas

- Domain filtering edge cases for subdomain and host-only cookies
- Parent-domain detection based on domain string shape
- Persistent classification based on expiration metadata
