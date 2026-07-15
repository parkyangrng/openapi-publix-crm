'use strict' if False else None  # Python file

from flask import Flask, jsonify, request, render_template_string, redirect
from datetime import datetime, date
import math, copy, random

app = Flask(__name__, static_folder='public', static_url_path='')

# ─── Mock Database ────────────────────────────────────────────────────────────

CUSTOMERS = {
    "CUS-001": {
        "id": "CUS-001", "first_name": "Maria", "last_name": "Gonzalez",
        "email": "maria.gonzalez@email.com",
        "phone": "(301) 326-3739",
        "mobile": "(301) 326-3739",
        "store_id": "store_FL01", "tier": "Gold",
        "points_balance": 4750, "lifetime_points": 12340,
        "joined": "2021-03-15",
        "birthday": "1988-06-14",
        "address": {
            "street": "245 Brickell Ave", "apt": "Apt 18B",
            "city": "Miami", "state": "FL", "zip": "33129",
            "country": "US"
        },
        "preferences": ["organic", "gluten-free"], "active": True
    },
    "CUS-002": {
        "id": "CUS-002", "first_name": "James", "last_name": "Whitfield",
        "email": "j.whitfield@email.com",
        "phone": "(404) 871-2256",
        "mobile": "(404) 993-7741",
        "store_id": "store_GA01", "tier": "Platinum",
        "points_balance": 9820, "lifetime_points": 48900,
        "joined": "2019-08-22",
        "birthday": "1975-11-03",
        "address": {
            "street": "3310 Peachtree Rd NE", "apt": "Unit 4A",
            "city": "Atlanta", "state": "GA", "zip": "30326",
            "country": "US"
        },
        "preferences": ["deli", "seafood"], "active": True
    },
    "CUS-003": {
        "id": "CUS-003", "first_name": "Priya", "last_name": "Nair",
        "email": "priya.nair@email.com",
        "phone": "(305) 446-9012",
        "mobile": "(305) 781-6623",
        "store_id": "store_FL02", "tier": "Silver",
        "points_balance": 1230, "lifetime_points": 5670,
        "joined": "2022-11-01",
        "birthday": "1994-03-27",
        "address": {
            "street": "88 Coral Way", "apt": "Suite 202",
            "city": "Coral Gables", "state": "FL", "zip": "33133",
            "country": "US"
        },
        "preferences": ["vegetarian", "dairy-free"], "active": True
    },
    "CUS-004": {
        "id": "CUS-004", "first_name": "Derek", "last_name": "Fontaine",
        "email": "derek.fontaine@email.com",
        "phone": "(786) 230-5587",
        "mobile": "(786) 904-1132",
        "store_id": "store_FL03", "tier": "Green",
        "points_balance": 310, "lifetime_points": 980,
        "joined": "2023-06-10",
        "birthday": "2000-08-19",
        "address": {
            "street": "190 NW 2nd Ave", "apt": "Apt 7",
            "city": "Miami", "state": "FL", "zip": "33128",
            "country": "US"
        },
        "preferences": ["bakery", "beverages"], "active": True
    },
    "CUS-005": {
        "id": "CUS-005", "first_name": "Angela", "last_name": "Torres",
        "email": "angela.torres@email.com",
        "phone": "(404) 523-6690",
        "mobile": "(404) 817-4459",
        "store_id": "store_GA02", "tier": "Gold",
        "points_balance": 3410, "lifetime_points": 15200,
        "joined": "2020-05-28",
        "birthday": "1991-01-08",
        "address": {
            "street": "650 Ponce De Leon Ave NE", "apt": "Apt 3C",
            "city": "Atlanta", "state": "GA", "zip": "30308",
            "country": "US"
        },
        "preferences": ["meat", "pantry"], "active": True
    },
    "CUS-006": {
        "id": "CUS-006", "first_name": "Robert", "last_name": "Chen",
        "email": "rob.chen@email.com",
        "phone": "(305) 667-3318",
        "mobile": "(305) 924-8807",
        "store_id": "store_FL04", "tier": "Silver",
        "points_balance": 1890, "lifetime_points": 7340,
        "joined": "2022-02-14",
        "birthday": "1986-09-22",
        "address": {
            "street": "3401 Main Hwy", "apt": "Unit 12",
            "city": "Coconut Grove", "state": "FL", "zip": "33133",
            "country": "US"
        },
        "preferences": ["organic", "produce"], "active": True
    },
}

