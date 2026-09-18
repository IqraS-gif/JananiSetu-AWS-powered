"""
janani_agent_server/opensearch/ingest.py

One-time data ingestion script.
Run this ONCE after starting OpenSearch to populate all indices.

Usage:
    python opensearch/ingest.py

Data sources indexed:
    - maa-app/nutrition_dataset.csv    → janani-nutrition   (1,014 food items)
    - maa-app/learn_content.json       → janani-knowledge   (~120 pregnancy articles)
    - Hardcoded schemes                → janani-schemes     (10 govt scheme docs)
    - medical_kb.py                    → janani-medical     (12 curated Q&A docs)
"""

import os
import sys
import csv
import json
import time

# Add parent dir to path so we can import client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opensearch.client import (
    get_client,
    create_indices,
    bulk_index,
    IDX_NUTRITION,
    IDX_KNOWLEDGE,
    IDX_SCHEMES,
    IDX_MEDICAL,
)
from opensearch.medical_kb import MEDICAL_DOCUMENTS

# Paths to data files (relative to this script's parent directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # janani_agent_server/
MAA_APP_DIR = os.path.join(BASE_DIR, "..", "maa-app")                   # maa-app/
NUTRITION_CSV = os.path.join(MAA_APP_DIR, "nutrition_dataset.csv")
LEARN_JSON    = os.path.join(MAA_APP_DIR, "learn_content.json")


def safe_float(val, default=0.0):
    try:
        return float(str(val).replace(",", "").strip())
    except (ValueError, TypeError):
        return default


# ── Ingest 1: Nutrition dataset ───────────────────────────────────────────────

