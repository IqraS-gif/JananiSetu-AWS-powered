"""
janani_agent_server/opensearch/client.py

OpenSearch client for the Janani health knowledge RAG system.
Connects to local OpenSearch (Docker) — no AWS account needed.

Indices:
  janani-nutrition   : 1,014 Indian food nutritional records
  janani-knowledge   : Pregnancy articles (EN + HI, bilingual)
  janani-schemes     : Government welfare scheme documents
  janani-medical     : Curated pregnancy medical Q&A
"""

import os
from opensearchpy import OpenSearch, RequestError

OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "http://localhost:9200")

# Index names
IDX_NUTRITION  = "janani-nutrition"
IDX_KNOWLEDGE  = "janani-knowledge"
IDX_SCHEMES    = "janani-schemes"
IDX_MEDICAL    = "janani-medical"

ALL_INDICES = [IDX_NUTRITION, IDX_KNOWLEDGE, IDX_SCHEMES, IDX_MEDICAL]


def get_client() -> OpenSearch:
    """Return a connected OpenSearch client."""
    host = OPENSEARCH_HOST.replace("http://", "").replace("https://", "")
    host_part, _, port_str = host.partition(":")
    port = int(port_str) if port_str else 9200

    client = OpenSearch(
        hosts=[{"host": host_part, "port": port}],
        use_ssl=False,
        verify_certs=False,
        http_compress=True,
    )
    return client


# ── Index mappings ─────────────────────────────────────────────────────────────

NUTRITION_MAPPING = {
    "mappings": {
        "properties": {
            "dish_name":      {"type": "text", "analyzer": "standard"},
            "calories":       {"type": "float"},
            "protein_g":      {"type": "float"},
            "carbs_g":        {"type": "float"},
            "fat_g":          {"type": "float"},
            "iron_mg":        {"type": "float"},
            "calcium_mg":     {"type": "float"},
            "folate_ug":      {"type": "float"},
            "vitamin_c_mg":   {"type": "float"},
            "fibre_g":        {"type": "float"},
            "sodium_mg":      {"type": "float"},
            "text":           {"type": "text", "analyzer": "standard"},  # full-text search field
        }
    }
}

KNOWLEDGE_MAPPING = {
    "mappings": {
        "properties": {
            "article_id":     {"type": "keyword"},
            "topic_id":       {"type": "keyword"},
            "topic_en":       {"type": "text"},
            "title_en":       {"type": "text", "analyzer": "standard"},
            "title_hi":       {"type": "text", "analyzer": "standard"},
            "body_en":        {"type": "text", "analyzer": "standard"},
            "body_hi":        {"type": "text", "analyzer": "standard"},
            "tags":           {"type": "keyword"},
            "week_relevance": {"type": "integer"},
            "text":           {"type": "text", "analyzer": "standard"},
        }
    }
}

SCHEMES_MAPPING = {
    "mappings": {
        "properties": {
            "scheme_id":      {"type": "keyword"},
            "name":           {"type": "text"},
            "benefit":        {"type": "text"},
            "eligibility":    {"type": "text"},
            "action":         {"type": "text"},
            "urgency":        {"type": "keyword"},
            "category":       {"type": "keyword"},
            "text":           {"type": "text", "analyzer": "standard"},
        }
    }
}

MEDICAL_MAPPING = {
    "mappings": {
        "properties": {
            "doc_id":         {"type": "keyword"},
            "category":       {"type": "keyword"},
            "question_en":    {"type": "text", "analyzer": "standard"},
            "answer_en":      {"type": "text", "analyzer": "standard"},
            "question_hi":    {"type": "text", "analyzer": "standard"},
            "answer_hi":      {"type": "text", "analyzer": "standard"},
            "trimester":      {"type": "integer"},
            "is_emergency":   {"type": "boolean"},
            "text":           {"type": "text", "analyzer": "standard"},
        }
    }
}

INDEX_MAPPINGS = {
    IDX_NUTRITION: NUTRITION_MAPPING,
    IDX_KNOWLEDGE: KNOWLEDGE_MAPPING,
    IDX_SCHEMES:   SCHEMES_MAPPING,
    IDX_MEDICAL:   MEDICAL_MAPPING,
}


def create_indices(client: OpenSearch):
    """Create all Janani indices if they don't exist."""
    for index_name, mapping in INDEX_MAPPINGS.items():
        if not client.indices.exists(index=index_name):
            client.indices.create(index=index_name, body=mapping)
            print(f"  [OpenSearch] Created index: {index_name}")
        else:
            print(f"  [OpenSearch] Index already exists: {index_name}")


def search(
    query: str,
    index: str = None,
    top_k: int = 3,
) -> list[dict]:
    """
    Full-text search across Janani knowledge indices.

    Args:
        query:  Search query string
        index:  Specific index to search (None = all indices)
        top_k:  Number of results to return

    Returns:
        List of matching documents (as dicts with _source + _score)
    """
    client = get_client()

    target_index = index if index else ",".join(ALL_INDICES)

    search_body = {
        "size": top_k,
        "query": {
            "multi_match": {
                "query": query,
                "fields": [
                    "text^2",           # boosted combined field
                    "title_en^2",
                    "title_hi^2",
                    "body_en",
                    "body_hi",
                    "dish_name^2",
                    "question_en^2",
                    "question_hi^2",
                    "answer_en",
                    "answer_hi",
                    "name^2",
                    "benefit",
                    "eligibility",
                ],
                "type": "best_fields",
                "fuzziness": "AUTO",
            }
        },
    }

    try:
        response = client.search(index=target_index, body=search_body)
        hits = response["hits"]["hits"]
        return [
            {
                "score":  hit["_score"],
                "index":  hit["_index"],
                "source": hit["_source"],
            }
            for hit in hits
        ]
    except Exception as e:
        print(f"[OpenSearch] Search error: {e}")
        return []


def index_document(client: OpenSearch, index: str, doc_id: str, doc: dict):
    """Index a single document."""
    client.index(index=index, id=doc_id, body=doc)


def bulk_index(client: OpenSearch, index: str, docs: list[tuple[str, dict]]):
    """
    Bulk index documents. docs is list of (id, body) tuples.
    Uses simple loop for clarity; for >10k docs use opensearch bulk helper.
    """
    for doc_id, body in docs:
        client.index(index=index, id=doc_id, body=body)
