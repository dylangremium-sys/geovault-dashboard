# TASK.md

## Current task

DO NOT BUILD UI.

DO NOT WRITE COMPONENTS.

DO NOT ADD API CALLS.

---

## Task

Create contract-locked frontend types from `BACKEND_CONTRACT.md`.

---

## Steps

1. Inspect:
   - `BACKEND_CONTRACT.md`
   - current frontend file tree

2. Create only the minimal type file(s) needed to represent:
   - health response
   - root response
   - drop list item
   - admin drops response
   - admin entitlements response
   - admin summary response
   - claim request / success / out_of_range
   - reveal request / success
   - payments create request / success
   - payments callback handled responses

3. Keep every field exactly aligned to verified backend contract.

4. Do not invent:
   - optional frontend-only fields
   - labels
   - enums not proven by contract
   - UI helper types
   - filters/sort state
   - view models

---

## Output requirement

- Types only
- Exact contract alignment
- No assumptions
- No placeholders
- No frontend rendering code

---

## Completion condition

A minimal TypeScript type layer exists and every field maps directly to `BACKEND_CONTRACT.md`.
