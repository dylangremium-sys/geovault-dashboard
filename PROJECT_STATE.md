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
- Minimal scaffold still in place
- No dashboard feature UI exists yet
- No dashboard routes or feature pages exist yet

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

### Confirmed NOT implemented
- Admin dashboard UI
- Drops UI
- Payments UI
- Entitlements UI
- Map view
- Read-only dashboard page
- Auth system
- Role system
- Shared component system
- State management layer

### Contract rule
Frontend work must follow `BACKEND_CONTRACT.md` exactly.
No frontend field, route, request shape, or response shape may exceed the verified contract.

### Important rule
Anything not present in the repo or not present in `BACKEND_CONTRACT.md` is NOT IMPLEMENTED.

---

## Current phase

Phase 2 — Contract foundation complete

---

## Next approved task

Create the first minimal read-only dashboard page using only verified API/config/types.

Allowed scope:
- create one read-only page
- use existing request helpers only
- use existing type layer only
- render only verified fields
- no extra dashboard features
- no invented filters, charts, tabs, or summaries
