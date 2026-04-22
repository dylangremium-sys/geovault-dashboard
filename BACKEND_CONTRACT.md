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

- `src/api/schemas.py` contains `ItemDropCreate`, but it is **not used** by the live routes inspected.
- `src/main.py` imports `require_admin_api_key` from `src.core.auth` and then defines a local function with the same name. Live behavior is still header-based admin key auth.
- Startup environment validation requires:
  - `DATABASE_URL`
  - `ADMIN_API_KEY`
  - `NOWPAYMENTS_API_KEY`
  - `NOWPAYMENTS_IPN_SECRET`
  - `BASE_URL`
- Payment invoice creation uses `BASE_API_URL` fallback logic for callback URL construction, even though startup validation checks `BASE_URL`.

---

## Verified live endpoints

### GET `/health`
Auth: none  
Headers required: none  
Query params: none  
Request body: none  

Success response:

    {
      "status": "ok"
    }

---

### GET `/`
Auth: none  
Headers required: none  
Query params: none  
Request body: none  

Success response:

    {
      "message": "GeoVault Protocol API running"
    }

---

### POST `/drops`
Auth: required  
Header required:

    x-api-key: <ADMIN_API_KEY>

Request shape:
- `w3w_address`: string
- `lat`: float
- `lng`: float
- `price_crypto`: float

Success response:

    {
      "status": "success",
      "id": number
    }

Verified failure responses:

    {
      "detail": "ADMIN_API_KEY not configured"
    }

    {
      "detail": "Unauthorized"
    }

    {
      "detail": "Drop already exists at this location"
    }

Notes:
- In the live FastAPI function, these inputs are declared as primitive parameters, not a Pydantic body model.

---

### GET `/drops/nearby`
Auth: none  
Headers required: none  

Query params:
- `lat`: float
- `lng`: float
- `radius_km`: float, optional, default `10`

Success response:

    [
      {
        "id": number,
        "distance_km": number,
        "status": "active"
      }
    ]

Notes:
- Only unclaimed drops are included.
- Items with missing coordinates are skipped.

---

### GET `/admin/drops`
Auth: required  
Header required:

    x-api-key: <ADMIN_API_KEY>

Success response:

    {
      "status": "success",
      "count": number,
      "items": [
        {
          "id": number,
          "w3w_address": string,
          "lat": float,
          "lng": float,
          "price_crypto": float,
          "is_claimed": boolean,
          "product_id": string | null
        }
      ]
    }

Verified failure responses:

    {
      "detail": "ADMIN_API_KEY not configured"
    }

    {
      "detail": "Unauthorized"
    }

---

### GET `/admin/entitlements`
Auth: required  
Header required:

    x-api-key: <ADMIN_API_KEY>

Success response:

    {
      "status": "success",
      "count": number,
      "items": [
        {
          "id": number,
          "drop_id": number,
          "payment_id": string,
          "is_used": boolean,
          "expires_at": string | null,
          "created_at": string | null
        }
      ]
    }

Verified failure responses:

    {
      "detail": "ADMIN_API_KEY not configured"
    }

    {
      "detail": "Unauthorized"
    }

---

### GET `/admin/summary`
Auth: required  
Header required:

    x-api-key: <ADMIN_API_KEY>

Success response:

    {
      "status": "success",
      "summary": {
        "total_drops": number,
        "claimed_drops": number,
        "total_entitlements": number,
        "used_entitlements": number
      }
    }

Verified failure responses:

    {
      "detail": "ADMIN_API_KEY not configured"
    }

    {
      "detail": "Unauthorized"
    }

---

### POST `/claim`
Auth: none  
Headers required: none  

Request body:

    {
      "drop_id": number,
      "lat": float,
      "lng": float,
      "entitlement_token": string
    }

Success response:

    {
      "status": "success",
      "distance_m": number,
      "drop_id": number
    }

Verified non-success responses:

Out of range:

    {
      "status": "out_of_range",
      "distance_m": number
    }

Drop not found:

    {
      "detail": "Drop not found"
    }

Entitlement validation failure:

    {
      "detail": "<validation message from entitlement checks>"
    }

Already claimed:

    {
      "detail": "Drop already claimed"
    }

Rate limited:

    {
      "detail": "Too many claim attempts"
    }

Notes:
- Entitlement must exist, match the drop, be unused, and be unexpired.
- On success, the entitlement is marked used.

---

### POST `/reveal`
Auth: none  
Headers required: none  

Request body:

    {
      "drop_id": number,
      "entitlement_token": string
    }

Success response:

    {
      "status": "success",
      "drop_id": number,
      "w3w_address": string,
      "product_id": string | null
    }

Verified non-success responses:

Drop not found:

    {
      "detail": "Drop not found"
    }

Entitlement validation failure:

    {
      "detail": "<validation message from entitlement checks>"
    }

Notes:
- Entitlement must exist, match the drop, be unexpired, and already be used.

---

### POST `/payments/create`
Auth: required  
Header required:

    x-api-key: <ADMIN_API_KEY>

Request body:

    {
      "drop_id": number,
      "price_currency": "usd",
      "pay_currency": "btc"
    }

Notes:
- `price_currency` defaults to `"usd"`.
- `pay_currency` defaults to `"btc"`.

Success response:

    {
      "status": "success",
      "drop_id": number,
      "price_used": number,
      "invoice": object
    }

Verified failure responses:

    {
      "detail": "ADMIN_API_KEY not configured"
    }

    {
      "detail": "Unauthorized"
    }

    {
      "detail": "Drop not found"
    }

    {
      "detail": "Drop already claimed"
    }

    {
      "detail": "Payment creation failed: <message>"
    }

---

### POST `/payments/callback`
Auth: provider callback with signature verification  
Header required:

    x-nowpayments-sig: <signature>

Request body:
- arbitrary NOWPayments callback JSON
- live code specifically reads:
  - `payment_status`
  - `order_id`
  - `payment_id`

Success response variants:

Ignored non-finished payment:

    {
      "status": "ignored",
      "payment_status": string | null
    }

Already processed payment:

    {
      "status": "already_processed",
      "drop_id": number,
      "payment_id": string,
      "entitlement_id": number
    }

New entitlement issued:

    {
      "status": "entitlement_issued",
      "drop_id": number,
      "payment_id": string,
      "entitlement_id": number
    }

Verified failure responses:

Invalid signature:

    {
      "detail": "Invalid NOWPayments signature"
    }

Missing order_id:

    {
      "detail": "Missing order_id in callback"
    }

Missing payment_id:

    {
      "detail": "Missing payment_id in callback"
    }

Drop not found:

    {
      "detail": "Drop not found"
    }

---

## Verified data model fields used by live routes

### ItemDrop
- `id`: integer
- `w3w_address`: string
- `lat`: float
- `lng`: float
- `product_id`: string | null
- `price_crypto`: float
- `is_claimed`: boolean
- `created_at`: datetime | null
- `is_paid`: boolean

### Entitlement
- `id`: integer
- `drop_id`: integer
- `payment_id`: string
- `token`: string
- `is_used`: boolean
- `expires_at`: datetime
- `created_at`: datetime

---

## Frontend contract rule

The frontend may only use:
- routes explicitly documented in this file
- fields explicitly documented in this file
- response variants explicitly documented in this file

If backend behavior changes, update this file first.
