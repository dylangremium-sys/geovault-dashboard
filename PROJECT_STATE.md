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
- Homepage contains a minimal live read-only dashboard
- Homepage is connected to the live backend
- Homepage renders only approved contract-backed data

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
- `BACKEND_CONTRACT.md` exists and has been repaired
- contract-locked TypeScript API types exist
- minimal config layer exists
- minimal request layer exists
- homepage runtime verification completed successfully
- live backend connectivity verified
- authenticated `/admin/summary` rendering verified
- authenticated `/admin/drops` rendering verified
- authenticated `/admin/entitlements` rendering verified
- Cursor contract review passes
- TypeScript type-check passes

### Verified homepage content
The homepage currently renders only:
- API health status
- root API message
- admin summary values
- admin drops list
- admin entitlements list

### Confirmed NOT implemented
- Payments UI
- Claim UI
- Reveal UI
- Drop creation UI
- Map view
- Multi-page dashboard structure
- Auth UI
- Role system
- Shared component system
- Filters/search/sort/tabs/charts
- Row actions or mutations

### Contract rule
Frontend work must follow `BACKEND_CONTRACT.md` exactly.
No frontend field, route, request shape, response shape, or rendered label may exceed the verified contract.

### Important rule
Anything not present in the repo or not present in `BACKEND_CONTRACT.md` is NOT IMPLEMENTED.

---

## Current phase

Phase 7 — Verified checkpoint frozen

---

## Next approved task

Structural cleanup only, with no behavior change.

Allowed scope:
- improve maintainability of the existing homepage code
- extract minimal presentational pieces only if behavior stays identical
- keep same routes
- keep same rendered fields
- keep same loading/error behavior
- keep same page content

Not allowed:
- new endpoints
- new UI sections
- new pages
- new features
- behavior changes
- auth flow changes
- request-layer changes
- contract changes
