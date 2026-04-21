# BACKEND_CONTRACT.md

## Source of truth
Verified from:
- ~/geovault-protocol/gfp-motherboard/src/main.py
- ~/geovault-protocol/gfp-motherboard/src/api/payments.py
- ~/geovault-protocol/gfp-motherboard/src/db/models.py
- ~/geovault-protocol/gfp-motherboard/src/core/auth.py
- ~/geovault-protocol/gfp-motherboard/src/core/config.py

---

## Verified endpoints

GET /health
Response:
{ "status": "ok" }

GET /
Response:
{ "message": "GeoVault Protocol API running" }

POST /drops
Auth: x-api-key required
Input:
- w3w_address: string
- lat: float
- lng: float
- price_crypto: float
Response:
{ "status": "success", "id": number }

GET /drops/nearby
Query:
- lat: float
- lng: float
- radius_km: float (default 10)
Response:
[
  { "id": number, "distance_km": number, "status": "active" }
]

GET /admin/drops
Auth: x-api-key required

GET /admin/entitlements
Auth: x-api-key required

GET /admin/summary
Auth: x-api-key required

POST /claim
Input:
- drop_id: number
- lat: float
- lng: float
- entitlement_token: string

POST /reveal
Input:
- drop_id: number
- entitlement_token: string

POST /payments/create
Auth: x-api-key required

POST /payments/callback
Header:
- x-nowpayments-sig
