# Publix CRM API

Mockup Customer Relationship Management API for Publix supermarket. Manages customer profiles, loyalty points, order records, and purchasing history analytics.

Built with **Python + Flask**, served by **Gunicorn**, interactive docs via **Swagger UI**, deployed on **Render**.

**Live:** https://publix-crm-api.onrender.com  
**Swagger UI:** https://publix-crm-api.onrender.com/docs  
**OpenAPI spec:** https://publix-crm-api.onrender.com/api/openapi.json

---

## Project structure

```
publix-crm-api/
├── app.py            Flask app — all routes, mock DB, OpenAPI spec
├── requirements.txt  flask, gunicorn
├── render.yaml       Render Blueprint (Python web service)
└── README.md
```

---

## Quick start

```bash
git clone https://github.com/your-username/publix-crm-api.git
cd publix-crm-api
pip install -r requirements.txt
python app.py
# → http://localhost:8000
# → http://localhost:8000/docs  (Swagger UI)
```

---

## Endpoints

All endpoints use `POST` with `Content-Type: application/json`.

| Method | Path | Description |
|---|---|---|
| POST | `/api/customers` | List customers with filters |
| POST | `/api/customers/profile` | Get full customer profile |
| POST | `/api/customers/search` | Search by name or email |
| POST | `/api/points/balance` | Points balance + tier info |
| POST | `/api/points/earn` | Award points for a purchase |
| POST | `/api/points/redeem` | Redeem points for dollar credit |
| POST | `/api/points/tiers` | List all loyalty tier definitions |
| POST | `/api/orders` | List orders with filters |
| POST | `/api/orders/detail` | Get full order with line items |
| POST | `/api/history/summary` | Customer spending summary |
| POST | `/api/history/by-category` | Spend breakdown by category |
| POST | `/api/history/top-products` | Most purchased products |
| POST | `/api/products` | Product catalog with points info |
| GET  | `/api/openapi.json` | OpenAPI 3.1 spec |
| GET  | `/health` | Health check |

---

## Loyalty tiers

| Tier | Lifetime Points | Multiplier | Key Perks |
|---|---|---|---|
| Green | 0–999 | 1.0× | Birthday bonus points |
| Silver | 1,000–4,999 | 1.25× | 5% off floral, free sub upgrade |
| Gold | 5,000–19,999 | 1.5× | 10% off deli, double points weekends |
| Platinum | 20,000+ | 2.0× | 15% off all, triple points, free delivery |

Points earn rate: **1 pt per $1** (multiplied by tier). Redemption rate: **100 pts = $1.00** (minimum 100 pts).

---

## Mock data

**6 customers** across FL and GA stores:

| ID | Name | Tier | Points |
|---|---|---|---|
| CUS-001 | Maria Gonzalez | Gold | 4,750 |
| CUS-002 | James Whitfield | Platinum | 9,820 |
| CUS-003 | Priya Nair | Silver | 1,230 |
| CUS-004 | Derek Fontaine | Green | 310 |
| CUS-005 | Angela Torres | Gold | 3,410 |
| CUS-006 | Robert Chen | Silver | 1,890 |

**8 orders** with full line-item detail, points earned/redeemed, and payment method.

**23 products** across 9 categories with points-per-dollar rates (1–3 pts/$).

---

## curl examples

```bash
BASE=https://publix-crm-api.onrender.com

# Customer profile
curl -X POST $BASE/api/customers/profile \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUS-001"}'

# Points balance + tier detail
curl -X POST $BASE/api/points/balance \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUS-002"}'

# Earn points for a purchase
curl -X POST $BASE/api/points/earn \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUS-001","purchase_amount":45.99,"order_id":"ORD-2026-0001"}'

# Redeem 500 points ($5.00 credit)
curl -X POST $BASE/api/points/redeem \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUS-001","points":500}'

# Order detail with line items
curl -X POST $BASE/api/orders/detail \
  -H "Content-Type: application/json" \
  -d '{"order_id":"ORD-2026-0003"}'

# Purchasing summary
curl -X POST $BASE/api/history/summary \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUS-002"}'

# Spend by category
curl -X POST $BASE/api/history/by-category \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUS-001"}'

# Top 5 most purchased products
curl -X POST $BASE/api/history/top-products \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUS-002","limit":5}'

# List Gold tier customers
curl -X POST $BASE/api/customers \
  -H "Content-Type: application/json" \
  -d '{"tier":"Gold"}'

# Search by name
curl -X POST $BASE/api/customers/search \
  -H "Content-Type: application/json" \
  -d '{"q":"torres"}'

# Products with 3 pts/$
curl -X POST $BASE/api/products \
  -H "Content-Type: application/json" \
  -d '{"min_points_ppd":3}'
```

---

## Deploy to Render

1. Push this repo to GitHub (all 4 files in repo root)
2. [dashboard.render.com](https://dashboard.render.com) → **New +** → **Web Service**
3. Connect repo → Render reads `render.yaml` → **Create Web Service**

| Setting | Value |
|---|---|
| Runtime | Python |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2` |
| Health check | `/health` |

---

## License

MIT
