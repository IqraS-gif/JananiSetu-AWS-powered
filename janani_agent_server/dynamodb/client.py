"""
janani_agent_server/dynamodb/client.py

DynamoDB Local client for JananiSetu.
Enables local NoSQL persistence for patient profiles, ANC checkup visits,
and daily nutrition logs — running 100% locally with no AWS account required.

Architecture:
    React Native (maa-app)
        ↓
    FastAPI (main.py) / Strands Agent (agent.py)
        ↓
    DynamoDB Local (port 8001)
        ↓
    JananiPatients / JananiVisits / JananiNutritionLogs

Switching to Real AWS DynamoDB:
    Simply set USE_AWS_DYNAMODB=true and configure standard AWS credentials
    in .env. The same boto3 code works seamlessly without changes!
"""

import os
import time
import json
from decimal import Decimal
from typing import Optional, Dict, Any, List
import boto3
from botocore.exceptions import ClientError


# ── Table Names ───────────────────────────────────────────────────────────────
PATIENTS_TABLE       = os.getenv("DYNAMODB_PATIENTS_TABLE", "JananiPatients")
VISITS_TABLE         = os.getenv("DYNAMODB_VISITS_TABLE", "JananiVisits")
NUTRITION_LOGS_TABLE = os.getenv("DYNAMODB_NUTRITION_TABLE", "JananiNutritionLogs")


# ── Helper: Decimal <-> Python types ──────────────────────────────────────────
def _to_dynamodb_friendly(obj: Any) -> Any:
    """Recursively convert float to Decimal for DynamoDB serialization."""
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: _to_dynamodb_friendly(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_to_dynamodb_friendly(v) for v in obj]
    return obj


