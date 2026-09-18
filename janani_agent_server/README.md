# Janani Setu AI Agent Server 🌸

A unified maternal health backend integrating **5 key AWS ecosystem technologies** — running **100% locally with zero cloud bill**:

1. 🤖 **AWS Strands Agents SDK** — AI orchestration with local Ollama or Amazon Bedrock
2. 🔎 **OpenSearch** — RAG retrieval over 1,000+ nutrition records, 120 articles, 10 government schemes, and medical Q&A
3. 🛡️ **Cedar** — Fine-grained authorization engine controlling Mother, ASHA worker, and Doctor access
4. ⚡ **DynamoDB Local** — Local NoSQL data store for patient profiles, ANC checkups, and nutrition logs
5. 🔐 **AWS Firecracker MicroVM** — Isolated hardware-level virtualization sandbox for sensitive clinical triage and PHI protection

---

## 🏛️ Architecture

```
React Native (maa-app)
       │
       ▼ (HTTP POST /chat with user_role)
FastAPI Server (main.py :8000)
       │
       ├── 🛡️ Cedar Policy Engine (cedar_auth.py)
       │      └── Evaluates permit/forbid for Mother vs ASHA vs Doctor
       │
       ├── 🤖 Strands Agent Orchestrator (agent.py)
       │      ├── 🔎 OpenSearch RAG (:9200)
       │      │      └── Semantic search over medical KB, nutrition & schemes
       │      │
       │      ├── ⚡ DynamoDB Local (:8001)
       │      │      ├── JananiPatients (vitals, pregnancy week, risk levels)
       │      │      ├── JananiVisits (ANC checkup history)
       │      │      └── JananiNutritionLogs (daily diet tracking)
       │      │
       │      ├── 🔐 Firecracker MicroVM Sandboxing (firecracker/)
       │      │      ├── Sub-5ms isolated microVM boot
       │      │      ├── Multi-factor Preeclampsia & Obstetric Emergency Triage
       │      │      ├── Sensitive PHI Redaction (Aadhaar, Phone, MCP IDs)
       │      │      └── Pregnancy Medication Contraindication Screening
       │      │
       │      └── 🧮 Rule-based Welfare Schemes (PMMVY, JSY)
       │
       └── 🧠 LLM Backend: Ollama (FREE local) or Amazon Bedrock (Claude)
```

---

## 🚀 Quick Start (Local & Free)

### Step 1: Start Docker Containers (OpenSearch + DynamoDB Local)
```bash
cd janani_agent_server
docker-compose up -d
```
- OpenSearch: `http://localhost:9200`
- OpenSearch Dashboards: `http://localhost:5601`
- DynamoDB Local: `http://localhost:8001`

### Step 2: Install Python Dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Seed OpenSearch & DynamoDB (Run Once)
```bash
# Ingest nutrition CSV, schemes, articles, and medical Q&A into OpenSearch
python opensearch/ingest.py

# Create DynamoDB tables and seed demo patients, ANC visits, and nutrition logs
python -m dynamodb.seed
```

### Step 4: Run the Server
```bash
python main.py
```
Server runs on `http://localhost:8000`.

### Step 5: Connect React Native Mobile App
1. Run `ipconfig` on Windows to find your IPv4 Address (e.g. `192.168.1.50`).
2. In `maa-app/.env`, set:
   ```env
   EXPO_PUBLIC_STRANDS_AGENT_URL=http://192.168.1.50:8000
   ```
3. Start or reload your Expo app.

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | `GET` | Health check returning status of Strands, OpenSearch, Cedar, DynamoDB, and Firecracker |
| `/chat` | `POST` | Main AI chat endpoint (role-checked by Cedar, grounded by OpenSearch RAG & DynamoDB) |
| `/permissions/{role}` | `GET` | Returns Cedar-authorized capabilities for `Mother`, `ASHA`, or `Doctor` |
| `/patients/{user_id}` | `GET` | Retrieve patient profile from DynamoDB Local |
| `/patients/{user_id}/visits` | `GET` | Retrieve ANC checkup visits from DynamoDB Local |
| `/patients/{user_id}/vitals` | `POST` | Log new patient vitals into DynamoDB Local |
| `/sandbox/status` | `GET` | Firecracker microVM engine status, memory boundary, and boot metrics |
| `/sandbox/clinical-triage` | `POST` | Execute isolated high-risk obstetric triage inside Firecracker microVM |
| `/sandbox/redact-phi` | `POST` | Strip sensitive identifiers (Aadhaar, Phone) inside microVM sandbox |
| `/session/{session_id}` | `DELETE` | Clear conversation history |

---

## 🔐 Sensitive AI Processing (AWS Firecracker)

Maternal health records contain Protected Health Information (PHI) and critical clinical emergency conditions.
Janani Setu leverages **AWS Firecracker microVMs**:
- **Isolated Execution**: High-risk symptom calculations (preeclampsia, convulsions, hemorrhage) run in an isolated microVM sandbox with dedicated vCPU and 128 MiB memory boundaries.
- **Data Protection**: Patient identifiers (Aadhaar, phone, MCP IDs) are scrubbed inside the microVM sandbox before prompt construction.
- **Ephemeral Storage**: All temporary files and scratch memory inside the microVM are destroyed upon task termination.
