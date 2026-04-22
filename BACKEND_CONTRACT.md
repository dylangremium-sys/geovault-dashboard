# BACKEND_CONTRACT.md

## Source of truth
Verified from:
- `~/geovault-protocol/gfp-motherboard/src/main.py`
- `~/geovault-protocol/gfp-motherboard/src/api/payments.py`
- `~/geovault-protocol/gfp-motherboard/src/db/models.py`
- `~/geovault-protocol/gfp-motherboard/src/core/auth.py`
- `~/geovault-protocol/gfp-motherboard/src/core/config.py`

Only routes and structures explicitly present in those files are included below.

---

## Notes
- `src/api/schemas.py` contains `ItemDropCreate`, but it is **not used** by live routes.
- `src/main.py` defines a local `require_admin_api_key` that overrides the imported one; behavior is header-based API key.
- Startup requires env:
  - `DATABASE_URL`
  - `ADMIN_API_KEY`
  - `NOWPAYMENTS_API_KEY`
  - `NOWPAYMENTS_IPN_SECRET`
  - `BASE_URL`
- Payments use `BASE_API_URL` fallback for callback URL, while validation checks `BASE_URL`.

---

## Endpoints

### GET `/health`
Auth: none  
Response:
```json
{ "status": "ok" }