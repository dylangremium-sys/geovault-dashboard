# VERIFY.md

## Purpose

Defines how every step must be verified.

---

## Rules

- No step is complete without verification
- Verification must be command-based or file-based
- No “it should work”
- `BACKEND_CONTRACT.md` is the source of truth for all frontend fields

---

## Contract verification

Before frontend implementation:
- read `BACKEND_CONTRACT.md`
- confirm no extra fields are introduced
- confirm existing request helpers and types are reused
- confirm rendered fields are contract-backed only

---

## Frontend verification

For the homepage extension step:
- only approved files change
- homepage still renders existing validated sections
- added section uses `/admin/drops`
- rendered item fields are limited to:
  - `id`
  - `w3w_address`
  - `lat`
  - `lng`
  - `price_crypto`
  - `is_claimed`
  - `product_id`
- no unapproved controls or sections appear

Runtime checks:
- dev server runs
- page renders
- no console errors
- existing summary still works
- admin drops section renders real backend data or visible error state

---

## Git verification

After each step:

git status
git log --oneline -5

---

## Absolute rule

If it is not verified, it does not exist.
