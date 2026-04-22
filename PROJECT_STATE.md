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
- Homepage now contains a minimal live read-only dashboard
- Homepage is connected to the live backend
- Homepage renders only contract-backed data that has been explicitly approved

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
- authenticated `/admin/drops` rendering verified

### Verified homepage content
The homepage currently renders only:
- API health status
- root API message
- admin summary values
- admin drops list

### Confirmed NOT implemented
- Admin entitlements section
- Payments UI
- Map view
- Multi-page dashboard structure
- Auth UI
- Role system
- Shared component system
- State management layer
- Filters/search/sort/tabs/charts
- Row actions or mutations

### Contract rule
Frontend work must follow `BACKEND_CONTRACT.md` exactly.
No frontend field, route, request shape, response shape, or rendered label may exceed the verified contract.

### Important rule
Anything not present in the repo or not present in `BACKEND_CONTRACT.md` is NOT IMPLEMENTED.

---

## Current phase

Phase 4 — Live admin drops validation complete

---

## Next approved task

Extend the homepage with one additional read-only contract-backed section only:
- admin entitlements list from `/admin/entitlements`

Allowed scope:
- reuse existing request helpers and type layer
- extend homepage only
- render only verified fields from admin entitlements response
- no filters
- no sorting UI
- no search
- no row actions
- no edit/create/delete controls
