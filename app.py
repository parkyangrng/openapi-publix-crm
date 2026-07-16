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
        "phone": "(786) 304-8821",
        "mobile": "(786) 512-3394",
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
    # Additional products used in historical orders
    "PRD-SPN-BYB": {"name": "Organic Baby Spinach 5oz",     "category": "produce",   "price": 3.99,  "points_per_dollar": 2},
    "PRD-BRO-CRW": {"name": "Broccoli Crown",               "category": "produce",   "price": 2.49,  "points_per_dollar": 2},
    "PRD-TOM-ROM": {"name": "Roma Tomatoes",                 "category": "produce",   "price": 1.29,  "points_per_dollar": 2},
    "PRD-KAL-ORG": {"name": "Organic Kale Bunch",           "category": "produce",   "price": 2.99,  "points_per_dollar": 2},
    "DRY-MLK-ALM": {"name": "Almond Milk Unsweetened",      "category": "dairy",     "price": 4.29,  "points_per_dollar": 1},
    "DRY-YGT-GRK": {"name": "Greek Yogurt Plain 17.6oz",   "category": "dairy",     "price": 2.79,  "points_per_dollar": 1},
    "DRY-BTR-UNS": {"name": "Unsalted Butter 4 sticks",     "category": "dairy",     "price": 5.99,  "points_per_dollar": 1},
    "BKR-BRD-WHT": {"name": "Whole Wheat Bread",            "category": "bakery",    "price": 3.49,  "points_per_dollar": 2},
    "BKR-MFN-BLB": {"name": "Blueberry Muffin Jumbo",      "category": "bakery",    "price": 2.79,  "points_per_dollar": 2},
    "BKR-SUB-ITA": {"name": "Italian Sub Roll 6-pack",      "category": "bakery",    "price": 3.99,  "points_per_dollar": 2},
    "BEV-WTR-SPK": {"name": "Sparkling Water 12pk",         "category": "beverages", "price": 7.49,  "points_per_dollar": 1},
    "BEV-TEA-GRN": {"name": "Green Tea 20-bag box",         "category": "beverages", "price": 3.99,  "points_per_dollar": 1},
    "BEV-JUC-APL": {"name": "Apple Juice 64oz",             "category": "beverages", "price": 4.49,  "points_per_dollar": 1},
    "MET-SHR-LRG": {"name": "Large Shrimp 1lb Raw",         "category": "meat",      "price": 11.99, "points_per_dollar": 3},
    "PNT-RCE-JSM": {"name": "Jasmine Rice 5lb",             "category": "pantry",    "price": 6.99,  "points_per_dollar": 1},
    "PNT-CAN-TOM": {"name": "Diced Tomatoes 14.5oz",        "category": "pantry",    "price": 1.09,  "points_per_dollar": 1},
    "PNT-PNB-CRK": {"name": "Creamy Peanut Butter 16oz",   "category": "pantry",    "price": 4.29,  "points_per_dollar": 1},
    "DLI-HAM-HNY": {"name": "Honey Glazed Ham",             "category": "deli",      "price": 8.99,  "points_per_dollar": 2},
    "PHR-ADV-200": {"name": "Ibuprofen 200mg 100ct",        "category": "pharmacy",  "price": 7.49,  "points_per_dollar": 1},
    "FLR-MIX-SEA": {"name": "Seasonal Mix Bouquet",         "category": "floral",    "price": 12.99, "points_per_dollar": 3},
    "FRZ-VEG-MIX": {"name": "Mixed Vegetables 12oz",        "category": "frozen",    "price": 2.79,  "points_per_dollar": 1},
    "FRZ-EDM-SHL": {"name": "Edamame Shelled 12oz",         "category": "frozen",    "price": 3.99,  "points_per_dollar": 1},
}

