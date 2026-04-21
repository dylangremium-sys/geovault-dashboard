# VERIFY.md

## Purpose

Defines how every step must be verified.

---

## Rules

- No step is complete without verification
- Verification must be command-based or file-based
- No “it should work”

---

## Backend verification

Use:

curl http://127.0.0.1:8000/health

Example checks:

- endpoint responds
- correct status code
- correct JSON shape

---

## Frontend verification (later)

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
