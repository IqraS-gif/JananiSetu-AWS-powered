"""
janani_agent_server/dynamodb package
Provides DynamoDB Local client, table provisioning, and persistence operations.
"""

from .client import (
    get_dynamodb_resource,
    get_dynamodb_client,
    create_tables_if_not_exist,
    get_patient,
    put_patient,
    log_visit,
    get_visits,
    log_nutrition,
    get_nutrition_logs,
    PATIENTS_TABLE,
    VISITS_TABLE,
    NUTRITION_LOGS_TABLE,
)

__all__ = [
    "get_dynamodb_resource",
    "get_dynamodb_client",
    "create_tables_if_not_exist",
    "get_patient",
    "put_patient",
    "log_visit",
    "get_visits",
    "log_nutrition",
    "get_nutrition_logs",
    "PATIENTS_TABLE",
    "VISITS_TABLE",
    "NUTRITION_LOGS_TABLE",
]