ORDERS = {

    # ── CUS-001 Maria Gonzalez (Gold · Brickell) — 3 orders ─────────────────────
    "ORD-2026-0001": {
        "id": "ORD-2026-0001", "customer_id": "CUS-001", "store_id": "store_FL01",
        "date": "2026-07-14", "status": "completed",
        "note": "Weekly grocery run — breakfast and dinner staples",
        "items": [
            {"sku": "DRY-EGG-LRG", "name": "Large Eggs Dozen",        "qty": 2,  "unit_price": 6.29,  "subtotal": 12.58,  "note": "2 dozen eggs"},
            {"sku": "DRY-OAT-PLN", "name": "Horizon Oat Milk 32oz",   "qty": 1,  "unit_price": 5.49,  "subtotal": 5.49,   "note": "1 litre oat milk"},
            {"sku": "BKR-BRD-SRD", "name": "Sourdough Loaf",          "qty": 1,  "unit_price": 4.99,  "subtotal": 4.99,   "note": "1 sourdough loaf"},
            {"sku": "MET-SAL-ATL", "name": "Atlantic Salmon Fillet",   "qty": 1,  "unit_price": 13.99, "subtotal": 13.99,  "note": "1 lb salmon fillet"},
            {"sku": "PRD-BAN-ORG", "name": "Organic Bananas",          "qty": 1,  "unit_price": 0.69,  "subtotal": 0.69,   "note": "1 bunch organic bananas"},
        ],
        "subtotal": 37.74, "tax": 2.64, "total": 40.38,
        "points_earned": 81, "points_redeemed": 0, "payment": "credit_card"
    },
    "ORD-2026-0002": {
        "id": "ORD-2026-0002", "customer_id": "CUS-001", "store_id": "store_FL01",
        "date": "2026-07-06", "status": "completed",
        "note": "Sunday brunch pickup",
        "items": [
            {"sku": "BKR-CRW-BUT", "name": "Butter Croissant",         "qty": 3,  "unit_price": 2.29,  "subtotal": 6.87,   "note": "3 butter croissants"},
            {"sku": "PRD-STR-ORG", "name": "Organic Strawberries 1lb", "qty": 2,  "unit_price": 5.49,  "subtotal": 10.98,  "note": "2 pints organic strawberries"},
            {"sku": "DRY-MLK-WHL", "name": "Whole Milk Gallon",        "qty": 1,  "unit_price": 4.59,  "subtotal": 4.59,   "note": "1 gallon whole milk"},
            {"sku": "BEV-OJ-NAT",  "name": "Orange Juice 52oz",        "qty": 1,  "unit_price": 5.79,  "subtotal": 5.79,   "note": "1 bottle orange juice"},
        ],
        "subtotal": 28.23, "tax": 1.98, "total": 30.21,
        "points_earned": 57, "points_redeemed": 500, "payment": "publix_card"
    },
    "ORD-2026-0003": {
        "id": "ORD-2026-0003", "customer_id": "CUS-001", "store_id": "store_FL01",
        "date": "2026-06-22", "status": "completed",
        "note": "Weekend dinner party prep",
        "items": [
            {"sku": "MET-STK-RIB", "name": "Ribeye Steak",             "qty": 2,  "unit_price": 16.99, "subtotal": 33.98,  "note": "2 ribeye steaks"},
            {"sku": "PRD-AVC-HAS", "name": "Hass Avocado",             "qty": 4,  "unit_price": 1.49,  "subtotal": 5.96,   "note": "4 ripe avocados"},
            {"sku": "PNT-OLV-OIL", "name": "Extra Virgin Olive Oil",   "qty": 1,  "unit_price": 8.99,  "subtotal": 8.99,   "note": "1 bottle EVOO"},
            {"sku": "DRY-CHZ-CHD", "name": "Sharp Cheddar Block 16oz", "qty": 1,  "unit_price": 6.99,  "subtotal": 6.99,   "note": "1 block sharp cheddar"},
            {"sku": "FLR-RSE-DZN", "name": "Red Rose Bouquet Dozen",   "qty": 1,  "unit_price": 19.99, "subtotal": 19.99,  "note": "1 dozen red roses for table"},
        ],
        "subtotal": 75.91, "tax": 5.31, "total": 81.22,
        "points_earned": 183, "points_redeemed": 0, "payment": "credit_card"
    },

    # ── CUS-002 James Whitfield (Platinum · Buckhead) — 3 orders ────────────────
    "ORD-2026-0004": {
        "id": "ORD-2026-0004", "customer_id": "CUS-002", "store_id": "store_GA01",
        "date": "2026-07-13", "status": "completed",
        "note": "Weeknight deli and pantry restock",
        "items": [
            {"sku": "DLI-TKY-RST", "name": "Oven Roasted Turkey Breast","qty": 1, "unit_price": 10.99, "subtotal": 10.99,  "note": "1 lb roasted turkey, sliced"},
            {"sku": "DLI-SUB-ITA", "name": "Italian Sub 12-inch",       "qty": 2,  "unit_price": 9.99,  "subtotal": 19.98,  "note": "2 Italian subs for lunch"},
            {"sku": "BEV-COF-GRD", "name": "Ground Coffee Medium 12oz", "qty": 2,  "unit_price": 8.99,  "subtotal": 17.98,  "note": "2 bags ground coffee"},
            {"sku": "PNT-RCE-JSM", "name": "Jasmine Rice 5lb",          "qty": 1,  "unit_price": 6.99,  "subtotal": 6.99,   "note": "1 bag jasmine rice"},
        ],
        "subtotal": 55.94, "tax": 3.92, "total": 59.86,
        "points_earned": 240, "points_redeemed": 0, "payment": "credit_card"
    },
    "ORD-2026-0005": {
        "id": "ORD-2026-0005", "customer_id": "CUS-002", "store_id": "store_GA01",
        "date": "2026-07-05", "status": "completed",
        "note": "4th of July BBQ haul",
        "items": [
            {"sku": "MET-GBF-8020","name": "Ground Beef 80/20 1lb",     "qty": 4,  "unit_price": 6.99,  "subtotal": 27.96,  "note": "4 lbs ground beef for burgers"},
            {"sku": "MET-CHK-BRS", "name": "Chicken Breast Boneless",   "qty": 3,  "unit_price": 5.99,  "subtotal": 17.97,  "note": "3 lbs boneless chicken"},
            {"sku": "BEV-OJ-NAT",  "name": "Orange Juice 52oz",         "qty": 2,  "unit_price": 5.79,  "subtotal": 11.58,  "note": "2 bottles OJ for mimosas"},
            {"sku": "PNT-CAN-TOM", "name": "Diced Tomatoes 14.5oz",     "qty": 3,  "unit_price": 1.09,  "subtotal": 3.27,   "note": "3 cans diced tomatoes"},
            {"sku": "FRZ-ICE-VNL", "name": "Vanilla Bean Ice Cream",    "qty": 2,  "unit_price": 5.99,  "subtotal": 11.98,  "note": "2 tubs vanilla ice cream"},
        ],
        "subtotal": 72.76, "tax": 5.09, "total": 77.85,
        "points_earned": 312, "points_redeemed": 1000, "payment": "publix_card"
    },
    "ORD-2026-0006": {
        "id": "ORD-2026-0006", "customer_id": "CUS-002", "store_id": "store_GA01",
        "date": "2026-06-28", "status": "completed",
        "note": "Premium seafood and flowers for anniversary dinner",
        "items": [
            {"sku": "MET-SAL-ATL", "name": "Atlantic Salmon Fillet",    "qty": 2,  "unit_price": 13.99, "subtotal": 27.98,  "note": "2 lbs fresh salmon fillet"},
            {"sku": "MET-SHR-LRG", "name": "Large Shrimp 1lb Raw",      "qty": 1,  "unit_price": 11.99, "subtotal": 11.99,  "note": "1 lb raw large shrimp"},
            {"sku": "PNT-PST-SPN", "name": "Spaghetti 16oz",            "qty": 2,  "unit_price": 1.89,  "subtotal": 3.78,   "note": "2 boxes spaghetti"},
            {"sku": "FLR-RSE-DZN", "name": "Red Rose Bouquet Dozen",    "qty": 1,  "unit_price": 19.99, "subtotal": 19.99,  "note": "1 dozen red roses"},
            {"sku": "BEV-COF-GRD", "name": "Ground Coffee Medium 12oz", "qty": 1,  "unit_price": 8.99,  "subtotal": 8.99,   "note": "1 bag specialty coffee"},
        ],
        "subtotal": 72.73, "tax": 5.09, "total": 77.82,
        "points_earned": 312, "points_redeemed": 0, "payment": "credit_card"
    },

    # ── CUS-003 Priya Nair (Silver · Coral Gables) — 3 orders ───────────────────
    "ORD-2026-0007": {
        "id": "ORD-2026-0007", "customer_id": "CUS-003", "store_id": "store_FL02",
        "date": "2026-07-12", "status": "completed",
        "note": "Plant-based weekly shop",
        "items": [
            {"sku": "DRY-OAT-PLN", "name": "Horizon Oat Milk 32oz",    "qty": 2,  "unit_price": 5.49,  "subtotal": 10.98,  "note": "2 cartons oat milk"},
            {"sku": "PRD-AVC-HAS", "name": "Hass Avocado",             "qty": 4,  "unit_price": 1.49,  "subtotal": 5.96,   "note": "4 ripe avocados"},
            {"sku": "PRD-SPN-BYB", "name": "Organic Baby Spinach 5oz", "qty": 2,  "unit_price": 3.99,  "subtotal": 7.98,   "note": "2 bags baby spinach"},
            {"sku": "PNT-PST-SPN", "name": "Spaghetti 16oz",           "qty": 3,  "unit_price": 1.89,  "subtotal": 5.67,   "note": "3 boxes spaghetti"},
        ],
        "subtotal": 30.59, "tax": 2.14, "total": 32.73,
        "points_earned": 41, "points_redeemed": 0, "payment": "debit_card"
    },
    "ORD-2026-0008": {
        "id": "ORD-2026-0008", "customer_id": "CUS-003", "store_id": "store_FL02",
        "date": "2026-07-01", "status": "completed",
        "note": "Farmers market-style produce run",
        "items": [
            {"sku": "PRD-STR-ORG", "name": "Organic Strawberries 1lb", "qty": 2,  "unit_price": 5.49,  "subtotal": 10.98,  "note": "2 pints organic strawberries"},
            {"sku": "PRD-BRO-CRW", "name": "Broccoli Crown",           "qty": 2,  "unit_price": 2.49,  "subtotal": 4.98,   "note": "2 broccoli crowns"},
            {"sku": "PRD-TOM-ROM", "name": "Roma Tomatoes",             "qty": 1,  "unit_price": 1.29,  "subtotal": 1.29,   "note": "1 lb Roma tomatoes"},
            {"sku": "DRY-YGT-GRK", "name": "Greek Yogurt Plain 17.6oz","qty": 2,  "unit_price": 2.79,  "subtotal": 5.58,   "note": "2 tubs plain Greek yogurt"},
            {"sku": "BEV-TEA-GRN", "name": "Green Tea 20-bag box",     "qty": 1,  "unit_price": 3.99,  "subtotal": 3.99,   "note": "1 box green tea bags"},
        ],
        "subtotal": 26.82, "tax": 1.88, "total": 28.70,
        "points_earned": 36, "points_redeemed": 0, "payment": "credit_card"
    },
    "ORD-2026-0009": {
        "id": "ORD-2026-0009", "customer_id": "CUS-003", "store_id": "store_FL02",
        "date": "2026-06-18", "status": "completed",
        "note": "Quick pantry top-up and dairy-free essentials",
        "items": [
            {"sku": "DRY-MLK-ALM", "name": "Almond Milk Unsweetened",  "qty": 2,  "unit_price": 4.29,  "subtotal": 8.58,   "note": "2 cartons unsweetened almond milk"},
            {"sku": "PNT-OLV-OIL", "name": "Extra Virgin Olive Oil",   "qty": 1,  "unit_price": 8.99,  "subtotal": 8.99,   "note": "1 bottle olive oil"},
            {"sku": "PNT-PNB-CRK", "name": "Creamy Peanut Butter 16oz","qty": 1,  "unit_price": 4.29,  "subtotal": 4.29,   "note": "1 jar creamy peanut butter"},
            {"sku": "PRD-KAL-ORG", "name": "Organic Kale Bunch",       "qty": 2,  "unit_price": 2.99,  "subtotal": 5.98,   "note": "2 bunches organic kale"},
        ],
        "subtotal": 27.84, "tax": 1.95, "total": 29.79,
        "points_earned": 35, "points_redeemed": 250, "payment": "debit_card"
    },

    # ── CUS-004 Derek Fontaine (Green · Wynwood) — 2 orders ─────────────────────
    "ORD-2026-0010": {
        "id": "ORD-2026-0010", "customer_id": "CUS-004", "store_id": "store_FL03",
        "date": "2026-07-11", "status": "completed",
        "note": "Morning bakery and coffee run",
        "items": [
            {"sku": "BKR-MFN-BLB", "name": "Blueberry Muffin Jumbo",   "qty": 3,  "unit_price": 2.79,  "subtotal": 8.37,   "note": "3 jumbo blueberry donuts / muffins"},
            {"sku": "BKR-BRD-SRD", "name": "Sourdough Loaf",           "qty": 1,  "unit_price": 4.99,  "subtotal": 4.99,   "note": "1 sourdough loaf"},
            {"sku": "BEV-COF-GRD", "name": "Ground Coffee Medium 12oz", "qty": 1,  "unit_price": 8.99,  "subtotal": 8.99,   "note": "1 bag medium roast ground coffee"},
            {"sku": "BEV-OJ-NAT",  "name": "Orange Juice 52oz",         "qty": 1,  "unit_price": 5.79,  "subtotal": 5.79,   "note": "1 large OJ"},
        ],
        "subtotal": 28.14, "tax": 1.97, "total": 30.11,
        "points_earned": 30, "points_redeemed": 0, "payment": "cash"
    },
    "ORD-2026-0011": {
        "id": "ORD-2026-0011", "customer_id": "CUS-004", "store_id": "store_FL03",
        "date": "2026-06-29", "status": "completed",
        "note": "Weekend treat and beverage stock-up",
        "items": [
            {"sku": "BKR-CRW-BUT", "name": "Butter Croissant",          "qty": 4,  "unit_price": 2.29,  "subtotal": 9.16,   "note": "4 fresh butter croissants"},
            {"sku": "FRZ-ICE-VNL", "name": "Vanilla Bean Ice Cream",    "qty": 1,  "unit_price": 5.99,  "subtotal": 5.99,   "note": "1 tub vanilla ice cream"},
            {"sku": "BEV-WTR-SPK", "name": "Sparkling Water 12pk",      "qty": 1,  "unit_price": 7.49,  "subtotal": 7.49,   "note": "1 case sparkling water"},
            {"sku": "BEV-JUC-APL", "name": "Apple Juice 64oz",          "qty": 2,  "unit_price": 4.49,  "subtotal": 8.98,   "note": "2 bottles apple juice"},
        ],
        "subtotal": 31.62, "tax": 2.21, "total": 33.83,
        "points_earned": 34, "points_redeemed": 0, "payment": "debit_card"
    },

    # ── CUS-005 Angela Torres (Gold · Midtown Atlanta) — 3 orders ───────────────
    "ORD-2026-0012": {
        "id": "ORD-2026-0012", "customer_id": "CUS-005", "store_id": "store_GA02",
        "date": "2026-07-14", "status": "completed",
        "note": "Weekly protein and pantry restock",
        "items": [
            {"sku": "MET-CHK-BRS", "name": "Chicken Breast Boneless",   "qty": 4,  "unit_price": 5.99,  "subtotal": 23.96,  "note": "4 lbs boneless chicken breast"},
            {"sku": "MET-GBF-8020","name": "Ground Beef 80/20 1lb",     "qty": 3,  "unit_price": 6.99,  "subtotal": 20.97,  "note": "3 lbs ground beef"},
            {"sku": "PNT-OLV-OIL", "name": "Extra Virgin Olive Oil",    "qty": 1,  "unit_price": 8.99,  "subtotal": 8.99,   "note": "1 bottle EVOO"},
            {"sku": "PNT-PST-SPN", "name": "Spaghetti 16oz",            "qty": 4,  "unit_price": 1.89,  "subtotal": 7.56,   "note": "4 boxes spaghetti"},
            {"sku": "PHR-VIT-C",   "name": "Vitamin C 1000mg 100ct",    "qty": 1,  "unit_price": 9.99,  "subtotal": 9.99,   "note": "1 bottle Vitamin C supplements"},
        ],
        "subtotal": 71.47, "tax": 5.00, "total": 76.47,
        "points_earned": 172, "points_redeemed": 0, "payment": "credit_card"
    },
    "ORD-2026-0013": {
        "id": "ORD-2026-0013", "customer_id": "CUS-005", "store_id": "store_GA02",
        "date": "2026-07-03", "status": "completed",
        "note": "Holiday weekend grill prep",
        "items": [
            {"sku": "MET-STK-RIB", "name": "Ribeye Steak",              "qty": 2,  "unit_price": 16.99, "subtotal": 33.98,  "note": "2 thick-cut ribeyes"},
            {"sku": "MET-SHR-LRG", "name": "Large Shrimp 1lb Raw",      "qty": 2,  "unit_price": 11.99, "subtotal": 23.98,  "note": "2 lbs raw shrimp for skewers"},
            {"sku": "PNT-RCE-JSM", "name": "Jasmine Rice 5lb",          "qty": 1,  "unit_price": 6.99,  "subtotal": 6.99,   "note": "1 bag jasmine rice"},
            {"sku": "PNT-CAN-TOM", "name": "Diced Tomatoes 14.5oz",     "qty": 2,  "unit_price": 1.09,  "subtotal": 2.18,   "note": "2 cans tomatoes for salsa"},
        ],
        "subtotal": 67.13, "tax": 4.70, "total": 71.83,
        "points_earned": 162, "points_redeemed": 500, "payment": "publix_card"
    },
    "ORD-2026-0014": {
        "id": "ORD-2026-0014", "customer_id": "CUS-005", "store_id": "store_GA02",
        "date": "2026-06-20", "status": "completed",
        "note": "Deli lunch order and beverage refill",
        "items": [
            {"sku": "DLI-HAM-HNY", "name": "Honey Glazed Ham",          "qty": 1,  "unit_price": 8.99,  "subtotal": 8.99,   "note": "1 lb honey ham, sliced thin"},
            {"sku": "DLI-TKY-RST", "name": "Oven Roasted Turkey Breast","qty": 1,  "unit_price": 10.99, "subtotal": 10.99,  "note": "1 lb turkey breast"},
            {"sku": "BEV-WTR-SPK", "name": "Sparkling Water 12pk",      "qty": 2,  "unit_price": 7.49,  "subtotal": 14.98,  "note": "2 cases sparkling water"},
            {"sku": "BEV-JUC-APL", "name": "Apple Juice 64oz",          "qty": 1,  "unit_price": 4.49,  "subtotal": 4.49,   "note": "1 large apple juice"},
            {"sku": "DRY-EGG-LRG", "name": "Large Eggs Dozen",          "qty": 1,  "unit_price": 6.29,  "subtotal": 6.29,   "note": "1 dozen eggs"},
        ],
        "subtotal": 45.74, "tax": 3.20, "total": 48.94,
        "points_earned": 103, "points_redeemed": 0, "payment": "credit_card"
    },

    # ── CUS-006 Robert Chen (Silver · Coconut Grove) — 3 orders ─────────────────
    "ORD-2026-0015": {
        "id": "ORD-2026-0015", "customer_id": "CUS-006", "store_id": "store_FL04",
        "date": "2026-07-10", "status": "completed",
        "note": "Organic produce and dairy essentials",
        "items": [
            {"sku": "PRD-BAN-ORG", "name": "Organic Bananas",           "qty": 3,  "unit_price": 0.69,  "subtotal": 2.07,   "note": "3 lbs organic bananas"},
            {"sku": "PRD-APL-HON", "name": "Honeycrisp Apples",         "qty": 2,  "unit_price": 2.29,  "subtotal": 4.58,   "note": "2 lbs Honeycrisp apples"},
            {"sku": "PRD-AVC-HAS", "name": "Hass Avocado",              "qty": 6,  "unit_price": 1.49,  "subtotal": 8.94,   "note": "6 ripe avocados"},
            {"sku": "DRY-MLK-WHL", "name": "Whole Milk Gallon",         "qty": 1,  "unit_price": 4.59,  "subtotal": 4.59,   "note": "1 gallon Horizon whole milk"},
            {"sku": "FRZ-ICE-VNL", "name": "Vanilla Bean Ice Cream",    "qty": 2,  "unit_price": 5.99,  "subtotal": 11.98,  "note": "2 tubs vanilla ice cream"},
        ],
        "subtotal": 32.16, "tax": 2.25, "total": 34.41,
        "points_earned": 54, "points_redeemed": 0, "payment": "publix_card"
    },
    "ORD-2026-0016": {
        "id": "ORD-2026-0016", "customer_id": "CUS-006", "store_id": "store_FL04",
        "date": "2026-07-02", "status": "completed",
        "note": "Midweek fruit and breakfast top-up",
        "items": [
            {"sku": "PRD-STR-ORG", "name": "Organic Strawberries 1lb", "qty": 2,  "unit_price": 5.49,  "subtotal": 10.98,  "note": "2 pints fresh strawberries"},
            {"sku": "DRY-EGG-LRG", "name": "Large Eggs Dozen",         "qty": 2,  "unit_price": 6.29,  "subtotal": 12.58,  "note": "2 boxes of eggs"},
            {"sku": "BKR-BRD-WHT", "name": "Whole Wheat Bread",        "qty": 1,  "unit_price": 3.49,  "subtotal": 3.49,   "note": "1 loaf whole wheat bread"},
            {"sku": "DRY-YGT-GRK", "name": "Greek Yogurt Plain 17.6oz","qty": 2,  "unit_price": 2.79,  "subtotal": 5.58,   "note": "2 tubs plain Greek yogurt"},
        ],
        "subtotal": 32.63, "tax": 2.28, "total": 34.91,
        "points_earned": 55, "points_redeemed": 0, "payment": "credit_card"
    },
    "ORD-2026-0017": {
        "id": "ORD-2026-0017", "customer_id": "CUS-006", "store_id": "store_FL04",
        "date": "2026-06-14", "status": "completed",
        "note": "Supplement, health, and pantry restock",
        "items": [
            {"sku": "PHR-VIT-C",   "name": "Vitamin C 1000mg 100ct",   "qty": 1,  "unit_price": 9.99,  "subtotal": 9.99,   "note": "1 bottle Vitamin C tablets"},
            {"sku": "PHR-ADV-200", "name": "Ibuprofen 200mg 100ct",     "qty": 1,  "unit_price": 7.49,  "subtotal": 7.49,   "note": "1 bottle ibuprofen"},
            {"sku": "PNT-RCE-JSM", "name": "Jasmine Rice 5lb",          "qty": 1,  "unit_price": 6.99,  "subtotal": 6.99,   "note": "1 bag jasmine rice"},
            {"sku": "PNT-PNB-CRK", "name": "Creamy Peanut Butter 16oz","qty": 2,  "unit_price": 4.29,  "subtotal": 8.58,   "note": "2 jars creamy peanut butter"},
            {"sku": "PRD-KAL-ORG", "name": "Organic Kale Bunch",        "qty": 1,  "unit_price": 2.99,  "subtotal": 2.99,   "note": "1 bunch organic kale"},
        ],
        "subtotal": 36.04, "tax": 2.52, "total": 38.56,
        "points_earned": 61, "points_redeemed": 0, "payment": "publix_card"
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

def resolve_customer(body):
    """Return (customer_dict, error_response) from customer_id OR phone lookup."""
    cid   = body.get("customer_id")
    phone = str(body.get("phone", "")).strip()
    if not cid and not phone:
        return None, api_err("Supply either 'customer_id' or 'phone'.", 400)
    if cid:
        c = CUSTOMERS.get(cid)
        return (c, api_err(f"Customer '{cid}' not found.", 404)) if not c else (c, None)
    digits = "".join(ch for ch in phone if ch.isdigit())
    if len(digits) < 4:
        return None, api_err("'phone' must contain at least 4 digits.", 400)
    for c in CUSTOMERS.values():
        pd = "".join(ch for ch in c.get("phone",  "") if ch.isdigit())
        md = "".join(ch for ch in c.get("mobile", "") if ch.isdigit())
        if digits in pd or digits in md:
            return c, None
    return None, api_err(f"No customer found matching phone '{phone}'.", 404)

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
                "description": "List all orders filtered by customer_id OR phone/mobile number, store, or status. Supply customer_id or phone — not both.",
                "operationId": "listOrders",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/OrdersRequest"},
                            "examples": {
                                "by_id":    {"summary": "By customer ID",   "value": {"customer_id": "CUS-001", "page": 1, "limit": 10}},
                                "by_phone": {"summary": "By phone number",  "value": {"phone": "786-304-8821"}},
                            },
                        }
                    },
                },
                "responses": {"200": {"description": "Paginated order list with customer info attached"}, "400": {"description": "Invalid request"}, "404": {"description": "Customer not found"}},
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
                "description": "Get spending summary by customer_id OR phone/mobile number.",
                "operationId": "purchaseSummary",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/PhoneLookupRequest"},
                            "examples": {
                                "by_id":    {"summary": "By customer ID",  "value": {"customer_id": "CUS-001"}},
                                "by_phone": {"summary": "By phone number", "value": {"phone": "786-304-8821"}},
                            },
                        }
                    },
                },
                "responses": {"200": {"description": "Spending totals, favorite category, order stats"}, "400": {"description": "No lookup key supplied"}, "404": {"description": "Customer not found"}},
            }
        },
        "/api/history/by-category": {
            "post": {
                "tags": ["History"], "summary": "Spend by category",
                "description": "Get spend breakdown by category using customer_id OR phone/mobile number.",
                "operationId": "spendByCategory",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/PhoneLookupRequest"},
                            "examples": {
                                "by_id":    {"summary": "By customer ID",  "value": {"customer_id": "CUS-002"}},
                                "by_phone": {"summary": "By phone number", "value": {"phone": "404-871-2256"}},
                            },
                        }
                    },
                },
                "responses": {"200": {"description": "Spending breakdown by product category"}, "404": {"description": "Customer not found"}},
            }
        },
        "/api/history/top-products": {
            "post": {
                "tags": ["History"], "summary": "Most purchased products",
                "description": "Get top products by quantity using customer_id OR phone/mobile number.",
                "operationId": "topProducts",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/TopProductsRequest"},
                            "examples": {
                                "by_id":    {"summary": "By customer ID",  "value": {"customer_id": "CUS-001", "limit": 5}},
                                "by_phone": {"summary": "By phone number", "value": {"phone": "786-304-8821", "limit": 5}},
                            },
                        }
                    },
                },
                "responses": {"200": {"description": "Top products by quantity purchased"}, "404": {"description": "Customer not found"}},
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
            "PhoneLookupRequest": {
                "type": "object",
                "description": "Supply exactly one of customer_id or phone.",
                "properties": {
                    "customer_id": {"type": "string", "example": "CUS-001",      "description": "Unique customer ID"},
                    "phone":       {"type": "string", "example": "786-304-8821", "description": "Phone or mobile — any format, min 4 digits"},
                },
            },
            "OrdersRequest": {
                "type": "object",
                "description": "Supply customer_id OR phone to filter by customer. Both are optional — omit both to return all orders.",
                "properties": {
                    "customer_id": {"type": "string",  "example": "CUS-001",      "description": "Filter by customer ID"},
                    "phone":       {"type": "string",  "example": "786-304-8821", "description": "Filter by phone or mobile number (any format, min 4 digits)"},
                    "store_id":    {"type": "string"},
                    "status":      {"type": "string", "enum": ["completed","pending","cancelled"]},
                    "page":        {"type": "integer", "default": 1},
                    "limit":       {"type": "integer", "default": 20},
                },
            },
            "TopProductsRequest": {
                "type": "object",
                "description": "Supply customer_id OR phone.",
                "properties": {
                    "customer_id": {"type": "string", "example": "CUS-001"},
                    "phone":       {"type": "string", "example": "786-304-8821", "description": "Phone or mobile number (any format, min 4 digits)"},
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
    store_id = body.get("store_id")
    status   = body.get("status")
    page     = body.get("page", 1)
    limit    = body.get("limit", 20)

    items = list(ORDERS.values())

    # phone or customer_id filter — both optional for orders list
    if body.get("customer_id") or body.get("phone"):
        c, err = resolve_customer(body)
        if err: return err
        items = [o for o in items if o["customer_id"] == c["id"]]

    if store_id: items = [o for o in items if o["store_id"] == store_id]
    if status:   items = [o for o in items if o["status"] == status]
    items.sort(key=lambda x: x["date"], reverse=True)

    # attach customer name and phone to each order for convenience
    for o in items:
        c = CUSTOMERS.get(o["customer_id"], {})
        o["customer_name"]  = f"{c.get('first_name','')} {c.get('last_name','')}".strip()
        o["customer_phone"] = c.get("phone", "")

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
    c, err = resolve_customer(body)
    if err: return err

    orders  = customer_orders(c["id"])
    summary = spending_summary(orders)
    summary["customer_id"]    = c["id"]
    summary["customer_name"]  = f"{c['first_name']} {c['last_name']}"
    summary["customer_phone"] = c.get("phone", "")
    summary["tier"]           = c["tier"]
    summary["points_balance"] = c["points_balance"]
    summary["member_since"]   = c["joined"]
    return jsonify(summary)


@app.route("/api/history/by-category", methods=["POST"])
def spend_by_category():
    body = request.json or {}
    c, err = resolve_customer(body)
    if err: return err

    orders = customer_orders(c["id"])
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
        "customer_id":    c["id"],
        "customer_name":  f"{c['first_name']} {c['last_name']}",
        "customer_phone": c.get("phone", ""),
        "breakdown":      breakdown,
        "total_spent":    round(sum(o["total"] for o in orders), 2),
    })


@app.route("/api/history/top-products", methods=["POST"])
def top_products():
    body  = request.json or {}
    limit = min(20, int(body.get("limit", 5)))
    c, err = resolve_customer(body)
    if err: return err

    orders = customer_orders(c["id"])
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

    return jsonify({"customer_id": c["id"], "customer_phone": c.get("phone",""), "top_products": results})

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
