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

Before any structural cleanup:
- confirm no new fields are introduced
- confirm no routes are added or removed
- confirm all existing rendered values still map to the contract

---

## Structural cleanup verification

For the next cleanup phase:
- behavior must remain identical
- same homepage sections must remain visible
- same request helpers must be used
- no new endpoints may be introduced
- no request-layer logic may change
- no type-layer meaning may change

Runtime checks after cleanup:
- dev server runs
- page renders
- no console errors
- health section still works
- summary still works
- drops still work
- entitlements still work

Type checks after cleanup:
- `npx tsc --noEmit` passes

---

## Git verification

After each step:

git status
git log --oneline -5

---

## Absolute rule

If it is not verified, it does not exist.