def ingest_nutrition(client):
    print("\n[1/4] Ingesting nutrition_dataset.csv...")
    docs = []

    with open(NUTRITION_CSV, encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            name = row.get("Dish Name", "").strip()
            if not name:
                continue

            cal  = safe_float(row.get("Calories (kcal)", 0))
            prot = safe_float(row.get("Protein (g)", 0))
            carb = safe_float(row.get("Carbohydrates (g)", 0))
            fat  = safe_float(row.get("Fats (g)", 0))
            iron = safe_float(row.get("Iron (mg)", 0))
            ca   = safe_float(row.get("Calcium (mg)", 0))
            fol  = safe_float(row.get("Folate (\ufefeg)", row.get("Folate (µg)", row.get("Folate (g)", 0))))
            vitc = safe_float(row.get("Vitamin C (mg)", 0))
            fib  = safe_float(row.get("Fibre (g)", 0))
            sod  = safe_float(row.get("Sodium (mg)", 0))

            text = (
                f"{name} calories {cal} kcal protein {prot}g carbs {carb}g "
                f"fat {fat}g iron {iron}mg calcium {ca}mg folate {fol}mcg "
                f"vitamin C {vitc}mg fibre {fib}g sodium {sod}mg pregnancy nutrition food"
            )

            doc = {
                "dish_name":    name,
                "calories":     cal,
                "protein_g":    prot,
                "carbs_g":      carb,
                "fat_g":        fat,
                "iron_mg":      iron,
                "calcium_mg":   ca,
                "folate_ug":    fol,
                "vitamin_c_mg": vitc,
                "fibre_g":      fib,
                "sodium_mg":    sod,
                "text":         text,
            }
            docs.append((f"nutrition_{i}", doc))

    bulk_index(client, IDX_NUTRITION, docs)
    print(f"  Indexed {len(docs)} food items into {IDX_NUTRITION}")


# ── Ingest 2: Learn content articles ─────────────────────────────────────────

def ingest_knowledge(client):
    print("\n[2/4] Ingesting learn_content.json articles...")
    docs = []

    with open(LEARN_JSON, encoding="utf-8") as f:
        data = json.load(f)

    topics = data.get("topics", [])
    for topic in topics:
        topic_id = topic.get("id", "")
        topic_en = topic.get("titleEn", "")

        articles = topic.get("articles", [])
        for art in articles:
            art_id   = art.get("id", "")
            title_en = art.get("titleEn", "")
            title_hi = art.get("titleHi", "")
            body_en  = art.get("bodyEn", "")
            body_hi  = art.get("bodyHi", "")
            tags     = art.get("tags", [])
            week     = art.get("week_relevance", 0)

            # key takeaways as extra text
            takeaways_en = " ".join(art.get("key_takeaways_en", []))

            text = f"{title_en} {title_hi} {body_en} {takeaways_en} {topic_en} pregnancy maternal health"

            doc = {
                "article_id":     art_id,
                "topic_id":       topic_id,
                "topic_en":       topic_en,
                "title_en":       title_en,
                "title_hi":       title_hi,
                "body_en":        body_en[:2000],   # truncate very long bodies
                "body_hi":        body_hi[:2000],
                "tags":           tags,
                "week_relevance": week,
                "text":           text[:3000],
            }
            docs.append((art_id, doc))

        # Also index daily tips if present
    for i, tip in enumerate(data.get("daily_tips", [])):
        doc = {
            "article_id":     f"tip_{i}",
            "topic_id":       "daily_tips",
            "topic_en":       "Daily Tips",
            "title_en":       tip.get("titleEn", f"Tip {i}"),
            "title_hi":       tip.get("titleHi", ""),
            "body_en":        tip.get("bodyEn", ""),
            "body_hi":        tip.get("bodyHi", ""),
            "tags":           [],
            "week_relevance": 0,
            "text":           f"{tip.get('titleEn','')} {tip.get('bodyEn','')} pregnancy daily tip",
        }
        docs.append((f"tip_{i}", doc))

    bulk_index(client, IDX_KNOWLEDGE, docs)
    print(f"  Indexed {len(docs)} knowledge articles into {IDX_KNOWLEDGE}")


# ── Ingest 3: Government schemes ─────────────────────────────────────────────

def ingest_schemes(client):
    print("\n[3/4] Ingesting government scheme documents...")

    schemes = [
        {
            "scheme_id":   "pmmvy",
            "name":        "PMMVY - Pradhan Mantri Matru Vandana Yojana",
            "benefit":     "Rs.6,000 cash transfer in 3 instalments for first live birth",
            "eligibility": "All pregnant women for first live birth. Aadhaar and bank account needed.",
            "action":      "Register at nearest Anganwadi centre with Aadhaar card and bank passbook. Do it before 19 weeks for full benefit.",
            "urgency":     "HIGH",
            "category":    "cash_transfer",
            "text":        "PMMVY Pradhan Mantri Matru Vandana Yojana 6000 rupees cash first birth anganwadi aadhaar bank",
        },
        {
            "scheme_id":   "jsy",
            "name":        "JSY - Janani Suraksha Yojana",
            "benefit":     "Rs.1,400 cash (rural) or Rs.1,000 (urban) for institutional delivery",
            "eligibility": "BPL (Below Poverty Line) pregnant women. All women in low-performing states.",
            "action":      "Register with your ASHA worker before delivery. Carry BPL card and Aadhaar to hospital.",
            "urgency":     "HIGH",
            "category":    "delivery_benefit",
            "text":        "JSY Janani Suraksha Yojana 1400 rupees delivery institutional BPL ASHA hospital cash",
        },
        {
            "scheme_id":   "jssk",
            "name":        "JSSK - Janani Shishu Suraksha Karyakaram",
            "benefit":     "Free delivery, free medicines, free diet, free blood, free transport to government hospital",
            "eligibility": "All pregnant women delivering in government hospitals. No cost at all.",
            "action":      "Go to government hospital (PHC/CHC/District Hospital). Show Aadhaar. Everything is free.",
            "urgency":     "HIGH",
            "category":    "free_services",
            "text":        "JSSK Janani Shishu Suraksha free delivery medicines diet blood transport government hospital",
        },
        {
            "scheme_id":   "anc_checkup",
            "name":        "Free Antenatal Checkups (ANC)",
            "benefit":     "4 free ANC visits including blood tests, urine tests, weight, BP, ultrasound",
            "eligibility": "All pregnant women at PHC/CHC",
            "action":      "Visit PHC/CHC with MCP (Mother and Child Protection) card for all 4 scheduled ANC visits.",
            "urgency":     "HIGH",
            "category":    "healthcare",
            "text":        "antenatal checkup ANC free blood test urine weight BP ultrasound PHC CHC MCP card pregnancy",
        },
        {
            "scheme_id":   "iron_supplements",
            "name":        "Free Iron Folic Acid (IFA) Supplements",
            "benefit":     "Free iron and folic acid tablets throughout pregnancy and 6 months postpartum",
            "eligibility": "All pregnant and lactating women",
            "action":      "Ask your ASHA worker or visit nearest PHC/sub-centre/Anganwadi to get tablets.",
            "urgency":     "HIGH",
            "category":    "supplements",
            "text":        "iron folic acid IFA tablets free supplements pregnancy postpartum ASHA PHC anemia prevention",
        },
        {
            "scheme_id":   "poshan_abhiyan",
            "name":        "POSHAN Abhiyan - Supplementary Nutrition",
            "benefit":     "Free supplementary nutrition (Take Home Ration / hot meals) at Anganwadi",
            "eligibility": "All pregnant and lactating women",
            "action":      "Visit nearest Anganwadi centre and register. Collect nutrition supplement every week.",
            "urgency":     "MEDIUM",
            "category":    "nutrition",
            "text":        "POSHAN Abhiyan nutrition supplement anganwadi THR take home ration hot meals pregnant lactating",
        },
        {
            "scheme_id":   "pradhan_mantri_surakshit_matritva",
            "name":        "PMSMA - Pradhan Mantri Surakshit Matritva Abhiyan",
            "benefit":     "Free antenatal checkup by specialist doctor on 9th of every month",
            "eligibility": "All pregnant women",
            "action":      "Visit government health facility on the 9th of each month for specialist ANC checkup.",
            "urgency":     "MEDIUM",
            "category":    "healthcare",
            "text":        "PMSMA safe motherhood specialist doctor ANC checkup 9th every month free antenatal",
        },
        {
            "scheme_id":   "tt_vaccine",
            "name":        "Free Tetanus Toxoid (TT) Vaccination",
            "benefit":     "Free TT vaccine — 2 doses to protect mother and baby from tetanus",
            "eligibility": "All pregnant women",
            "action":      "Get TT1 as soon as pregnancy confirmed. TT2 four weeks later. Free at PHC/hospital.",
            "urgency":     "HIGH",
            "category":    "vaccines",
            "text":        "TT tetanus toxoid vaccine injection free pregnancy two doses PHC hospital protection",
        },
        {
            "scheme_id":   "pm_jan_arogya",
            "name":        "PM-JAY (Ayushman Bharat) Maternity Cover",
            "benefit":     "Up to Rs.5 lakh health cover for pregnancy complications and delivery",
            "eligibility": "BPL/SECC beneficiary families. Check eligibility at pmjay.gov.in",
            "action":      "Check eligibility at pmjay.gov.in using your ration card. Get Ayushman card from Anganwadi or bank.",
            "urgency":     "MEDIUM",
            "category":    "insurance",
            "text":        "PM-JAY Ayushman Bharat 5 lakh health insurance maternity BPL ration card eligibility",
        },
        {
            "scheme_id":   "rashtriya_parivar_labh",
            "name":        "Rashtriya Parivar Labh Yojana (for BPL)",
            "benefit":     "Rs.20,000 one-time support for BPL families losing primary earner",
            "eligibility": "BPL families where primary earning member dies",
            "action":      "Apply at district social welfare office with death certificate and BPL card.",
            "urgency":     "LOW",
            "category":    "social_security",
            "text":        "Rashtriya Parivar Labh Yojana 20000 BPL family death primary earner district welfare",
        },
    ]

    docs = [(s["scheme_id"], s) for s in schemes]
    bulk_index(client, IDX_SCHEMES, docs)
    print(f"  Indexed {len(docs)} scheme documents into {IDX_SCHEMES}")


# ── Ingest 4: Medical knowledge base ──────────────────────────────────────────

def ingest_medical(client):
    print("\n[4/4] Ingesting curated medical Q&A knowledge base...")
    docs = [(doc["doc_id"], doc) for doc in MEDICAL_DOCUMENTS]
    bulk_index(client, IDX_MEDICAL, docs)
    print(f"  Indexed {len(docs)} medical Q&A documents into {IDX_MEDICAL}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  Janani OpenSearch Data Ingestion")
    print("=" * 55)
    print(f"\n  Connecting to OpenSearch...")

    client = get_client()

    # Wait for OpenSearch to be ready
    for attempt in range(10):
        try:
            info = client.info()
            print(f"  Connected! OpenSearch version: {info['version']['number']}")
            break
        except Exception as e:
            if attempt == 9:
                print(f"\n[ERROR] Could not connect to OpenSearch after 10 attempts.")
                print("  Make sure OpenSearch is running:")
                print("  > docker-compose up -d")
                print("  Then wait ~30 seconds and retry.")
                sys.exit(1)
            print(f"  Waiting for OpenSearch... (attempt {attempt+1}/10)")
            time.sleep(5)

    print("\n  Creating indices...")
    create_indices(client)

    ingest_nutrition(client)
    ingest_knowledge(client)
    ingest_schemes(client)
    ingest_medical(client)

    print("\n" + "=" * 55)
    print("  Ingestion complete!")
    print("  View data at: http://localhost:5601 (OpenSearch Dashboards)")
    print("=" * 55)


if __name__ == "__main__":
    main()
