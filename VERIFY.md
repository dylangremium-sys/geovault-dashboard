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

Before approving any new frontend task:
- read `BACKEND_CONTRACT.md`
- confirm the route or response actually exists
- confirm whether it is already covered in the frontend
- confirm whether it is read-only or mutation-driven
- confirm no extra fields are introduced

---

## Frontend verification

For review/control-file steps:
- no UI files change
- no type files change
- no request layer files change
- reviewed conclusion must be supported by the verified contract only

Later runtime checks:
- dev server runs
- page renders
- no console errors
- existing verified sections remain working

---

## Git verification

After each step:

git status
git log --oneline -5

---

## Absolute rule

If it is not verified, it does not exist.