PRODUCTS = {
    "PRD-BAN-ORG": {"name": "Organic Bananas",          "category": "produce",   "price": 0.69,  "points_per_dollar": 2},
    "PRD-APL-HON": {"name": "Honeycrisp Apples",         "category": "produce",   "price": 2.29,  "points_per_dollar": 2},
    "PRD-STR-ORG": {"name": "Organic Strawberries 1lb",  "category": "produce",   "price": 5.49,  "points_per_dollar": 2},
    "PRD-AVC-HAS": {"name": "Hass Avocado",               "category": "produce",   "price": 1.49,  "points_per_dollar": 2},
    "DRY-MLK-WHL": {"name": "Whole Milk Gallon",          "category": "dairy",     "price": 4.59,  "points_per_dollar": 1},
    "DRY-OAT-PLN": {"name": "Oat Milk Barista 32oz",      "category": "dairy",     "price": 5.49,  "points_per_dollar": 1},
    "DRY-EGG-LRG": {"name": "Large Eggs Dozen",           "category": "dairy",     "price": 6.29,  "points_per_dollar": 1},
    "DRY-CHZ-CHD": {"name": "Sharp Cheddar Block 16oz",   "category": "dairy",     "price": 6.99,  "points_per_dollar": 1},
    "BKR-BRD-SRD": {"name": "Sourdough Loaf",             "category": "bakery",    "price": 4.99,  "points_per_dollar": 2},
    "BKR-CRW-BUT": {"name": "Butter Croissant",           "category": "bakery",    "price": 2.29,  "points_per_dollar": 2},
    "MET-CHK-BRS": {"name": "Chicken Breast Boneless",    "category": "meat",      "price": 5.99,  "points_per_dollar": 3},
    "MET-SAL-ATL": {"name": "Atlantic Salmon Fillet",     "category": "meat",      "price": 13.99, "points_per_dollar": 3},
    "MET-GBF-8020":{"name": "Ground Beef 80/20 1lb",      "category": "meat",      "price": 6.99,  "points_per_dollar": 3},
    "MET-STK-RIB": {"name": "Ribeye Steak",               "category": "meat",      "price": 16.99, "points_per_dollar": 3},
    "BEV-OJ-NAT":  {"name": "Orange Juice 52oz",           "category": "beverages", "price": 5.79,  "points_per_dollar": 1},
    "BEV-COF-GRD": {"name": "Ground Coffee Medium 12oz",   "category": "beverages", "price": 8.99,  "points_per_dollar": 1},
    "PNT-PST-SPN": {"name": "Spaghetti 16oz",              "category": "pantry",    "price": 1.89,  "points_per_dollar": 1},
    "PNT-OLV-OIL": {"name": "Extra Virgin Olive Oil",      "category": "pantry",    "price": 8.99,  "points_per_dollar": 1},
    "DLI-TKY-RST": {"name": "Oven Roasted Turkey Breast",  "category": "deli",      "price": 10.99, "points_per_dollar": 2},
    "DLI-SUB-ITA": {"name": "Italian Sub 12-inch",         "category": "deli",      "price": 9.99,  "points_per_dollar": 2},
    "FRZ-ICE-VNL": {"name": "Vanilla Bean Ice Cream",      "category": "frozen",    "price": 5.99,  "points_per_dollar": 1},
    "PHR-VIT-C":   {"name": "Vitamin C 1000mg 100ct",       "category": "pharmacy",  "price": 9.99,  "points_per_dollar": 1},
    "FLR-RSE-DZN": {"name": "Red Rose Bouquet Dozen",       "category": "floral",    "price": 19.99, "points_per_dollar": 3},
}

