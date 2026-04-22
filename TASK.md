# TASK.md

## Current task

EXTEND ONLY THE EXISTING HOMEPAGE.

DO NOT ADD EXTRA PAGES.

DO NOT ADD NEW FEATURES.

---

## Task

Add one minimal read-only admin entitlements section to `app/page.tsx`.

---

## Steps

1. Inspect:
   - `BACKEND_CONTRACT.md`
   - `src/types/api.ts`
   - `src/lib/api.ts`
   - `app/page.tsx`

2. Reuse the existing homepage only.

3. Add one additional read-only section backed by:
   - `/admin/entitlements`

4. Render only verified fields from each entitlement item:
   - `id`
   - `drop_id`
   - `payment_id`
   - `is_used`
   - `expires_at`
   - `created_at`

5. Keep the presentation minimal.
   A simple stacked list or plain table is acceptable.

6. Do not add:
   - filters
   - search
   - tabs
   - charts
   - buttons
   - edit actions
   - pagination
   - row expansion
   - client-side state abstractions unless strictly required

---

## Output requirement

- Homepage only
- One additional read-only section only
- Use existing config/api/types only
- Exact contract alignment
- No assumptions
- No placeholders beyond loading/error states

---

## Completion condition

`app/page.tsx` renders:
- health status
- root message
- admin summary
- admin drops list
- admin entitlements list

All fields must map directly to verified contract data.
