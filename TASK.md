# TASK.md

## Current task

BUILD ONLY ONE READ-ONLY PAGE.

DO NOT ADD EXTRA PAGES.

DO NOT ADD NEW FEATURES.

---

## Task

Create the first minimal read-only dashboard page from verified contract data.

---

## Steps

1. Inspect:
   - `BACKEND_CONTRACT.md`
   - `src/types/api.ts`
   - `src/lib/api.ts`
   - current app file tree

2. Replace the scaffold homepage only.

3. The page may render only:
   - API health status from `/health`
   - root API message from `/`
   - admin summary values from `/admin/summary`

4. Render only verified fields already present in the contract and type layer.

5. Do not add:
   - charts
   - filters
   - search
   - tabs
   - mock sections
   - payments tables
   - drops tables
   - entitlement tables
   - map UI
   - auth UI
   - local state abstractions beyond what is strictly required

---

## Output requirement

- One minimal read-only page only
- Use existing config/api/types only
- Exact contract alignment
- No assumptions
- No placeholders beyond loading/error states

---

## Completion condition

`app/page.tsx` is replaced with a minimal read-only contract-aligned page that fetches and renders:
- health status
- root message
- admin summary
