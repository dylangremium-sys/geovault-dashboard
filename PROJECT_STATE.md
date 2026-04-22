# PROJECT_STATE.md

## Project
GeoVault Dashboard

## Repo path
~/geovault-dashboard

## Backend reference
~/geovault-protocol/gfp-motherboard

---

## Current factual state (VERIFIED)

### Frontend
- Next.js App Router project
- Minimal scaffold only
- No real dashboard implementation exists yet
- No dashboard routes or feature pages exist yet

### Existing frontend files
- app/layout.tsx
- app/page.tsx
- app/globals.css
- public assets
- config files

### Confirmed NOT implemented
- Admin dashboard UI
- Drops UI
- Payments UI
- Entitlements UI
- Map view
- API integration layer
- Typed frontend contract layer
- Auth system
- Role system
- Shared component system
- State management layer

### Backend contract status
- `BACKEND_CONTRACT.md` exists
- It has been derived from verified backend code
- Frontend work must follow this file exactly
- No frontend field, route, or state shape may exceed the verified contract

### Important rule
Anything not present in the repo or not present in `BACKEND_CONTRACT.md` is NOT IMPLEMENTED.

---

## Current phase

Phase 1 — Contract lock complete

---

## Next approved task

Create the frontend contract-aligned type layer only.

Allowed scope:
- read `BACKEND_CONTRACT.md`
- define exact frontend TypeScript types that mirror verified backend structures
- no UI
- no components
- no fetch logic
- no mock expansion beyond verified contract
