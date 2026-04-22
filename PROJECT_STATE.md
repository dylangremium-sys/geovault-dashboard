# PROJECT_STATE.md

## Project
GeoVault Dashboard

## Repo path
~/geovault-dashboard

## Backend reference
~/geovault-protocol/gfp-motherboard

---

## Current factual state (VERIFIED)

### Frontend foundation
- Next.js App Router project
- Minimal dashboard implementation now exists on the homepage
- Homepage is connected to the live backend
- Homepage renders verified contract-backed data only

### Existing frontend files
- app/layout.tsx
- app/page.tsx
- app/globals.css
- src/types/api.ts
- src/lib/config.ts
- src/lib/api.ts
- public assets
- config files

### Verified completed implementation
- `BACKEND_CONTRACT.md` exists and is derived from backend code
- contract-locked TypeScript API types exist
- minimal config layer exists
- minimal request layer exists
- first minimal read-only page exists
- runtime verification completed successfully
- live backend connectivity verified
- authenticated `/admin/summary` rendering verified

### Verified homepage content
The homepage currently renders only:
- API health status
- root API message
- admin summary values

### Confirmed NOT implemented
- Admin drops list page/section
- Payments UI
- Entitlements UI
- Map view
- Multi-page dashboard structure
- Auth UI
- Role system
- Shared component system
- State management layer
- Filters/search/sort/tabs/charts

### Contract rule
Frontend work must follow `BACKEND_CONTRACT.md` exactly.
No frontend field, route, request shape, response shape, or rendered label may exceed the verified contract.

### Important rule
Anything not present in the repo or not present in `BACKEND_CONTRACT.md` is NOT IMPLEMENTED.

---

## Current phase

Phase 3 — Live read-only validation complete

---

## Next approved task

Extend the homepage with one additional read-only contract-backed section only:
- admin drops list from `/admin/drops`

Allowed scope:
- reuse existing request helpers and type layer
- extend homepage only
- render only verified fields from admin drops response
- no filters
- no sorting UI
- no search
- no row actions
- no edit/create/delete controls
