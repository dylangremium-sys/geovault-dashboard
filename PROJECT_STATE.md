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
- `BACKEND_CONTRACT.md` exists and is derived from backend code
- contract-locked TypeScript API types exist
- minimal config layer exists
- minimal request layer exists
- homepage runtime verification completed successfully
- live backend connectivity verified
- authenticated `/admin/summary` rendering verified
- authenticated `/admin/drops` rendering verified
- authenticated `/admin/entitlements` rendering verified

### Verified homepage content
The homepage currently renders only:
- API health status
- root API message
- admin summary values
- admin drops list
- admin entitlements list

### Contract review result
Verified backend routes already represented in the frontend layer:
- `GET /health`
- `GET /`
- `GET /admin/summary`
- `GET /admin/drops`
- `GET /admin/entitlements`

Verified backend routes not yet implemented as homepage read-only rendering:
- none of the currently exposed GET admin list/summary routes remain unused

Verified backend routes present in contract but not appropriate as the next homepage read-only section:
- `POST /drops`
- `POST /claim`
- `POST /reveal`
- `POST /payments/create`
- `POST /payments/callback`

Reason:
- they are mutation or provider-driven flows, not the next smallest safe read-only homepage extension

### Confirmed NOT implemented
- Payments execution UI
- Drop creation UI
- Claim UI
- Reveal UI
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

Phase 6 — Contract review complete after core read-only admin coverage

---

## Next approved task

Do a control-file planning step to define the next implementation direction before adding new UI.

Approved planning options:
- keep homepage frozen and document this checkpoint
- approve a minimal mutation-safe technical preparation step only if contract-backed
- approve structural cleanup only if it does not change behavior

Not yet approved:
- new mutation UI
- payments flow UI
- claim/reveal UI
- extra pages
- speculative sections
