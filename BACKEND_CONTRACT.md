# BACKEND_CONTRACT.md

## Status
UNVERIFIED — DO NOT USE FOR IMPLEMENTATION

---

## Purpose

This file will contain the ONLY allowed source of truth
for frontend ↔ backend communication.

---

## Rules

- Do NOT write anything here from memory
- Do NOT copy from chat
- Do NOT assume endpoints
- Everything must come from:
  ~/geovault-protocol/gfp-motherboard

---

## Required verification

The following must be extracted from backend code:

For each endpoint:

- Route path
- HTTP method
- Headers required
- Auth requirements
- Request body shape
- Response shape
- Error responses

---

## Target endpoint groups

- /health
- /drops
- /drops/nearby
- /claim
- /payments/*
- /admin/*

---

## Current state

No endpoints verified yet.

DO NOT CONNECT FRONTEND TO BACKEND UNTIL THIS FILE IS COMPLETE.
