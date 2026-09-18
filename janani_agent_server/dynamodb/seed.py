"""
janani_agent_server/dynamodb/seed.py

One-time database seed script for DynamoDB Local.
Creates the tables and populates sample patient profiles, ANC checkup visits,
and daily nutrition logs.

Usage:
    python -m dynamodb.seed
    or
    python dynamodb/seed.py
"""

import sys
import os
import time

# Ensure parent directory is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dynamodb.client import (
    create_tables_if_not_exist,
    put_patient,
    log_visit,
    log_nutrition,
    get_patient,
    get_visits,
    get_dynamodb_client,
)

SAMPLE_PATIENTS = [
    {
        "user_id": "user_001",
        "name": "Sunita Sharma (सुनीता शर्मा)",
        "age": 24,
        "pregnancy_week": 28,
        "trimester": 3,
        "bp_systolic": 118,
        "bp_diastolic": 76,
        "blood_glucose_mg_dl": 98,
        "hemoglobin_g_dl": 11.2,
        "bp_risk": "LOW",
        "diabetes_risk": "LOW",
        "ration_category": "BPL",
        "assigned_asha_id": "asha_101",
        "assigned_asha_name": "Meena Devi",
        "notes": "All vitals normal. Regular iron-folic acid intake.",
    },
    {
        "user_id": "user_002",
        "name": "Pooja Devi (पूजा देवी)",
        "age": 29,
        "pregnancy_week": 32,
        "trimester": 3,
        "bp_systolic": 148,
        "bp_diastolic": 96,
        "blood_glucose_mg_dl": 188,
        "hemoglobin_g_dl": 10.1,
        "bp_risk": "HIGH",
        "diabetes_risk": "HIGH",
        "ration_category": "APL",
        "assigned_asha_id": "asha_102",
        "assigned_asha_name": "Kavita Rani",
        "notes": "High BP and high glucose. Advised low-salt diet and weekly PHC review.",
    },
    {
        "user_id": "user_003",
        "name": "Anita Kumari (अनीता कुमारी)",
        "age": 22,
        "pregnancy_week": 16,
        "trimester": 2,
        "bp_systolic": 110,
        "bp_diastolic": 70,
        "blood_glucose_mg_dl": 92,
        "hemoglobin_g_dl": 9.4,
        "bp_risk": "LOW",
        "diabetes_risk": "LOW",
        "ration_category": "BPL",
        "assigned_asha_id": "asha_101",
        "assigned_asha_name": "Meena Devi",
        "notes": "Mild anemia. Prescribed double dose of Iron & Folic Acid tablets.",
    },
]

SAMPLE_VISITS = [
    # Visits for user_001
    {
        "user_id": "user_001",
        "visit_id": "visit_001_anc1",
        "visit_type": "ANC-1",
        "pregnancy_week": 12,
        "bp_systolic": 115,
        "bp_diastolic": 74,
        "blood_glucose_mg_dl": 95,
        "weight_kg": 52.0,
        "recorded_by": "ASHA Meena Devi",
        "notes": "First trimester registration. MCP card issued. IFA tablets started.",
    },
    {
        "user_id": "user_001",
        "visit_id": "visit_001_anc2",
        "visit_type": "ANC-2",
        "pregnancy_week": 20,
        "bp_systolic": 116,
        "bp_diastolic": 75,
        "blood_glucose_mg_dl": 96,
        "weight_kg": 54.5,
        "recorded_by": "Dr. R. K. Verma (PHC)",
        "notes": "Anomaly scan normal. Fetal movements felt.",
    },
    {
        "user_id": "user_001",
        "visit_id": "visit_001_anc3",
        "visit_type": "ANC-3",
        "pregnancy_week": 28,
        "bp_systolic": 118,
        "bp_diastolic": 76,
        "blood_glucose_mg_dl": 98,
        "weight_kg": 57.0,
        "recorded_by": "ASHA Meena Devi",
        "notes": "All vitals stable. Counseled on danger signs and delivery plan.",
    },
    # Visits for user_002
    {
        "user_id": "user_002",
        "visit_id": "visit_002_anc1",
        "visit_type": "ANC-2",
        "pregnancy_week": 24,
        "bp_systolic": 138,
        "bp_diastolic": 88,
        "blood_glucose_mg_dl": 160,
        "weight_kg": 64.0,
        "recorded_by": "Dr. S. Sharma",
        "notes": "Borderline blood pressure and glucose. Scheduled OGTT test.",
    },
    {
        "user_id": "user_002",
        "visit_id": "visit_002_anc2",
        "visit_type": "ANC-3",
        "pregnancy_week": 32,
        "bp_systolic": 148,
        "bp_diastolic": 96,
        "blood_glucose_mg_dl": 188,
        "weight_kg": 67.5,
        "recorded_by": "Dr. S. Sharma",
        "notes": "Diagnosed gestational hypertension and gestational diabetes. Urgent hospital referral.",
    },
]

SAMPLE_NUTRITION_LOGS = [
    {"user_id": "user_001", "meal": "Breakfast", "food": "Moong dal cheela + milk", "calories": 280, "iron_mg": 3.8, "calcium_mg": 160},
    {"user_id": "user_001", "meal": "Lunch", "food": "Roti (2), Palak dal, Rice, Curd", "calories": 520, "iron_mg": 6.2, "calcium_mg": 240},
    {"user_id": "user_002", "meal": "Breakfast", "food": "Oats with nuts and milk", "calories": 250, "iron_mg": 2.1, "calcium_mg": 140},
]


def seed_database():
    print("🌱 Starting DynamoDB Local seeding...")
    
    # 1. Ensure connection
    try:
        client = get_dynamodb_client()
        tables = client.list_tables().get("TableNames", [])
        print(f"Connected to DynamoDB. Existing tables: {tables}")
    except Exception as e:
        print(f"❌ Could not connect to DynamoDB Local: {e}")
        print("💡 Make sure DynamoDB Local is running:")
        print("   cd janani_agent_server && docker-compose up -d")
        return False

    # 2. Create tables
    create_tables_if_not_exist()
    time.sleep(1)

    # 3. Seed Patients
    print(f"\nSeeding {len(SAMPLE_PATIENTS)} patient profiles...")
    for p in SAMPLE_PATIENTS:
        success = put_patient(p)
        status = "✅" if success else "❌"
        print(f"  {status} Seeded patient {p['user_id']} ({p['name']})")

    # 4. Seed Visits
    print(f"\nSeeding {len(SAMPLE_VISITS)} ANC checkup visits...")
    for v in SAMPLE_VISITS:
        vid = log_visit(v["user_id"], v)
        status = "✅" if vid else "❌"
        print(f"  {status} Seeded visit {v['visit_id']} for {v['user_id']}")

    # 5. Seed Nutrition Logs
    print(f"\nSeeding {len(SAMPLE_NUTRITION_LOGS)} nutrition logs...")
    for n in SAMPLE_NUTRITION_LOGS:
        ok = log_nutrition(n["user_id"], n)
        status = "✅" if ok else "❌"
        print(f"  {status} Seeded nutrition log for {n['user_id']} ({n['meal']})")

    # Verification
    print("\nVerifying data in DynamoDB...")
    patient = get_patient("user_001")
    visits = get_visits("user_001")
    print(f"  Verified user_001: Name={patient.get('name')}, Week={patient.get('pregnancy_week')}")
    print(f"  Verified user_001 visits count: {len(visits)}")
    
    print("\n✨ DynamoDB Local seeding completed successfully!")
    return True


if __name__ == "__main__":
    seed_database()
