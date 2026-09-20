# 🤱 Janani Setu × Amazon Web Services (AWS) ☁️
### *Offline-First, Multilingual Maternal Healthcare & Smart Triage Platform Powered by AWS Ecosystem*

[![AWS Strands](https://img.shields.io/badge/AWS-Strands%20Agents%20SDK-8B5CF6?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Amazon OpenSearch](https://img.shields.io/badge/Amazon-OpenSearch%20(RAG)-0284C7?style=for-the-badge&logo=opensearch&logoColor=white)](https://opensearch.org/)
[![AWS Cedar](https://img.shields.io/badge/AWS-Cedar%20Auth%20Engine-10B981?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://www.cedarpolicy.com/)
[![Amazon DynamoDB](https://img.shields.io/badge/Amazon-DynamoDB-4F46E5?style=for-the-badge&logo=amazon-dynamodb&logoColor=white)](https://aws.amazon.com/dynamodb/)
[![AWS Firecracker](https://img.shields.io/badge/AWS-Firecracker%20MicroVM-E11D48?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://firecracker-microvm.github.io/)
[![Amazon SQS](https://img.shields.io/badge/Amazon-SQS%20(FIFO)-FF9900?style=for-the-badge&logo=amazon-sqs&logoColor=white)](https://aws.amazon.com/sqs/)
[![Amazon Bedrock](https://img.shields.io/badge/Amazon-Bedrock%20(Claude%203.5)-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/bedrock/)
[![Local Development](https://img.shields.io/badge/100%25-Local%20Demonstrable%20(Zero%20Cost)-059669?style=for-the-badge&logo=docker&logoColor=white)](#-quick-start--local-aws-stack)

---

## 📌 Executive Summary

**Janani Setu** (*"Bridge of Motherhood"*) is an enterprise-grade, offline-first maternal healthcare coordination and triage platform designed specifically for underserved rural communities in India. 

Every year, India accounts for approximately **10.3% of global maternal deaths**. Rural mothers frequently suffer from delayed detection of life-threatening complications (e.g., preeclampsia, severe anemia, gestational hypertension) due to geographical isolation, language barriers, low health literacy, and manual paper-heavy overburden on frontline **ASHA (Accredited Social Health Activist)** workers.

In collaboration with **Amazon Web Services (AWS)** technologies, Janani Setu transforms rural maternal healthcare by integrating a **tri-party smart triage system** connecting **Rural Mothers**, **ASHA Workers**, and **Government Hospital Doctors** through resilient cloud infrastructure, agentic AI, sub-millisecond hardware sandboxing, and zero-loss emergency pipelines.

---

## 🏛️ The Janani Setu × AWS Architectural Synergy

Janani Setu integrates **6 core AWS ecosystem technologies**, architected to operate with **dual capability**:
1. **100% Free Local Emulation** for edge nodes, development, and offline demonstrations (via DynamoDB Local, OpenSearch container, LocalStack, and Ollama).
2. **Seamless Cloud Switch** to production-grade managed AWS services with zero code changes (simply flipping `.env` configuration flags).

```
 ┌────────────────────────────────────────────────────────────────────────────────┐
 │                          JANANI SETU CLIENT INTERFACES                         │
 ├─────────────────────────┬──────────────────────────┬───────────────────────────┤
 │    👩‍👧 Rural Mother     │     🩺 ASHA Worker       │    👨‍⚕️ Hospital Doctor    │
 │ React Native (Maa App)  │   Risk Radar Dashboard   │  Emergency Referral Desk  │
 │ Voice / Hindi / Vitals  │  ANC Checkup & Triage    │  Prescriptions & PHI View │
 └────────────┬────────────┴─────────────┬────────────┴─────────────┬─────────────┘
              │                          │                          │
              ▼                          ▼                          ▼
 ┌────────────────────────────────────────────────────────────────────────────────┐
 │                      AWS CEDAR AUTHORIZATION ENGINE                            │
 │                      (Amazon Verified Permissions)                             │
 │   • Mathematical RBAC / ABAC Role Enforcer (Mother vs. ASHA vs. Doctor)       │
 │   • Prevents Unauthorized PHI Access & Guarantees Medical Record Privacy       │
 └───────────────────────────────────────┬────────────────────────────────────────┘
                                         │  (cedar_permit)
                                         ▼
 ┌────────────────────────────────────────────────────────────────────────────────┐
 │                 FASTAPI CENTRAL BRAIN + AWS STRANDS AGENTS SDK                 │
 │            Autonomous Clinical Conductor with 12 Indian Languages              │
 ├────────────────────────────────────────────────────────────────────────────────┤
 │   • Evaluates User Intent & Clinical Danger Signs (Empathetic ASHA Persona)    │
 │   • Dynamically orchestrates specialized tool calls across AWS services        │
 └───────┬──────────────────────────┬─────────────────────────────┬───────────────┘
         │                          │                             │
         ▼                          ▼                             ▼
┌──────────────────┐      ┌──────────────────┐      ┌───────────────────────────┐
│ 🔎 Amazon        │      │ ⚡ Amazon         │      │ 🔐 AWS Firecracker        │
│    OpenSearch    │      │    DynamoDB      │      │    MicroVM Sandbox        │
├──────────────────┤      ├──────────────────┤      ├───────────────────────────┤
│ • 1,014 Indian   │      │ • JananiPatients │      │ • Sub-5ms isolated boot   │
│   Nutrition Foods│      │   (Real-time BP, │      │ • Preeclampsia & High-    │
│ • 120 Trimester  │      │   Glucose, Risk) │      │   Risk Obstetric Triage   │
│   Health Articles│      │ • JananiVisits   │      │ • Automatic PHI Redaction │
│ • Welfare RAG    │      │   (ANC 1-4 Logs) │      │   (Aadhaar, Phone, MCP)   │
│   (PMMVY, JSY)   │      │ • Daily Diet Logs│      │ • Contraindication Screen │
└──────────────────┘      └──────────────────┘      └─────────────┬─────────────┘
                                                                  │
                                      [CRITICAL EMERGENCY / SOS]  │
                                                                  ▼
                                                    ┌───────────────────────────┐
                                                    │ 🚨 Amazon SQS (FIFO)      │
                                                    ├───────────────────────────┤
                                                    │ • Zero-loss emergency bus │
                                                    │ • Instant SMS & Doctor Alert│
                                                    │ • Auto-dispatch to 108 Amb│
                                                    └───────────────────────────┘
```

---

## ⚡ The 6 Core AWS Architecture Pillars

### 🤖 1. AWS Strands Agents SDK — Intelligent Clinical Conductor
* **Role**: Orchestrates natural-language conversations, tool invocation, and multi-turn clinical triage.
* **Empathetic ASHA Persona**: Tuned with a warm, caring frontline worker persona (*"Janani"*), capable of interacting naturally with low-literacy mothers.
* **12 Indian Regional Languages**: Supports Hindi, Hinglish, Bengali, Marathi, Telugu, Tamil, Gujarati, Punjabi, Kannada, Odia, Malayalam, and Assamese.
* **Autonomous Decisioning**: Rather than relying on simple static prompts, Strands autonomously decides when to query DynamoDB for historical vitals, search OpenSearch for clinical facts, or trigger Firecracker for emergency obstetric sandboxing.
* **Code Reference**: [`janani_agent_server/agent.py`](file:///c:/Users/iqras/Downloads/jananisetuAWS/jananisetu2.0/mini-project-sem6/janani_agent_server/agent.py)

---

### 🔎 2. Amazon OpenSearch Service — Clinical RAG & Regional Nutrition Engine
* **Role**: Eliminates Large Language Model hallucinations by grounding all clinical and dietary advice in verified medical datasets.
* **Indexed Knowledge Bases**:
  * **1,014 Indian Regional Foods**: Accurate micro and macronutrients (Calories, Protein, Iron, Calcium, Folate) for everyday Indian dishes (e.g., *Palak Dal, Ragi Mudde, Khichdi, Sattu*).
  * **120 Trimester Articles**: Safe physical activity, fetal milestones, and danger symptoms across trimesters 1, 2, and 3.
  * **Government Welfare Schemes (RAG)**: Real-time eligibility logic for **Pradhan Mantri Matru Vandana Yojana (PMMVY)** (₹6,000 direct benefit) and **Janani Suraksha Yojana (JSY)** (₹1,400 institutional delivery assistance).
  * **Bilingual Medical Q&A**: Verified obstetric clinical protocols in Hindi & English.
* **Code Reference**: [`janani_agent_server/opensearch/client.py`](file:///c:/Users/iqras/Downloads/jananisetuAWS/jananisetu2.0/mini-project-sem6/janani_agent_server/opensearch/client.py), [`janani_agent_server/opensearch/ingest.py`](file:///c:/Users/iqras/Downloads/jananisetuAWS/jananisetu2.0/mini-project-sem6/janani_agent_server/opensearch/ingest.py)

---

### 🛡️ 3. AWS Cedar Authorization Engine — Zero-Trust Tri-Party Privacy
* **Role**: Enforces mathematical, deterministic role-based and attribute-based access control (RBAC/ABAC) via Amazon Verified Permissions principles.
* **Strict Role Segregation**:
  | Role | Authorized Capabilities | Forbidden Actions |
  | :--- | :--- | :--- |
  | 👩‍👧 **Mother** | Access own vitals, chat with AI, view diet logs, trigger SOS | Accessing records of any other village mother |
  | 🩺 **ASHA Worker** | View assigned village mothers, log ANC visits, review triage status | Modifying or overriding doctor prescriptions |
  | 👨‍⚕️ **Doctor** | Full clinical diagnostic read/write, triage escalation, prescribing medications | Prohibited from unauthorized data exfiltration |
* **Code Reference**: [`janani_agent_server/cedar_auth.py`](file:///c:/Users/iqras/Downloads/jananisetuAWS/jananisetu2.0/mini-project-sem6/janani_agent_server/cedar_auth.py)

---

### ⚡ 4. Amazon DynamoDB — Serverless Longitudinal ANC Datastore
* **Role**: Ultra-fast, highly scalable NoSQL database storing longitudinal maternal records, vitals trends, and Antenatal Care (ANC) checkups.
* **Data Model**:
  * `JananiPatients`: Partition Key `user_id`. Tracks real-time systolic/diastolic blood pressure, blood glucose, gestational age in weeks, risk classification (`LOW`, `HIGH`, `CRITICAL`), and assigned ASHA ID.
  * `JananiVisits`: Composite Key (`user_id` + `visit_id`). Stores chronological logs across **ANC-1, ANC-2, ANC-3, and ANC-4** checkups.
  * `JananiNutritionLogs`: Daily meal history with iron, folate, and caloric adherence monitoring.
* **Code Reference**: [`janani_agent_server/dynamodb/client.py`](file:///c:/Users/iqras/Downloads/jananisetuAWS/jananisetu2.0/mini-project-sem6/janani_agent_server/dynamodb/client.py)

---

### 🔐 5. AWS Firecracker MicroVM — Hardware-Isolated Sandboxing & PHI Redaction
* **Role**: Runs sensitive clinical calculations inside lightweight, hardware-isolated microVMs with sub-5ms boot times and strict memory boundaries.
* **Obstetric Emergency Triage**:
  * Evaluates multi-factor **Preeclampsia Triad** (Systolic BP ≥ 140 or Diastolic BP ≥ 90 + Severe Headache + Pedal Edema).
  * Classifies high-risk conditions into clinical color-codes: **GREEN (Normal)**, **AMBER (Moderate Risk)**, and **RED (Obstetric Emergency)**.
  * Screens contraindications (e.g., flagging harmful NSAIDs in late-stage pregnancy).
* **Protected Health Information (PHI) Sanitization**:
  * Scrubbing Indian 12-digit Aadhaar numbers, phone numbers, and Mother & Child Protection (MCP) card numbers inside the microVM sandbox before payload dispatch.
  * Ephemeral storage: All scratch files and RAM allocations are shredded upon task completion.
* **Code Reference**: [`janani_agent_server/firecracker/sandbox.py`](file:///c:/Users/iqras/Downloads/jananisetuAWS/jananisetu2.0/mini-project-sem6/janani_agent_server/firecracker/sandbox.py)

---

### 🚨 6. Amazon SQS (FIFO) — Zero-Loss Emergency Alert Pipeline
* **Role**: First-In, First-Out messaging queue (`janani-high-risk-sos.fifo`) guaranteeing deduplicated, reliable emergency alert dispatch.
* **Workflow**:
  * Mother taps SOS or Firecracker emits a **RED Alert**.
  * SQS enqueues the emergency payload with message group ID preserving chronological order.
  * Consumer initiates:
    1. Instant SMS and push notification to the assigned ASHA worker and primary healthcare doctor.
    2. Automated referral ticket generation for the nearest district hospital.
    3. Emergency dispatch webhook ready for state ambulance integration (108 Emergency Services).
* **Code Reference**: [`janani_agent_server/sqs/queue.py`](file:///c:/Users/iqras/Downloads/jananisetuAWS/jananisetu2.0/mini-project-sem6/janani_agent_server/sqs/queue.py)

---

## 🌟 Key Functional Capabilities

| Feature | Description | Target Beneficiary |
| :--- | :--- | :--- |
| **🎙️ Multilingual Voice AI** | Conversational voice interface in 12 Indian languages for low-literacy rural mothers. | Rural Mothers |
| **📷 Computer Vision Screening** | On-device CLAHE image enhancement and computer vision for ankle swelling (pedal edema) detection. | Rural Mothers & ASHA |
| **📊 Smart ASHA Workflows** | Automated patient prioritization queue replacing manual paper registers; smart visit scheduling. | Frontline ASHA Workers |
| **🚨 Smart Clinical Triage** | Automated categorization into Low, High, and Critical triage groups with real-time escalation. | Government Doctors |
| **🥗 AI Nutrition Counseling** | Grounded regional diet recommendations (e.g. Iron & Calcium rich foods for anemia prevention). | Rural Mothers |
| **📡 Offline-First Sync** | Local SQLite and client-side cache automatically synchronizes with DynamoDB when network is available. | Rural Clinics / Sub-Centres |

---

## 📂 Repository Structure

```
jananisetuAWS/
├── README.md                                  # Top-level workspace documentation
└── jananisetu2.0/
    └── mini-project-sem6/
        ├── README.md                          # Project documentation (Janani Setu X AWS)
        ├── janani-aws-architecture.html       # Interactive Standalone Architecture Visualizer
        ├── janani-aws-web/                    # Interactive React + Vite AWS Dashboard
        │   ├── src/
        │   │   ├── App.jsx                    # Comprehensive AWS 6-Pillar & Simulation UI
        │   │   ├── App.css                    # Modern glassmorphic styling
        │   │   └── main.jsx
        │   └── package.json
        ├── janani_agent_server/               # FastAPI Backend & AWS Cloud Emulation Layer
        │   ├── agent.py                       # AWS Strands Agents SDK implementation
        │   ├── cedar_auth.py                  # AWS Cedar Role-Based Access Engine
        │   ├── main.py                        # REST API routing & endpoints
        │   ├── docker-compose.yml             # OpenSearch + DynamoDB Local orchestration
        │   ├── requirements.txt               # Python backend dependencies
        │   ├── dynamodb/                      # DynamoDB schema, seeds, & client
        │   │   ├── client.py
        │   │   └── seed.py
        │   ├── firecracker/                   # AWS Firecracker microVM sandboxing
        │   │   ├── firecracker-config.json    # vCPU, memory, kernel & drive config
        │   │   └── sandbox.py                 # Triage logic & PHI redaction
        │   ├── opensearch/                    # OpenSearch client, seeders, & RAG
        │   │   ├── client.py
        │   │   └── ingest.py                  # 1,014 foods, articles, schemes
        │   └── sqs/                           # Amazon SQS FIFO Emergency queue
        │       └── queue.py
        ├── maa-app/                           # React Native / Expo Mobile Application
        │   ├── App.js                         # Mobile client with voice, vitals, SOS
        │   └── package.json
        └── risk-radar/                        # ASHA Worker Web Portal & ML Services
            ├── frontend/                      # Priority queue & patient tracking
            ├── backend/                       # ASHA coordination APIs
            └── ml-service/                    # XGBoost & LSTM risk prediction models
```

---

## 🚀 Quick Start — Run the Complete AWS Stack Locally (Zero Cost)

You can run and test the complete Janani Setu AWS architecture on your local machine with **zero cloud cost and without an AWS credit card**.

### Prerequisites
- **Docker Desktop** installed and running
- **Python 3.10+**
- **Node.js 18+** & `npm`

---

### Step 1: Launch Local AWS Services (OpenSearch + DynamoDB Local)

```bash
cd jananisetu2.0/mini-project-sem6/janani_agent_server
docker-compose up -d
```
Verify the services are live:
* **Amazon OpenSearch Local**: [http://localhost:9200](http://localhost:9200)
* **OpenSearch Dashboards**: [http://localhost:5601](http://localhost:5601)
* **Amazon DynamoDB Local**: [http://localhost:8001](http://localhost:8001)

---

### Step 2: Install Python Dependencies & Seed Databases

```bash
# Set up Python virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS: source venv/bin/activate

pip install -r requirements.txt

# Ingest 1,014 Indian nutrition records, welfare schemes, and articles into OpenSearch
python opensearch/ingest.py

# Create DynamoDB tables and populate sample patient vitals and ANC visits
python -m dynamodb.seed
```

---

### Step 3: Start the FastAPI AI Agent Server

```bash
python main.py
```
The central agent server will start at **`http://localhost:8000`**.
* Interactive API Documentation (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
* Health Status Endpoint: [http://localhost:8000/health](http://localhost:8000/health)

---

### Step 4: Run the Interactive AWS Architecture Web Dashboard

In a new terminal window:
```bash
cd jananisetu2.0/mini-project-sem6/janani-aws-web
npm install
npm run dev
```
Open **`http://localhost:5173`** in your browser to explore:
* Live interactive simulations of all **6 AWS services**.
* Interactive Cedar permission evaluator (switch between Mother, ASHA, and Doctor roles).
* OpenSearch nutrition semantic search tester.
* Firecracker microVM isolated preeclampsia triage engine demo.

---

### Step 5: (Optional) Switch to Production AWS Cloud

To point the backend to production AWS services rather than local containers, edit `janani_agent_server/.env`:

```env
# Switch LLM from local Ollama to Amazon Bedrock
MODEL_PROVIDER=bedrock
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=us.anthropic.claude-3-5-sonnet-20241022-v2:0

# Switch DynamoDB to live AWS
USE_AWS_DYNAMODB=true

# Switch SQS to live AWS SQS
USE_LOCALSTACK=false
SQS_QUEUE_NAME=janani-high-risk-sos.fifo
```

---

## 📡 Key API Endpoints

| Endpoint | Method | AWS Service | Description |
| :--- | :---: | :---: | :--- |
| `/health` | `GET` | All | Status of Strands Agent, OpenSearch, Cedar, DynamoDB, & Firecracker |
| `/chat` | `POST` | AWS Strands + OpenSearch | Main conversational endpoint (Cedar role-protected, grounded by RAG) |
| `/permissions/{role}` | `GET` | AWS Cedar | Returns RBAC capabilities and restrictions for `Mother`, `ASHA`, or `Doctor` |
| `/patients/{user_id}` | `GET` | Amazon DynamoDB | Retrieves patient vitals, gestational age, and assigned ASHA |
| `/patients/{user_id}/visits` | `GET` | Amazon DynamoDB | Retrieves longitudinal ANC 1–4 checkup history |
| `/patients/{user_id}/vitals` | `POST` | Amazon DynamoDB | Logs new systolic/diastolic BP, glucose, and symptoms |
| `/sandbox/status` | `GET` | AWS Firecracker | Returns microVM hypervisor state, memory ceiling, and boot latency |
| `/sandbox/clinical-triage` | `POST` | AWS Firecracker | Executes isolated preeclampsia calculation and emergency risk grading |
| `/sandbox/redact-phi` | `POST` | AWS Firecracker | Scrubs Aadhaar, phone numbers, and MCP IDs inside microVM memory |
| `/sos/emergency-alert` | `POST` | Amazon SQS | Dispatches zero-loss panic alerts and auto-triggers ambulance webhook |

---

## 🎯 Societal Impact & Alignment with UN SDGs

Janani Setu directly aligns with the **United Nations Sustainable Development Goals (SDGs)**:

* 🎯 **SDG 3: Good Health and Well-Being**
  * Target 3.1: Reduce the global maternal mortality ratio to less than 70 per 100,000 live births.
  * Target 3.2: End preventable deaths of newborns and children under 5 years of age.
* 🎯 **SDG 5: Gender Equality**
  * Empowering rural women through accessible, voice-first digital health tools in their native mother tongues.
* 🎯 **SDG 10: Reduced Inequalities**
  * Equalizing healthcare access between well-equipped urban hospitals and remote rural villages with minimal connectivity.

---

## 👥 Contributors & Collaboration

Developed with passion to bring cutting-edge cloud engineering and artificial intelligence to the most vulnerable frontline healthcare workflows.

**Janani Setu × Amazon Web Services**  
*Cloud Infrastructure • Agentic AI • Hardware Sandboxing • Built for Bharat 🇮🇳*