ORDERS = {
    "ORD-2026-0001": {
        "id": "ORD-2026-0001", "customer_id": "CUS-001", "store_id": "store_FL01",
        "date": "2026-07-14", "status": "completed",
        "items": [
            {"sku": "PRD-BAN-ORG", "name": "Organic Bananas",        "qty": 2,  "unit_price": 0.69,  "subtotal": 1.38},
            {"sku": "DRY-OAT-PLN", "name": "Oat Milk Barista 32oz",  "qty": 3,  "unit_price": 5.49,  "subtotal": 16.47},
            {"sku": "BKR-BRD-SRD", "name": "Sourdough Loaf",         "qty": 1,  "unit_price": 4.99,  "subtotal": 4.99},
            {"sku": "MET-SAL-ATL", "name": "Atlantic Salmon Fillet",  "qty": 1,  "unit_price": 13.99, "subtotal": 13.99},
        ],
        "subtotal": 36.83, "tax": 2.58, "total": 39.41,
        "points_earned": 74, "points_redeemed": 0, "payment": "credit_card"
    },
    "ORD-2026-0002": {
        "id": "ORD-2026-0002", "customer_id": "CUS-001", "store_id": "store_FL01",
        "date": "2026-07-07", "status": "completed",
        "items": [
            {"sku": "PRD-STR-ORG", "name": "Organic Strawberries",   "qty": 2,  "unit_price": 5.49,  "subtotal": 10.98},
            {"sku": "DRY-EGG-LRG", "name": "Large Eggs Dozen",       "qty": 1,  "unit_price": 6.29,  "subtotal": 6.29},
            {"sku": "DRY-CHZ-CHD", "name": "Sharp Cheddar Block",     "qty": 1,  "unit_price": 6.99,  "subtotal": 6.99},
            {"sku": "BKR-CRW-BUT", "name": "Butter Croissant",        "qty": 4,  "unit_price": 2.29,  "subtotal": 9.16},
        ],
        "subtotal": 33.42, "tax": 2.34, "total": 35.76,
        "points_earned": 67, "points_redeemed": 500, "payment": "publix_card"
    },
    "ORD-2026-0003": {
        "id": "ORD-2026-0003", "customer_id": "CUS-002", "store_id": "store_GA01",
        "date": "2026-07-13", "status": "completed",
        "items": [
            {"sku": "MET-STK-RIB", "name": "Ribeye Steak",           "qty": 2,  "unit_price": 16.99, "subtotal": 33.98},
            {"sku": "DLI-TKY-RST", "name": "Oven Roasted Turkey",    "qty": 1,  "unit_price": 10.99, "subtotal": 10.99},
            {"sku": "PNT-OLV-OIL", "name": "Extra Virgin Olive Oil", "qty": 2,  "unit_price": 8.99,  "subtotal": 17.98},
            {"sku": "BEV-COF-GRD", "name": "Ground Coffee",          "qty": 2,  "unit_price": 8.99,  "subtotal": 17.98},
            {"sku": "FLR-RSE-DZN", "name": "Red Rose Bouquet",       "qty": 1,  "unit_price": 19.99, "subtotal": 19.99},
        ],
        "subtotal": 100.92, "tax": 7.06, "total": 107.98,
        "points_earned": 303, "points_redeemed": 0, "payment": "credit_card"
    },
    "ORD-2026-0004": {
        "id": "ORD-2026-0004", "customer_id": "CUS-002", "store_id": "store_GA01",
        "date": "2026-07-05", "status": "completed",
        "items": [
            {"sku": "MET-CHK-BRS", "name": "Chicken Breast",         "qty": 3,  "unit_price": 5.99,  "subtotal": 17.97},
            {"sku": "MET-GBF-8020","name": "Ground Beef 80/20",       "qty": 2,  "unit_price": 6.99,  "subtotal": 13.98},
            {"sku": "DLI-SUB-ITA", "name": "Italian Sub 12-inch",     "qty": 2,  "unit_price": 9.99,  "subtotal": 19.98},
            {"sku": "BEV-OJ-NAT",  "name": "Orange Juice 52oz",       "qty": 2,  "unit_price": 5.79,  "subtotal": 11.58},
        ],
        "subtotal": 63.51, "tax": 4.45, "total": 67.96,
        "points_earned": 191, "points_redeemed": 1000, "payment": "publix_card"
    },
    "ORD-2026-0005": {
        "id": "ORD-2026-0005", "customer_id": "CUS-003", "store_id": "store_FL02",
        "date": "2026-07-12", "status": "completed",
        "items": [
            {"sku": "PRD-AVC-HAS", "name": "Hass Avocado",            "qty": 4,  "unit_price": 1.49,  "subtotal": 5.96},
            {"sku": "DRY-OAT-PLN", "name": "Oat Milk Barista 32oz",   "qty": 2,  "unit_price": 5.49,  "subtotal": 10.98},
            {"sku": "PRD-STR-ORG", "name": "Organic Strawberries",    "qty": 1,  "unit_price": 5.49,  "subtotal": 5.49},
            {"sku": "PNT-PST-SPN", "name": "Spaghetti 16oz",          "qty": 3,  "unit_price": 1.89,  "subtotal": 5.67},
        ],
        "subtotal": 28.10, "tax": 1.97, "total": 30.07,
        "points_earned": 28, "points_redeemed": 0, "payment": "debit_card"
    },
    "ORD-2026-0006": {
        "id": "ORD-2026-0006", "customer_id": "CUS-004", "store_id": "store_FL03",
        "date": "2026-07-11", "status": "completed",
        "items": [
            {"sku": "BKR-BRD-SRD", "name": "Sourdough Loaf",          "qty": 1,  "unit_price": 4.99,  "subtotal": 4.99},
            {"sku": "BKR-CRW-BUT", "name": "Butter Croissant",         "qty": 6,  "unit_price": 2.29,  "subtotal": 13.74},
            {"sku": "BEV-COF-GRD", "name": "Ground Coffee",            "qty": 1,  "unit_price": 8.99,  "subtotal": 8.99},
            {"sku": "BEV-OJ-NAT",  "name": "Orange Juice 52oz",        "qty": 1,  "unit_price": 5.79,  "subtotal": 5.79},
        ],
        "subtotal": 33.51, "tax": 2.35, "total": 35.86,
        "points_earned": 34, "points_redeemed": 0, "payment": "cash"
    },
    "ORD-2026-0007": {
        "id": "ORD-2026-0007", "customer_id": "CUS-005", "store_id": "store_GA02",
        "date": "2026-07-14", "status": "completed",
        "items": [
            {"sku": "MET-CHK-BRS", "name": "Chicken Breast",          "qty": 4,  "unit_price": 5.99,  "subtotal": 23.96},
            {"sku": "MET-GBF-8020","name": "Ground Beef 80/20",        "qty": 3,  "unit_price": 6.99,  "subtotal": 20.97},
            {"sku": "PNT-OLV-OIL", "name": "Extra Virgin Olive Oil",  "qty": 1,  "unit_price": 8.99,  "subtotal": 8.99},
            {"sku": "PNT-PST-SPN", "name": "Spaghetti 16oz",          "qty": 4,  "unit_price": 1.89,  "subtotal": 7.56},
            {"sku": "PHR-VIT-C",   "name": "Vitamin C 1000mg",         "qty": 1,  "unit_price": 9.99,  "subtotal": 9.99},
        ],
        "subtotal": 71.47, "tax": 5.00, "total": 76.47,
        "points_earned": 214, "points_redeemed": 0, "payment": "credit_card"
    },
    "ORD-2026-0008": {
        "id": "ORD-2026-0008", "customer_id": "CUS-006", "store_id": "store_FL04",
        "date": "2026-07-10", "status": "completed",
        "items": [
            {"sku": "PRD-BAN-ORG", "name": "Organic Bananas",         "qty": 3,  "unit_price": 0.69,  "subtotal": 2.07},
            {"sku": "PRD-APL-HON", "name": "Honeycrisp Apples",       "qty": 2,  "unit_price": 2.29,  "subtotal": 4.58},
            {"sku": "PRD-AVC-HAS", "name": "Hass Avocado",            "qty": 6,  "unit_price": 1.49,  "subtotal": 8.94},
            {"sku": "DRY-MLK-WHL", "name": "Whole Milk Gallon",       "qty": 1,  "unit_price": 4.59,  "subtotal": 4.59},
            {"sku": "FRZ-ICE-VNL", "name": "Vanilla Bean Ice Cream",  "qty": 2,  "unit_price": 5.99,  "subtotal": 11.98},
        ],
        "subtotal": 32.16, "tax": 2.25, "total": 34.41,
        "points_earned": 32, "points_redeemed": 0, "payment": "publix_card"
    },
}