def _from_dynamodb_friendly(obj: Any) -> Any:
    """Recursively convert Decimal back to int/float for JSON serialization."""
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    elif isinstance(obj, dict):
        return {k: _from_dynamodb_friendly(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_from_dynamodb_friendly(v) for v in obj]
    return obj


# ── Connection Factory ────────────────────────────────────────────────────────
def get_dynamodb_resource():
    """
    Returns boto3 DynamoDB resource.
    Points to DynamoDB Local (default http://localhost:8001) unless
    USE_AWS_DYNAMODB=true is set.
    """
    use_real_aws = os.getenv("USE_AWS_DYNAMODB", "false").lower() == "true"
    
    if use_real_aws:
        region = os.getenv("AWS_REGION", "us-east-1")
        return boto3.resource("dynamodb", region_name=region)
    else:
        endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8001")
        return boto3.resource(
            "dynamodb",
            endpoint_url=endpoint_url,
            region_name="us-east-1",
            aws_access_key_id="local",
            aws_secret_access_key="local",
        )


def get_dynamodb_client():
    """Returns low-level boto3 DynamoDB client."""
    use_real_aws = os.getenv("USE_AWS_DYNAMODB", "false").lower() == "true"
    
    if use_real_aws:
        region = os.getenv("AWS_REGION", "us-east-1")
        return boto3.client("dynamodb", region_name=region)
    else:
        endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8001")
        return boto3.client(
            "dynamodb",
            endpoint_url=endpoint_url,
            region_name="us-east-1",
            aws_access_key_id="local",
            aws_secret_access_key="local",
        )


# ── Table Provisioning ────────────────────────────────────────────────────────
def create_tables_if_not_exist():
    """
    Creates the required DynamoDB tables if they don't already exist.
    Idempotent and safe to run on startup.
    """
    db = get_dynamodb_resource()
    existing_tables = [t.name for t in db.tables.all()]
    
    # 1. JananiPatients: Key = user_id (String)
    if PATIENTS_TABLE not in existing_tables:
        print(f"[DynamoDB] Creating table: {PATIENTS_TABLE}...")
        db.create_table(
            TableName=PATIENTS_TABLE,
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        print(f"[DynamoDB] Created table: {PATIENTS_TABLE}")

    # 2. JananiVisits: Key = user_id (HASH), visit_id (RANGE)
    if VISITS_TABLE not in existing_tables:
        print(f"[DynamoDB] Creating table: {VISITS_TABLE}...")
        db.create_table(
            TableName=VISITS_TABLE,
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"},
                {"AttributeName": "visit_id", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"},
                {"AttributeName": "visit_id", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        print(f"[DynamoDB] Created table: {VISITS_TABLE}")

    # 3. JananiNutritionLogs: Key = user_id (HASH), timestamp (RANGE)
    if NUTRITION_LOGS_TABLE not in existing_tables:
        print(f"[DynamoDB] Creating table: {NUTRITION_LOGS_TABLE}...")
        db.create_table(
            TableName=NUTRITION_LOGS_TABLE,
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        print(f"[DynamoDB] Created table: {NUTRITION_LOGS_TABLE}")


# ── Patient Operations ────────────────────────────────────────────────────────
def get_patient(user_id: str) -> Optional[Dict[str, Any]]:
    """Fetch patient profile by user_id."""
    try:
        db = get_dynamodb_resource()
        table = db.Table(PATIENTS_TABLE)
        res = table.get_item(Key={"user_id": user_id})
        item = res.get("Item")
        return _from_dynamodb_friendly(item) if item else None
    except Exception as e:
        print(f"[DynamoDB] get_patient error: {e}")
        return None


def put_patient(patient_data: Dict[str, Any]) -> bool:
    """Create or update patient profile."""
    try:
        db = get_dynamodb_resource()
        table = db.Table(PATIENTS_TABLE)
        item = _to_dynamodb_friendly(patient_data)
        item["updated_at"] = int(time.time())
        table.put_item(Item=item)
        return True
    except Exception as e:
        print(f"[DynamoDB] put_patient error: {e}")
        return False


# ── ANC Visit / Checkup Operations ────────────────────────────────────────────
def log_visit(user_id: str, visit_data: Dict[str, Any]) -> Optional[str]:
    """
    Log an ANC visit or vitals checkup for a patient.
    Also updates latest vitals on the patient profile.
    """
    try:
        db = get_dynamodb_resource()
        visits_table = db.Table(VISITS_TABLE)
        
        timestamp = int(time.time())
        visit_id = visit_data.get("visit_id") or f"visit_{timestamp}"
        
        item = {
            "user_id": user_id,
            "visit_id": visit_id,
            "timestamp": timestamp,
            **visit_data,
        }
        visits_table.put_item(Item=_to_dynamodb_friendly(item))

        # Synchronize latest vitals back to patient record
        patient = get_patient(user_id) or {"user_id": user_id}
        for key in ["pregnancy_week", "bp_systolic", "bp_diastolic", "blood_glucose_mg_dl", "bp_risk", "diabetes_risk", "notes"]:
            if key in visit_data:
                patient[key] = visit_data[key]
        put_patient(patient)

        return visit_id
    except Exception as e:
        print(f"[DynamoDB] log_visit error: {e}")
        return None


def get_visits(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get past visits/checkups for a patient ordered newest first."""
    try:
        db = get_dynamodb_resource()
        table = db.Table(VISITS_TABLE)
        from boto3.dynamodb.conditions import Key
        
        res = table.query(
            KeyConditionExpression=Key("user_id").eq(user_id),
            ScanIndexForward=False,  # Descending order
            Limit=limit,
        )
        items = res.get("Items", [])
        return [_from_dynamodb_friendly(it) for it in items]
    except Exception as e:
        print(f"[DynamoDB] get_visits error: {e}")
        return []


# ── Nutrition Log Operations ──────────────────────────────────────────────────
def log_nutrition(user_id: str, entry: Dict[str, Any]) -> bool:
    """Log a food intake record for a patient."""
    try:
        db = get_dynamodb_resource()
        table = db.Table(NUTRITION_LOGS_TABLE)
        timestamp = str(int(time.time() * 1000))
        item = {
            "user_id": user_id,
            "timestamp": timestamp,
            **entry,
        }
        table.put_item(Item=_to_dynamodb_friendly(item))
        return True
    except Exception as e:
        print(f"[DynamoDB] log_nutrition error: {e}")
        return False


def get_nutrition_logs(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Fetch recent nutrition logs for a patient."""
    try:
        db = get_dynamodb_resource()
        table = db.Table(NUTRITION_LOGS_TABLE)
        from boto3.dynamodb.conditions import Key
        
        res = table.query(
            KeyConditionExpression=Key("user_id").eq(user_id),
            ScanIndexForward=False,
            Limit=limit,
        )
        return [_from_dynamodb_friendly(it) for it in res.get("Items", [])]
    except Exception as e:
        print(f"[DynamoDB] get_nutrition_logs error: {e}")
        return []
