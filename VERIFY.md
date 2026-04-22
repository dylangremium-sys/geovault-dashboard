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
- confirm existing types and request helpers are reused
- confirm rendered fields are contract-backed only

---

## Frontend verification

For the first read-only page:
- only `app/page.tsx` changes unless explicitly required
- page uses existing `src/lib/api.ts`
- page uses existing `src/types/api.ts`
- rendered fields are limited to:
  - health status
  - root message
  - admin summary values
- no unapproved sections appear

Runtime checks:
- dev server runs
- page renders
- no console errors
- request failures are handled visibly

---

## Git verification

After each step:

git status
git log --oneline -5

---

## Absolute rule

If it is not verified, it does not exist.