POINTS_TIERS = {
    "Green":    {"min": 0,     "max": 999,   "multiplier": 1.0, "perks": ["Birthday bonus points"]},
    "Silver":   {"min": 1000,  "max": 4999,  "multiplier": 1.25,"perks": ["Birthday bonus points","5% off floral","Free sub upgrade"]},
    "Gold":     {"min": 5000,  "max": 19999, "multiplier": 1.5, "perks": ["Birthday bonus points","10% off deli","Free sub upgrade","Double points weekends"]},
    "Platinum": {"min": 20000, "max": None,  "multiplier": 2.0, "perks": ["Birthday bonus points","15% off all purchases","Triple points weekends","Free delivery","Dedicated service line"]},
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def paginate(items, page=1, limit=20):
    page  = max(1, int(page or 1))
    limit = min(100, max(1, int(limit or 20)))
    total = len(items)
    start = (page - 1) * limit
    return {"data": items[start:start+limit], "page": page, "limit": limit,
            "total": total, "pages": math.ceil(total / limit) if total else 1}

def api_err(msg, code):
    return jsonify({"error": msg}), code

def customer_orders(cid):
    return [o for o in ORDERS.values() if o["customer_id"] == cid]

def spending_summary(orders):
    return {
        "total_orders": len(orders),
        "total_spent":  round(sum(o["total"] for o in orders), 2),
        "total_points_earned":   sum(o["points_earned"] for o in orders),
        "total_points_redeemed": sum(o["points_redeemed"] for o in orders),
        "avg_order_value": round(sum(o["total"] for o in orders) / len(orders), 2) if orders else 0,
        "favorite_category": _fav_category(orders),
    }

def _fav_category(orders):
    counts = {}
    for o in orders:
        for item in o["items"]:
            p = PRODUCTS.get(item["sku"], {})
            cat = p.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + item["qty"]
    return max(counts, key=counts.get) if counts else None

# ─── OpenAPI Spec ─────────────────────────────────────────────────────────────

SPEC = {
    "openapi": "3.1.0",
    "info": {
        "title": "Publix CRM API",
        "version": "1.0.0",
        "description": (
            "Customer Relationship Management API for Publix supermarket. "
            "Manage customer profiles, loyalty points, orders, and purchasing history. "
            "All endpoints use POST with a JSON request body."
        ),
        "contact": {"email": "crm-api@publix.com"},
    },
    "servers": [
        {"url": "https://publix-crm-api.onrender.com", "description": "Production"},
        {"url": "http://localhost:8000", "description": "Local"},
    ],
    "tags": [
        {"name": "Customers",  "description": "Customer profile management"},
        {"name": "Points",     "description": "Loyalty points and tiers"},
        {"name": "Orders",     "description": "Order records"},
        {"name": "History",    "description": "Purchasing history and analytics"},
        {"name": "Products",   "description": "Product catalog"},
    ],
    "paths": {
        "/api/customers": {
            "post": {
                "tags": ["Customers"], "summary": "List customers",
                "operationId": "listCustomers",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CustomersRequest"}, "example": {"tier": "Gold", "store_id": "store_FL01", "page": 1, "limit": 20}}}},
                "responses": {"200": {"description": "Paginated customer list"}, "400": {"description": "Invalid filter"}},
            }
        },
        "/api/customers/profile": {
            "post": {
                "tags": ["Customers"], "summary": "Get customer profile",
                "description": (
                    "Retrieve a full customer profile by customer_id OR by phone/mobile number. "
                    "Supply exactly one of customer_id or phone. "
                    "Phone lookup strips all formatting and searches both phone and mobile fields."
                ),
                "operationId": "getCustomer",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ProfileRequest"},
                            "examples": {
                                "by_id":    {"summary": "By customer ID",   "value": {"customer_id": "CUS-001"}},
                                "by_phone": {"summary": "By phone number",  "value": {"phone": "786-304-8821"}},
                                "by_mobile":{"summary": "By mobile number", "value": {"phone": "(404) 993-7741"}},
                            },
                        }
                    },
                },
                "responses": {
                    "200": {"description": "Full customer profile with orders summary and tier details"},
                    "400": {"description": "Neither customer_id nor phone was supplied"},
                    "404": {"description": "Customer not found"},
                },
            }
        },
        "/api/customers/search": {
            "post": {
                "tags": ["Customers"], "summary": "Search customers",
                "operationId": "searchCustomers",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CustomerSearchRequest"}, "example": {"q": "gonzalez"}}}},
                "responses": {"200": {"description": "Matching customers"}, "400": {"description": "Query too short"}},
            }
        },
        "/api/customers/search/phone": {
            "post": {
                "tags": ["Customers"], "summary": "Search by phone number",
                "description": (
                    "Look up a customer by phone or mobile number. "
                    "Accepts full or partial digits — formatting characters (dashes, dots, spaces, parentheses) are stripped automatically. "
                    "Searches both phone and mobile fields. Returns exact match on a full 10-digit number or partial matches for shorter queries."
                ),
                "operationId": "searchByPhone",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/PhoneSearchRequest"},
                            "example": {"phone": "786-304-8821"},
                        }
                    },
                },
                "responses": {
                    "200": {"description": "Matching customer(s) with matched_field indicating phone or mobile"},
                    "400": {"description": "phone field missing or fewer than 4 digits provided"},
                    "404": {"description": "No customer found for the given number"},
                },
            }
        },
        "/api/points/balance": {
            "post": {
                "tags": ["Points"], "summary": "Get points balance",
                "operationId": "pointsBalance",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CustomerIdRequest"}, "example": {"customer_id": "CUS-001"}}}},
                "responses": {"200": {"description": "Points balance and tier details"}, "404": {"description": "Customer not found"}},
            }
        },
        "/api/points/earn": {
            "post": {
                "tags": ["Points"], "summary": "Earn points",
                "operationId": "earnPoints",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/EarnPointsRequest"}, "example": {"customer_id": "CUS-001", "purchase_amount": 45.99, "order_id": "ORD-2026-0001"}}}},
                "responses": {"200": {"description": "Points awarded and new balance"}, "400": {"description": "Invalid request"}},
            }
        },
        "/api/points/redeem": {
            "post": {
                "tags": ["Points"], "summary": "Redeem points",
                "operationId": "redeemPoints",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RedeemPointsRequest"}, "example": {"customer_id": "CUS-001", "points": 500}}}},
                "responses": {"200": {"description": "Redemption result and new balance"}, "400": {"description": "Insufficient points"}},
            }
        },
        "/api/points/tiers": {
            "post": {
                "tags": ["Points"], "summary": "Get tier definitions",
                "operationId": "listTiers",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"type": "object"}, "example": {}}}},
                "responses": {"200": {"description": "All loyalty tier definitions"}},
            }
        },
        "/api/orders": {
            "post": {
                "tags": ["Orders"], "summary": "List orders",
                "operationId": "listOrders",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/OrdersRequest"}, "example": {"customer_id": "CUS-001", "page": 1, "limit": 10}}}},
                "responses": {"200": {"description": "Paginated order list"}},
            }
        },
        "/api/orders/detail": {
            "post": {
                "tags": ["Orders"], "summary": "Get order detail",
                "operationId": "getOrder",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/OrderIdRequest"}, "example": {"order_id": "ORD-2026-0001"}}}},
                "responses": {"200": {"description": "Full order with line items"}, "404": {"description": "Order not found"}},
            }
        },
        "/api/history/summary": {
            "post": {
                "tags": ["History"], "summary": "Purchasing summary",
                "operationId": "purchaseSummary",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CustomerIdRequest"}, "example": {"customer_id": "CUS-001"}}}},
                "responses": {"200": {"description": "Spending totals, favorite category, order stats"}, "404": {"description": "Customer not found"}},
            }
        },
        "/api/history/by-category": {
            "post": {
                "tags": ["History"], "summary": "Spend by category",
                "operationId": "spendByCategory",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CustomerIdRequest"}, "example": {"customer_id": "CUS-002"}}}},
                "responses": {"200": {"description": "Spending breakdown by product category"}},
            }
        },
        "/api/history/top-products": {
            "post": {
                "tags": ["History"], "summary": "Most purchased products",
                "operationId": "topProducts",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/TopProductsRequest"}, "example": {"customer_id": "CUS-001", "limit": 5}}}},
                "responses": {"200": {"description": "Top products by quantity purchased"}},
            }
        },
        "/api/products": {
            "post": {
                "tags": ["Products"], "summary": "List products with points info",
                "operationId": "listProducts",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ProductsRequest"}, "example": {"category": "meat"}}}},
                "responses": {"200": {"description": "Products with category and points-per-dollar"}},
            }
        },
    },
    "components": {
        "schemas": {
            "CustomerIdRequest": {"type": "object", "required": ["customer_id"], "properties": {"customer_id": {"type": "string", "example": "CUS-001"}}},
            "ProfileRequest": {
                "type": "object",
                "description": "Supply exactly one of customer_id or phone.",
                "properties": {
                    "customer_id": {"type": "string", "example": "CUS-001",      "description": "Unique customer ID"},
                    "phone":       {"type": "string", "example": "786-304-8821", "description": "Phone or mobile number — any format, min 4 digits"},
                },
            },
            "OrderIdRequest":    {"type": "object", "required": ["order_id"],    "properties": {"order_id":    {"type": "string", "example": "ORD-2026-0001"}}},
            "CustomersRequest": {
                "type": "object",
                "properties": {
                    "tier":     {"type": "string", "enum": ["Green","Silver","Gold","Platinum"]},
                    "store_id": {"type": "string", "example": "store_FL01"},
                    "active":   {"type": "boolean"},
                    "page":     {"type": "integer", "default": 1},
                    "limit":    {"type": "integer", "default": 20, "maximum": 100},
                },
            },
            "CustomerSearchRequest": {
                "type": "object", "required": ["q"],
                "properties": {
                    "q":     {"type": "string", "minLength": 2, "description": "Search name or email"},
                    "tier":  {"type": "string", "enum": ["Green","Silver","Gold","Platinum"]},
                    "page":  {"type": "integer", "default": 1},
                    "limit": {"type": "integer", "default": 20},
                },
            },
            "PhoneSearchRequest": {
                "type": "object", "required": ["phone"],
                "properties": {
                    "phone": {
                        "type": "string",
                        "description": "Phone or mobile number to search. Formatting characters are stripped automatically. Min 4 digits required.",
                        "example": "786-304-8821",
                    },
                    "exact": {
                        "type": "boolean",
                        "default": False,
                        "description": "If true, only return customers whose digits match exactly (full 10-digit match). Default is partial match.",
                    },
                },
            },
            "EarnPointsRequest": {
                "type": "object", "required": ["customer_id", "purchase_amount"],
                "properties": {
                    "customer_id":     {"type": "string"},
                    "purchase_amount": {"type": "number", "example": 45.99},
                    "order_id":        {"type": "string"},
                    "category_bonus":  {"type": "string", "description": "Category for bonus points calculation"},
                },
            },
            "RedeemPointsRequest": {
                "type": "object", "required": ["customer_id", "points"],
                "properties": {
                    "customer_id": {"type": "string"},
                    "points":      {"type": "integer", "minimum": 100, "description": "Minimum 100 points per redemption"},
                },
            },
            "OrdersRequest": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string"},
                    "store_id":    {"type": "string"},
                    "status":      {"type": "string", "enum": ["completed","pending","cancelled"]},
                    "page":        {"type": "integer", "default": 1},
                    "limit":       {"type": "integer", "default": 20},
                },
            },
            "TopProductsRequest": {
                "type": "object", "required": ["customer_id"],
                "properties": {
                    "customer_id": {"type": "string"},
                    "limit":       {"type": "integer", "default": 5, "maximum": 20},
                },
            },
            "ProductsRequest": {
                "type": "object",
                "properties": {
                    "category":       {"type": "string"},
                    "min_points_ppd": {"type": "integer", "description": "Minimum points per dollar"},
                },
            },
        }
    },
}

