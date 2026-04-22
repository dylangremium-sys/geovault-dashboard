# VERIFY.md

## Purpose

Defines how every step must be verified.

---

## Rules

- No step is complete without verification
- Verification must be command-based or file-based
- No “it should work”
- For frontend contract work, `BACKEND_CONTRACT.md` is the source of truth

---

## Contract verification

Before frontend implementation:
- read `BACKEND_CONTRACT.md`
- confirm no extra fields are introduced
- confirm every added type maps to verified backend structures only

---

## Frontend verification

For type-layer steps:
- file exists in repo
- file contents match verified contract
- TypeScript compiles if applicable
- no UI files changed unless explicitly approved

Later frontend checks:
- dev server runs
- no console errors
- layout renders correctly

---

## Git verification

After each step:

git status
git log --oneline -5

---

## Absolute rule

If it is not verified, it does not exist.
