# TASK.md

## Current task

STRUCTURAL CLEANUP ONLY.

NO BEHAVIOR CHANGE.

NO NEW FEATURES.

---

## Task

Prepare the repo for safe structural cleanup of the existing homepage only.

---

## Steps

1. Inspect:
   - `app/page.tsx`
   - `src/lib/api.ts`
   - `src/types/api.ts`
   - `BACKEND_CONTRACT.md`

2. Keep current behavior exactly the same.

3. Any future cleanup step may only:
   - reduce duplication
   - improve readability
   - extract minimal presentational helpers/components
   - preserve all current rendered fields and request usage

4. Do not change:
   - routes used
   - response handling behavior
   - page sections
   - field names
   - auth behavior
   - request flow

---

## Output requirement

- No implementation in this block
- Control files only
- Exact contract alignment
- Zero behavior expansion

---

## Completion condition

The repo control files clearly lock the next phase as structural cleanup only, with no behavior change.