# ─── Swagger UI ───────────────────────────────────────────────────────────────

SWAGGER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Publix CRM API</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"/>
  <style>body{margin:0;background:#f8f8f6}.topbar{display:none!important}</style>
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
<script>
SwaggerUIBundle({url:"/api/openapi.json",dom_id:"#swagger-ui",
  presets:[SwaggerUIBundle.presets.apis,SwaggerUIBundle.SwaggerUIStandalonePreset],
  layout:"BaseLayout",deepLinking:true,tryItOutEnabled:true,filter:true});
</script>
</body>
</html>"""

@app.route("/docs")
def swagger_ui():
    return SWAGGER_HTML

@app.route("/api/openapi.json")
def openapi_spec():
    return jsonify(SPEC)

# ─── Routes: Customers ────────────────────────────────────────────────────────

@app.route("/api/customers", methods=["POST"])
def list_customers():
    body     = request.json or {}
    tier     = body.get("tier")
    store_id = body.get("store_id")
    active   = body.get("active")
    page     = body.get("page", 1)
    limit    = body.get("limit", 20)

    items = list(CUSTOMERS.values())
    if tier:     items = [c for c in items if c["tier"] == tier]
    if store_id: items = [c for c in items if c["store_id"] == store_id]
    if active is not None: items = [c for c in items if c["active"] == active]

    # strip address for list view
    safe = [{k: v for k, v in c.items() if k != "address"} for c in items]
    return jsonify(paginate(safe, page, limit))


@app.route("/api/customers/profile", methods=["POST"])
def get_customer():
    body  = request.json or {}
    cid   = body.get("customer_id")
    phone = str(body.get("phone", "")).strip()

    # must supply at least one lookup key
    if not cid and not phone:
        return api_err("Supply either 'customer_id' or 'phone' to look up a profile.", 400)

    c = None
    lookup_method = None

    if cid:
        # primary lookup by customer ID
        c = CUSTOMERS.get(cid)
        lookup_method = "customer_id"
        if not c:
            return api_err(f"Customer '{cid}' not found.", 404)
    else:
        # phone lookup — strip non-digits, search both phone and mobile
        digits = "".join(ch for ch in phone if ch.isdigit())
        if len(digits) < 4:
            return api_err("'phone' must contain at least 4 digits.", 400)
        for customer in CUSTOMERS.values():
            phone_d  = "".join(ch for ch in customer.get("phone",  "") if ch.isdigit())
            mobile_d = "".join(ch for ch in customer.get("mobile", "") if ch.isdigit())
            if digits in phone_d or digits in mobile_d:
                c = customer
                lookup_method = "phone" if digits in phone_d else "mobile"
                break
        if not c:
            return api_err(f"No customer found with phone number matching '{phone}'.", 404)

    orders = customer_orders(c["id"])
    result = dict(c)
    result["order_count"]  = len(orders)
    result["total_spent"]  = round(sum(o["total"] for o in orders), 2)
    result["tier_details"] = POINTS_TIERS.get(c["tier"], {})
    result["lookup_method"] = lookup_method
    return jsonify(result)


@app.route("/api/customers/search", methods=["POST"])
def search_customers():
    body  = request.json or {}
    q     = str(body.get("q", "")).strip().lower()
    tier  = body.get("tier")
    page  = body.get("page", 1)
    limit = body.get("limit", 20)

    if len(q) < 2: return api_err("Query 'q' must be at least 2 characters.", 400)

    results = []
    for c in CUSTOMERS.values():
        full_name = f"{c['first_name']} {c['last_name']}".lower()
        if q in full_name or q in c["email"].lower() or q in c["id"].lower():
            if tier and c["tier"] != tier: continue
            results.append({k: v for k, v in c.items() if k != "address"})

    p = paginate(results, page, limit)
    p["query"] = q
    return jsonify(p)

@app.route("/api/customers/search/phone", methods=["POST"])
def search_by_phone():
    body  = request.json or {}
    raw   = str(body.get("phone", "")).strip()
    exact = body.get("exact", False)

    if not raw:
        return api_err("'phone' field is required.", 400)

    # strip all non-digit characters for comparison
    digits = "".join(ch for ch in raw if ch.isdigit())

    if len(digits) < 4:
        return api_err("At least 4 digits are required to search by phone.", 400)

    matches = []
    for c in CUSTOMERS.values():
        phone_digits  = "".join(ch for ch in c.get("phone",  "") if ch.isdigit())
        mobile_digits = "".join(ch for ch in c.get("mobile", "") if ch.isdigit())

        if exact:
            hit_phone  = digits == phone_digits
            hit_mobile = digits == mobile_digits
        else:
            hit_phone  = digits in phone_digits
            hit_mobile = digits in mobile_digits

        if hit_phone or hit_mobile:
            result = {k: v for k, v in c.items()}
            result["matched_field"] = "phone" if hit_phone else "mobile"
            result["matched_number"] = c["phone"] if hit_phone else c["mobile"]
            matches.append(result)

    if not matches:
        return api_err(f"No customer found with phone number matching '{raw}'.", 404)

    return jsonify({
        "results":      matches,
        "count":        len(matches),
        "query_digits": digits,
        "exact_match":  exact,
    })


# ─── Routes: Points ───────────────────────────────────────────────────────────

@app.route("/api/points/balance", methods=["POST"])
def points_balance():
    body = request.json or {}
    cid  = body.get("customer_id")
    if not cid: return api_err("customer_id is required.", 400)
    c = CUSTOMERS.get(cid)
    if not c:   return api_err(f"Customer '{cid}' not found.", 404)

    tier_info  = POINTS_TIERS.get(c["tier"], {})
    next_tier  = {"Green": "Silver", "Silver": "Gold", "Gold": "Platinum"}.get(c["tier"])
    next_min   = POINTS_TIERS.get(next_tier, {}).get("min") if next_tier else None
    pts_to_next= (next_min - c["lifetime_points"]) if next_min else None
    birthday   = c.get("birthday", "")
    birth_month= int(birthday.split("-")[1]) if birthday else None

    return jsonify({
        "customer_id":       cid,
        "name":              f"{c['first_name']} {c['last_name']}",
        "birthday":          birthday,
        "birth_month":       birth_month,
        "points_balance":    c["points_balance"],
        "lifetime_points":   c["lifetime_points"],
        "tier":              c["tier"],
        "tier_multiplier":   tier_info.get("multiplier"),
        "tier_perks":        tier_info.get("perks", []),
        "next_tier":         next_tier,
        "points_to_next_tier": pts_to_next,
        "redemption_value":  round(c["points_balance"] * 0.01, 2),  # 1 pt = $0.01
    })


@app.route("/api/points/earn", methods=["POST"])
def earn_points():
    body   = request.json or {}
    cid    = body.get("customer_id")
    amount = body.get("purchase_amount")
    if not cid:    return api_err("customer_id is required.", 400)
    if not amount: return api_err("purchase_amount is required.", 400)
    c = CUSTOMERS.get(cid)
    if not c:      return api_err(f"Customer '{cid}' not found.", 404)

    tier_mult  = POINTS_TIERS.get(c["tier"], {}).get("multiplier", 1.0)
    base_pts   = int(amount * 1)         # 1 pt per $1
    earned     = int(base_pts * tier_mult)
    prev_bal   = c["points_balance"]

    # update (in-memory)
    CUSTOMERS[cid]["points_balance"]  += earned
    CUSTOMERS[cid]["lifetime_points"] += earned

    return jsonify({
        "customer_id":     cid,
        "purchase_amount": amount,
        "base_points":     base_pts,
        "tier_multiplier": tier_mult,
        "points_earned":   earned,
        "previous_balance":prev_bal,
        "new_balance":     CUSTOMERS[cid]["points_balance"],
        "order_id":        body.get("order_id"),
    })


@app.route("/api/points/redeem", methods=["POST"])
def redeem_points():
    body   = request.json or {}
    cid    = body.get("customer_id")
    pts    = body.get("points", 0)
    if not cid: return api_err("customer_id is required.", 400)
    if pts < 100: return api_err("Minimum redemption is 100 points.", 400)
    c = CUSTOMERS.get(cid)
    if not c:   return api_err(f"Customer '{cid}' not found.", 404)
    if c["points_balance"] < pts:
        return api_err(f"Insufficient points. Balance: {c['points_balance']}, requested: {pts}.", 400)

    dollar_value = round(pts * 0.01, 2)
    CUSTOMERS[cid]["points_balance"] -= pts

    return jsonify({
        "customer_id":    cid,
        "points_redeemed":pts,
        "dollar_value":   dollar_value,
        "previous_balance": c["points_balance"] + pts,
        "new_balance":    CUSTOMERS[cid]["points_balance"],
    })


@app.route("/api/points/tiers", methods=["POST"])
def list_tiers():
    result = []
    for name, info in POINTS_TIERS.items():
        result.append({"tier": name, **info})
    return jsonify(result)

# ─── Routes: Orders ───────────────────────────────────────────────────────────

@app.route("/api/orders", methods=["POST"])
def list_orders():
    body     = request.json or {}
    cid      = body.get("customer_id")
    store_id = body.get("store_id")
    status   = body.get("status")
    page     = body.get("page", 1)
    limit    = body.get("limit", 20)

    items = list(ORDERS.values())
    if cid:      items = [o for o in items if o["customer_id"] == cid]
    if store_id: items = [o for o in items if o["store_id"] == store_id]
    if status:   items = [o for o in items if o["status"] == status]
    items.sort(key=lambda x: x["date"], reverse=True)
    return jsonify(paginate(items, page, limit))


@app.route("/api/orders/detail", methods=["POST"])
def get_order():
    body = request.json or {}
    oid  = body.get("order_id")
    if not oid: return api_err("order_id is required.", 400)
    o = ORDERS.get(oid)
    if not o:   return api_err(f"Order '{oid}' not found.", 404)
    c = CUSTOMERS.get(o["customer_id"], {})
    result = dict(o)
    result["customer_name"] = f"{c.get('first_name','')} {c.get('last_name','')}".strip()
    result["customer_tier"] = c.get("tier")
    return jsonify(result)

# ─── Routes: History ─────────────────────────────────────────────────────────

@app.route("/api/history/summary", methods=["POST"])
def purchase_summary():
    body = request.json or {}
    cid  = body.get("customer_id")
    if not cid: return api_err("customer_id is required.", 400)
    c = CUSTOMERS.get(cid)
    if not c:   return api_err(f"Customer '{cid}' not found.", 404)

    orders = customer_orders(cid)
    summary = spending_summary(orders)
    summary["customer_id"]   = cid
    summary["customer_name"] = f"{c['first_name']} {c['last_name']}"
    summary["tier"]          = c["tier"]
    summary["points_balance"]= c["points_balance"]
    summary["member_since"]  = c["joined"]
    return jsonify(summary)


@app.route("/api/history/by-category", methods=["POST"])
def spend_by_category():
    body = request.json or {}
    cid  = body.get("customer_id")
    if not cid: return api_err("customer_id is required.", 400)
    c = CUSTOMERS.get(cid)
    if not c:   return api_err(f"Customer '{cid}' not found.", 404)

    orders = customer_orders(cid)
    cat_spend = {}
    cat_qty   = {}
    for o in orders:
        for item in o["items"]:
            p   = PRODUCTS.get(item["sku"], {})
            cat = p.get("category", "unknown")
            cat_spend[cat] = round(cat_spend.get(cat, 0) + item["subtotal"], 2)
            cat_qty[cat]   = cat_qty.get(cat, 0) + item["qty"]

    breakdown = [
        {"category": cat, "total_spent": cat_spend[cat], "items_purchased": cat_qty[cat]}
        for cat in sorted(cat_spend, key=cat_spend.get, reverse=True)
    ]
    return jsonify({
        "customer_id": cid,
        "customer_name": f"{c['first_name']} {c['last_name']}",
        "breakdown": breakdown,
        "total_spent": round(sum(o["total"] for o in orders), 2),
    })


@app.route("/api/history/top-products", methods=["POST"])
def top_products():
    body  = request.json or {}
    cid   = body.get("customer_id")
    limit = min(20, int(body.get("limit", 5)))
    if not cid: return api_err("customer_id is required.", 400)
    c = CUSTOMERS.get(cid)
    if not c:   return api_err(f"Customer '{cid}' not found.", 404)

    orders  = customer_orders(cid)
    skus    = {}
    for o in orders:
        for item in o["items"]:
            skus[item["sku"]] = skus.get(item["sku"], {"qty": 0, "spent": 0.0, "name": item["name"]})
            skus[item["sku"]]["qty"]   += item["qty"]
            skus[item["sku"]]["spent"] += item["subtotal"]

    ranked = sorted(skus.items(), key=lambda x: x[1]["qty"], reverse=True)[:limit]
    results = [{"sku": sku, "name": info["name"], "total_qty": info["qty"],
                "total_spent": round(info["spent"], 2),
                "category": PRODUCTS.get(sku, {}).get("category")} for sku, info in ranked]

    return jsonify({"customer_id": cid, "top_products": results})

# ─── Routes: Products ─────────────────────────────────────────────────────────

@app.route("/api/products", methods=["POST"])
def list_products():
    body    = request.json or {}
    category = body.get("category")
    min_ppd  = body.get("min_points_ppd")

    items = [{"sku": k, **v} for k, v in PRODUCTS.items()]
    if category: items = [p for p in items if p["category"] == category]
    if min_ppd:  items = [p for p in items if p["points_per_dollar"] >= int(min_ppd)]
    items.sort(key=lambda x: x["category"])
    return jsonify({"data": items, "total": len(items)})

# ─── Health & root ────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": "1.0.0", "service": "publix-crm-api",
                    "customers": len(CUSTOMERS), "orders": len(ORDERS)})

@app.route("/")
def root():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
