import React, { useState } from 'react';
import { 
  HeartPulse, 
  Activity, 
  Bot, 
  Search, 
  ShieldCheck, 
  Database, 
  Cpu, 
  Network, 
  Play, 
  Server, 
  Radio, 
  Smartphone, 
  Users, 
  Stethoscope, 
  Lock, 
  FileText, 
  AlertTriangle, 
  CheckCircle2, 
  Layers,
  Heart,
  Globe,
  Settings,
  Zap,
  Sparkles,
  ArrowRight,
  AudioWaveform,
  Code2
} from 'lucide-react';

function MotherAvatar() {
  return (
    <svg width="68" height="68" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg" className="mother-svg">
      <circle cx="40" cy="40" r="38" fill="#FDF2F8" />
      {/* Hair Bun */}
      <circle cx="40" cy="22" r="16" fill="#1E293B" />
      <ellipse cx="40" cy="12" rx="7" ry="3.5" fill="#F59E0B" />
      {/* Neck */}
      <rect x="36" y="44" width="8" height="10" rx="3" fill="#FDBA74" />
      {/* Shoulders / Torso */}
      <path d="M22 66C22 55 29 50 40 50C51 50 58 55 58 66V74H22V66Z" fill="#8B5CF6" />
      <path d="M35 50L40 57L45 50" stroke="#7C3AED" strokeWidth="2" strokeLinecap="round" />
      {/* Face */}
      <circle cx="40" cy="35" r="14" fill="#FDBA74" />
      {/* Hair Bangs */}
      <path d="M27 32C30 26 35 25 40 25C45 25 50 26 53 32C49 28 45 27 40 27C35 27 31 28 27 32Z" fill="#1E293B" />
      {/* Eyes */}
      <circle cx="35.5" cy="34.5" r="1.5" fill="#1E293B" />
      <circle cx="44.5" cy="34.5" r="1.5" fill="#1E293B" />
      {/* Cheeks */}
      <circle cx="33" cy="38" r="2" fill="#F472B6" opacity="0.7" />
      <circle cx="47" cy="38" r="2" fill="#F472B6" opacity="0.7" />
      {/* Smile */}
      <path d="M37.5 39C38.5 41 41.5 41 42.5 39" stroke="#92400E" strokeWidth="1.5" strokeLinecap="round" />
      {/* Phone in hand */}
      <g transform="translate(48, 40)">
        <rect x="2" y="2" width="15" height="25" rx="3" fill="#1E293B" />
        <rect x="4" y="5" width="11" height="18" rx="1.5" fill="#60A5FA" />
        <ellipse cx="2" cy="18" rx="4" ry="5" fill="#FDBA74" />
      </g>
    </svg>
  );
}

function RobotAvatar() {
  return (
    <svg width="68" height="68" viewBox="0 0 76 76" fill="none" xmlns="http://www.w3.org/2000/svg" className="robot-svg">
      <rect width="76" height="76" rx="18" fill="#F5F3FF" />
      {/* Antenna */}
      <path d="M38 18V10" stroke="#8B5CF6" strokeWidth="3" strokeLinecap="round" />
      <circle cx="38" cy="8" r="4" fill="#F59E0B" />
      {/* Ears */}
      <rect x="11" y="26" width="5" height="15" rx="2.5" fill="#A78BFA" />
      <rect x="60" y="26" width="5" height="15" rx="2.5" fill="#A78BFA" />
      {/* Head Outer */}
      <rect x="14" y="17" width="48" height="35" rx="12" fill="#FFFFFF" stroke="#DDD6FE" strokeWidth="2" />
      {/* Screen */}
      <rect x="19" y="21" width="38" height="26" rx="8" fill="#1E1B4B" />
      {/* Eyes */}
      <ellipse cx="28" cy="33" rx="3.5" ry="4" fill="#38BDF8" />
      <ellipse cx="48" cy="33" rx="3.5" ry="4" fill="#38BDF8" />
      <circle cx="29" cy="31.5" r="1.2" fill="#FFFFFF" />
      <circle cx="49" cy="31.5" r="1.2" fill="#FFFFFF" />
      {/* Smile */}
      <path d="M35 38.5C36.5 40.5 39.5 40.5 41 38.5" stroke="#38BDF8" strokeWidth="2" strokeLinecap="round" />
      {/* Cheeks */}
      <circle cx="23.5" cy="36" r="1.8" fill="#F472B6" opacity="0.8" />
      <circle cx="52.5" cy="36" r="1.8" fill="#F472B6" opacity="0.8" />
      {/* Body */}
      <path d="M26 55C26 51 31 49 38 49C45 49 50 51 50 55V64H26V55Z" fill="#8B5CF6" />
      <circle cx="38" cy="57" r="3" fill="#38BDF8" />
    </svg>
  );
}

function OutputDocIcon() {
  return (
    <svg width="56" height="56" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg" className="output-doc-svg">
      <rect width="60" height="60" rx="16" fill="#E0F2FE" />
      <rect x="15" y="12" width="24" height="32" rx="4" fill="#FFFFFF" stroke="#0284C7" strokeWidth="2.5" />
      <line x1="20" y1="20" x2="31" y2="20" stroke="#0284C7" strokeWidth="2.5" strokeLinecap="round" />
      <line x1="20" y1="26" x2="33" y2="26" stroke="#0284C7" strokeWidth="2.5" strokeLinecap="round" />
      <line x1="20" y1="32" x2="28" y2="32" stroke="#0284C7" strokeWidth="2.5" strokeLinecap="round" />
      <g transform="translate(26, 26)">
        <rect width="20" height="16" rx="5" fill="#0284C7" />
        <path d="M3 16L0 20L7 16H3Z" fill="#0284C7" />
        <circle cx="6" cy="8" r="1.5" fill="#FFFFFF" />
        <circle cx="10" cy="8" r="1.5" fill="#FFFFFF" />
        <circle cx="14" cy="8" r="1.5" fill="#FFFFFF" />
      </g>
    </svg>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState('all');
  const [consoleOutputs, setConsoleOutputs] = useState({});
  const [cedarRole, setCedarRole] = useState('Mother');
  const [searchQuery, setSearchQuery] = useState('iron rich foods');
  const [isBootingVM, setIsBootingVM] = useState(false);

  const setOutput = (key, text) => {
    setConsoleOutputs(prev => ({ ...prev, [key]: text }));
  };

  // 1. Simulate Strands Agent
  const runStrandsSimulation = () => {
    setOutput('strands', 'Invoking AWS Strands Agent with Hindi voice query: "Mujhe chakkar aa rahe hain" (I feel dizzy)...');
    setTimeout(() => {
      setOutput('strands', JSON.stringify({
        "agent": "Janani Strands Agent v3.2 (AWS Strands Agents SDK)",
        "language_detected": "Hindi (hi)",
        "user_query": "Mujhe chakkar aa rahe hain (I feel dizzy)",
        "tool_orchestration_pipeline": [
          "1. cedar_auth: PERMIT (Mother can access AIChat)",
          "2. get_patient_health_summary(user_id='user_001') -> BP: 118/76, Week: 28",
          "3. search_health_knowledge(query='dizziness pregnancy first aid') -> 3 docs from OpenSearch",
          "4. assess_pregnancy_risk(bp_systolic=118, bp_diastolic=76) -> NORMAL"
        ],
        "synthesized_response": "नमस्ते सुनीता जी! 28वें हफ्ते में चक्कर आना कभी-कभी सामान्य होता है। आपकी बीपी (118/76) बिल्कुल सामान्य है। कृपया तुरंत बाईं करवट लेकर लेट जाएं और एक गिलास नींबू पानी या ओआरएस पिएं। यदि अचानक सिरदर्द या आंखों के आगे अंधेरा छाए, तो तुरंत अपनी आशा दीदी (मीना देवी) को बताएं।",
        "audio_tts_status": "Ready for Indian regional speech synthesis",
        "model_backend": "Ollama llama3.2 (Local Dev) / Claude 3.5 Sonnet (Bedrock Cloud)"
      }, null, 2));
    }, 500);
  };

  // 2. Simulate OpenSearch RAG
  const runOpenSearchSimulation = () => {
    setOutput('opensearch', `Searching OpenSearch cluster :9200 (index: janani-nutrition, query: "${searchQuery}")...`);
    setTimeout(() => {
      setOutput('opensearch', JSON.stringify({
        "cluster": "janani-opensearch:9200",
        "index_queried": "janani-nutrition + janani-medical",
        "search_term": searchQuery,
        "bm25_top_hits": [
          {
            "dish_name": "Palak Dal (Spinach Lentil Curry)",
            "calories": 142,
            "iron_mg": 4.6,
            "folate_ug": 110,
            "calcium_mg": 92,
            "relevance_score": 3.89,
            "clinical_note": "Crucial for preventing gestational anemia in 2nd & 3rd trimesters"
          },
          {
            "dish_name": "Moong Dal Cheela with Paneer",
            "calories": 210,
            "protein_g": 14.2,
            "iron_mg": 3.1,
            "calcium_mg": 180,
            "relevance_score": 3.45
          },
          {
            "dish_name": "Roasted Chana with Jaggery (Gur)",
            "calories": 240,
            "iron_mg": 5.8,
            "relevance_score": 3.28,
            "traditional_benefit": "Standard rural Anganwadi iron booster"
          }
        ],
        "rag_grounding": "LLM response strictly constrained to verified nutritional facts"
      }, null, 2));
    }, 450);
  };

  // 3. Simulate Cedar Policy Engine
  const runCedarSimulation = (role) => {
    setOutput('cedar', `Evaluating Cedar policies for role: [${role}]...`);
    setTimeout(() => {
      let evaluation = {};
      if (role === 'Mother') {
        evaluation = {
          "role": "Mother",
          "evaluated_rules": [
            { "action": "Chat (AIChat)", "decision": "cedar_permit", "rule": "permit(principal in Role::'Mother', action == Action::'Chat', resource == Resource::'AIChat')" },
            { "action": "ViewHealthSummary (OwnData)", "decision": "cedar_permit", "rule": "Can view own vitals and risk score" },
            { "action": "ViewHealthSummary (OtherPatientData)", "decision": "cedar_forbid", "reason": "FORBID: Explicit policy preventing cross-patient snooping" },
            { "action": "ModifyMedicalRecord", "decision": "cedar_forbid", "reason": "FORBID: Mother cannot alter clinical prescriptions" }
          ]
        };
      } else if (role === 'ASHA') {
        evaluation = {
          "role": "ASHA Worker",
          "evaluated_rules": [
            { "action": "Chat (AIChat)", "decision": "cedar_permit", "rule": "ASHA can chat on behalf of assigned mothers" },
            { "action": "ViewHealthSummary (AssignedPatientData)", "decision": "cedar_permit", "rule": "Can review vitals of mothers in her village" },
            { "action": "LogVitals", "decision": "cedar_permit", "rule": "Permitted to log ANC checkup measurements" },
            { "action": "ModifyMedicalRecord", "decision": "cedar_forbid", "reason": "FORBID: ASHA cannot alter doctor prescriptions or official diagnoses" }
          ]
        };
      } else {
        evaluation = {
          "role": "Doctor",
          "evaluated_rules": [
            { "action": "All Actions (Full Clinical Access)", "decision": "cedar_permit", "rule": "permit(principal in Role::'Doctor', action, resource)" },
            { "action": "ModifyMedicalRecord", "decision": "cedar_permit", "rule": "Authorized to prescribe medications and official diagnosis" }
          ]
        };
      }
      setOutput('cedar', JSON.stringify({
        "cedar_engine": "AWS Cedar Open Source Policy Engine (cedarpy v0.3.0)",
        ...evaluation
      }, null, 2));
    }, 400);
  };

  // 4. Simulate DynamoDB Local
  const runDynamoDBSimulation = () => {
    setOutput('dynamodb', 'Fetching patient record & visit history from DynamoDB Local (:8001)...');
    setTimeout(() => {
      setOutput('dynamodb', JSON.stringify({
        "table_name": "JananiPatients",
        "partition_key": "user_id = 'user_001'",
        "status": "HTTP 200 OK from DynamoDB Local",
        "patient_item": {
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
          "notes": "All vitals normal. Regular iron-folic acid intake."
        },
        "visits_table_query": {
          "table": "JananiVisits",
          "total_anc_visits_found": 3,
          "latest_visit": {
            "visit_id": "visit_001_anc3",
            "visit_type": "ANC-3",
            "pregnancy_week": 28,
            "weight_kg": 57.0,
            "recorded_by": "ASHA Meena Devi"
          }
        }
      }, null, 2));
    }, 450);
  };

  // 5. Simulate Firecracker MicroVM
  const runFirecrackerSimulation = () => {
    setIsBootingVM(true);
    setOutput('firecracker', 'Booting AWS Firecracker microVM for sensitive preeclampsia triage...');
    
    setTimeout(() => {
      setIsBootingVM(false);
      setOutput('firecracker', JSON.stringify({
        "microvm_telemetry": {
          "microvm_id": "uvm-9d41b02f",
          "technology": "AWS Firecracker microVM",
          "boot_latency_ms": 4.18,
          "execution_time_ms": 0.04,
          "total_sandbox_time_ms": 4.22,
          "memory_ceiling_mib": 128,
          "vcpu_allocated": 1,
          "jailer_confinement": "ACTIVE (UID 10001 / seccomp strict / cgroups)",
          "ephemeral_storage": "SHREDDED_ON_TERMINATION"
        },
        "isolated_workload": "preeclampsia_and_drug_safety_triage",
        "clinical_triage_result": {
          "triage_color": "RED",
          "triage_level": "CRITICAL OBSTETRIC EMERGENCY",
          "primary_recommendation": "CRITICAL: Urgent hospital review needed within 2 hours. High preeclampsia risk.",
          "clinical_flags": [
            "SEVERE PREECLAMPSIA RISK: Blood pressure (150/96) combined with persistent headache and peripheral edema."
          ],
          "vitals_evaluated": {
            "bp": "150/96 mmHg",
            "glucose": "165 mg/dL",
            "symptoms": ["headache", "swelling", "blurred_vision"]
          }
        },
        "medication_contraindication_check": {
          "flagged_drugs": [
            {
              "drug": "Ibuprofen",
              "contraindication": "CONTRAINDICATED IN 3RD TRIMESTER",
              "clinical_warning": "NSAIDs in 3rd trimester cause premature closure of ductus arteriosus."
            }
          ]
        },
        "phi_redaction": "Aadhaar and phone numbers scrubbed before host response."
      }, null, 2));
    }, 600);
  };

  // 6. Simulate Amazon SQS via LocalStack
  const runSqsSimulation = () => {
    setOutput('sqs', 'Publishing high-risk obstetric emergency to SQS FIFO queue via LocalStack (:4566)...');
    setTimeout(() => {
      setOutput('sqs', JSON.stringify({
        "sqs_queue_url": "http://localhost:4566/000000000000/janani-high-risk-sos.fifo",
        "engine": "Amazon SQS via LocalStack",
        "delivery_mode": "FIFO (Strict Ordering + Exactly-Once Delivery)",
        "message_id": "msg-9f4a8b21c43e",
        "message_deduplication_id": "dedup-user001-emergency-172666",
        "message_group_id": "user_001",
        "sequence_number": "18837492019485720192",
        "emergency_event": {
          "event_type": "HIGH_RISK_OBSTETRIC_ALERT",
          "priority": "P0_CRITICAL",
          "patient_id": "user_001",
          "mother_name": "Sunita Sharma",
          "vitals": {
            "bp": "160/100 mmHg",
            "glucose": "180 mg/dL",
            "symptoms": ["severe_headache", "blurred_vision", "epigastric_pain"]
          },
          "diagnosis_flag": "IMMINENT_PREECLAMPSIA_EMERGENCY"
        },
        "risk_processing_pipeline": [
          "1. SQS Consumer Worker dequeued message with receipt handle 'rh_8f92'",
          "2. Dispatched automated SOS SMS to ASHA Meena Devi (+91 98765 43210)",
          "3. Pushed high-priority referral alert to PHC Medical Officer console",
          "4. Spawned Firecracker microVM (uvm-9d41b02f) for isolated drug-safety validation"
        ],
        "status": "PROCESSED_SUCCESSFULLY"
      }, null, 2));
    }, 450);
  };

  return (
    <div className="container">
      
      {/* ── Slide Header Banner ── */}
      <header className="slide-header">
        <div className="header-title-box">
          <div className="header-logo-icon">
            <HeartPulse size={28} color="#E11D48" />
          </div>
          <div>
            <h1 className="header-title">
              Janani Setu – Smart Triage Connecting Rural Pregnant Women, ASHA Workers & Doctors
            </h1>
            <p className="header-subtitle">
              <Activity size={14} color="#BE123C" />
              <span>Interactive AWS Architecture & Technology Mapping</span>
            </p>
          </div>
        </div>
      </header>

      {/* ── Main Panel: Architecture Diagram & 5 AWS Service Deep-Dives ── */}
      <div className="dashboard-grid">
        <main className="main-panel">

          {/* Flow Diagram */}
          <div className="diagram-container">
            <div className="section-title-wrap">
              <h2 className="section-title">
                <Network size={20} color="#1E3A8A" />
                <span>End-to-End System Architecture Diagram</span>
              </h2>
              <span className="live-tag">
                <span className="live-dot"></span> System Active
              </span>
            </div>

            <div className="arch-flow-diagram">
              {/* Column 1: Client Interfaces */}
              <div className="flow-col">
                <div className="flow-node node-mother" onClick={() => setActiveTab('strands')}>
                  <div className="node-tag" style={{ color: '#F43F5E', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Smartphone size={12} /> Mother's App
                  </div>
                  <div className="node-title">React Native (Maa App)</div>
                  <div className="node-desc">Voice / Hindi / SOS / Daily Vitals</div>
                </div>
                <div className="flow-node node-asha" onClick={() => setActiveTab('dynamodb')}>
                  <div className="node-tag" style={{ color: '#F97316', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Users size={12} /> ASHA Portal
                  </div>
                  <div className="node-title">Risk Priority Dashboard</div>
                  <div className="node-desc">Triage list & checkup vitals logs</div>
                </div>
                <div className="flow-node node-doc" onClick={() => setActiveTab('firecracker')}>
                  <div className="node-tag" style={{ color: '#3B82F6', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Stethoscope size={12} /> Doctor's View
                  </div>
                  <div className="node-title">Clinical Review Console</div>
                  <div className="node-desc">Emergency referrals & vitals trends</div>
                </div>
              </div>

              {/* Column 2: FastAPI & AWS Services Hub */}
              <div className="flow-col">
                <div className="flow-node node-server">
                  <div className="node-tag" style={{ color: '#8B5CF6', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Server size={12} /> Central Brain (main.py)
                  </div>
                  <div className="node-title">FastAPI + AWS Strands Agents SDK</div>
                  <div className="node-desc">Autonomous tool orchestrator routing queries by role & privacy</div>
                </div>

                <div className="aws-services-hub">
                  <div className={`service-mini-card ${activeTab === 'strands' ? 'active' : ''}`} onClick={() => setActiveTab('strands')}>
                    <div className="service-icon"><Bot size={22} color="#8B5CF6" /></div>
                    <div className="service-name">Strands Agent</div>
                    <div className="service-purpose">Voice AI Orchestration</div>
                  </div>

                  <div className={`service-mini-card ${activeTab === 'opensearch' ? 'active' : ''}`} onClick={() => setActiveTab('opensearch')}>
                    <div className="service-icon"><Search size={22} color="#0284C7" /></div>
                    <div className="service-name">OpenSearch</div>
                    <div className="service-purpose">Medical Knowledge RAG</div>
                  </div>

                  <div className={`service-mini-card ${activeTab === 'cedar' ? 'active' : ''}`} onClick={() => setActiveTab('cedar')}>
                    <div className="service-icon"><ShieldCheck size={22} color="#10B981" /></div>
                    <div className="service-name">Cedar Auth</div>
                    <div className="service-purpose">Role-Based Privacy</div>
                  </div>

                  <div className={`service-mini-card ${activeTab === 'dynamodb' ? 'active' : ''}`} onClick={() => setActiveTab('dynamodb')}>
                    <div className="service-icon"><Database size={22} color="#4F46E5" /></div>
                    <div className="service-name">DynamoDB</div>
                    <div className="service-purpose">NoSQL Patient Vitals</div>
                  </div>

                  <div className={`service-mini-card ${activeTab === 'firecracker' ? 'active' : ''}`} onClick={() => setActiveTab('firecracker')}>
                    <div className="service-icon"><Cpu size={22} color="#E11D48" /></div>
                    <div className="service-name">Firecracker</div>
                    <div className="service-purpose">MicroVM Sandboxing</div>
                  </div>

                  <div className={`service-mini-card ${activeTab === 'sqs' ? 'active' : ''}`} onClick={() => setActiveTab('sqs')}>
                    <div className="service-icon"><Layers size={22} color="#F59E0B" /></div>
                    <div className="service-name">Amazon SQS</div>
                    <div className="service-purpose">SOS & Emergency Queue</div>
                  </div>
                </div>
              </div>

              {/* Column 3: Local Engine vs AWS Cloud */}
              <div className="flow-col">
                <div className="flow-node" style={{ borderLeft: '4px solid #10B981', background: '#F0FDF4' }}>
                  <div className="node-tag" style={{ color: '#15803D', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Server size={12} /> Local Dev Engine
                  </div>
                  <div className="node-title">Zero Cloud Bill</div>
                  <div className="node-desc">Ollama, OpenSearch, DynamoDB & LocalStack on laptop</div>
                </div>
                <div className="flow-node" style={{ borderLeft: '4px solid #FF9900', background: '#FFFBEB' }}>
                  <div className="node-tag" style={{ color: '#B45309', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Radio size={12} /> Production AWS Cloud
                  </div>
                  <div className="node-title">Seamless Switch</div>
                  <div className="node-desc">Bedrock, OpenSearch, Cedar, DynamoDB & Amazon SQS</div>
                </div>
              </div>
            </div>
          </div>

          {/* ── 5 Detailed AWS Service Cards ── */}
          <div className="service-deepdive-grid">

            {/* 1. AWS STRANDS AGENTS SDK */}
            {(activeTab === 'all' || activeTab === 'strands') && (
              <div className="aws-card theme-strands highlighted">
                <div className="aws-card-header">
                  <div className="aws-card-header-left">
                    <div className="aws-icon-bubble">
                      <Bot size={26} color="#FFFFFF" />
                    </div>
                    <div className="card-title-group">
                      <h3>1. AWS Strands Agents SDK</h3>
                      <p style={{ color: '#6D28D9' }}>Voice-Controlled Chatbot & Multi-Tool Orchestrator</p>
                    </div>
                  </div>
                  <div className="aws-card-header-right">
                    <span className="aws-badge-tool">
                      <AudioWaveform size={14} /> Voice Chatbot
                    </span>
                    <span className="cursive-tagline">
                      Same questions, better care <span className="heart-sym">♡</span>
                    </span>
                  </div>
                </div>

                <div className="aws-card-body strands-custom-body">
                  {/* Left Column: Context & 3 Feature Cards */}
                  <div className="body-left-content">
                    <span className="feature-tag-pill">HOW IT IS USED IN JANANI SETU</span>
                    <p className="feature-desc">
                      The <strong>AWS Strands Agent</strong> acts as the intelligent clinical conductor. Instead of just answering questions with generic LLM knowledge, it dynamically evaluates the user's intent and autonomously calls specialized tools to retrieve patient vitals, search nutrition data, verify government schemes, and trigger isolated risk models.
                    </p>

                    <div className="strands-features-stack">
                      <div className="strands-feature-card feat-pink">
                        <div className="feature-card-icon icon-pink">
                          <Heart size={18} color="#E11D48" />
                        </div>
                        <div className="feature-card-content">
                          <h4>Empathetic Persona</h4>
                          <p>Tuned as a caring older sister / trained ASHA worker (Janani).</p>
                        </div>
                      </div>

                      <div className="strands-feature-card feat-blue">
                        <div className="feature-card-icon icon-blue">
                          <Globe size={18} color="#0284C7" />
                        </div>
                        <div className="feature-card-content">
                          <h4>12 Indian Languages</h4>
                          <p>Speaks Hindi, Bengali, Marathi, Telugu, Tamil, Gujarati and Hinglish.</p>
                        </div>
                      </div>

                      <div className="strands-feature-card feat-amber">
                        <div className="feature-card-icon icon-amber">
                          <Settings size={18} color="#D97706" />
                        </div>
                        <div className="feature-card-content">
                          <h4>Autonomous Tools</h4>
                          <p>Invokes DynamoDB for vitals, OpenSearch for RAG, and Firecracker for emergency triage.</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Right Column: Visual Flow Box matching Image 2 */}
                  <div className="strands-flow-container">
                    <div className="strands-flow-row">
                      
                      {/* Step 1: Mother */}
                      <div className="strands-node-col node-mother-col">
                        <div className="mother-speech-bubble">
                          <div className="bubble-text-hindi">"Mujhe chakkar<br />aa rahe hain"</div>
                          <div className="bubble-text-en">(I feel dizzy)</div>
                          <div className="bubble-pointer"></div>
                        </div>

                        <div className="mother-avatar-box">
                          <MotherAvatar />
                        </div>

                        <div className="strands-node-badge">1</div>

                        <div className="strands-node-caption">
                          <strong>Mother speaks</strong>
                          <span className="caption-sub">"Mujhe chakkar aa rahe hain"</span>
                          <span className="caption-sub muted">(I feel dizzy)</span>
                        </div>
                      </div>

                      {/* Arrow 1 -> 2 */}
                      <div className="strands-arrow-wrap">
                        <ArrowRight size={20} color="#8B5CF6" />
                      </div>

                      {/* Step 2: Strands Agent */}
                      <div className="strands-node-col node-agent-col">
                        <div className="agent-avatar-card">
                          <div className="agent-sparkle-star">
                            <Sparkles size={14} color="#F59E0B" />
                          </div>
                          <RobotAvatar />
                        </div>

                        <div className="strands-node-badge">2</div>

                        <div className="strands-node-caption">
                          <strong>Strands Agent</strong>
                          <span className="caption-sub">checks Cedar auth</span>
                          <span className="caption-sub">& calls <code>get_patient_health_summary</code></span>
                        </div>
                      </div>

                      {/* Arrow 2 -> 3 */}
                      <div className="strands-arrow-wrap">
                        <ArrowRight size={20} color="#8B5CF6" />
                      </div>

                      {/* Step 3: Tool Stack */}
                      <div className="strands-node-col node-tools-col">
                        <div className="tools-stack-box">
                          <div className="tool-stack-item">
                            <div className="tool-square purple">
                              <Database size={15} color="#7C3AED" />
                            </div>
                            <span className="tool-title">Cedar auth</span>
                          </div>

                          <div className="tool-stack-item">
                            <div className="tool-square green">
                              <FileText size={15} color="#059669" />
                            </div>
                            <span className="tool-title mono">get_patient_health_summary</span>
                          </div>

                          <div className="tool-stack-item">
                            <div className="tool-square orange">
                              <Search size={15} color="#EA580C" />
                            </div>
                            <span className="tool-title mono">search_health_knowledge</span>
                          </div>

                          <div className="tool-stack-item">
                            <div className="tool-square red">
                              <Zap size={15} color="#E11D48" />
                            </div>
                            <span className="tool-title">Firecracker</span>
                          </div>
                        </div>
                      </div>

                      {/* Arrow 3 -> 4 */}
                      <div className="strands-arrow-wrap">
                        <ArrowRight size={20} color="#8B5CF6" />
                      </div>

                      {/* Step 4: Synthesizes Output */}
                      <div className="strands-node-col node-output-col">
                        <div className="output-card-box">
                          <OutputDocIcon />
                        </div>

                        <div className="strands-node-badge">4</div>

                        <div className="strands-node-caption">
                          <p className="output-desc-text">
                            Synthesizes clear, spoken Hindi advice grounded in clinical facts
                          </p>
                        </div>
                      </div>

                    </div>

                    {/* Bottom Autonomy Loop */}
                    <div className="strands-loop-track">
                      <div className="loop-svg-holder">
                        <svg width="100%" height="34" viewBox="0 0 600 34" preserveAspectRatio="none" fill="none">
                          <path d="M 525 2 V 18 H 75 V 2" stroke="#8B5CF6" strokeWidth="1.5" />
                          <polygon points="521,6 525,0 529,6" fill="#8B5CF6" />
                          <polygon points="71,6 75,0 79,6" fill="#8B5CF6" />
                        </svg>
                      </div>
                      <div className="loop-label-badge">
                        Agent autonomously selects the right tools
                      </div>
                    </div>
                  </div>
                </div>

                <div className="interactive-bar">
                  <div className="interactive-bar-top">
                    <span style={{ fontSize: '12px', fontWeight: '700', color: '#4B5563', display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <Code2 size={15} color="#4B5563" /> File: <code>janani_agent_server/agent.py</code>
                    </span>
                    <button className="sim-btn" onClick={runStrandsSimulation}>
                      <Play size={13} /> Simulate Live Agent Voice Query
                    </button>
                  </div>
                  {consoleOutputs['strands'] && (
                    <pre className="output-console">{consoleOutputs['strands']}</pre>
                  )}
                </div>
              </div>
            )}

            {/* 2. AMAZON OPENSEARCH SERVICE */}
            {(activeTab === 'all' || activeTab === 'opensearch') && (
              <div className="aws-card theme-opensearch highlighted">
                <div className="aws-card-header">
                  <div className="aws-card-header-left">
                    <div className="aws-icon-bubble">
                      <Search size={26} color="#FFFFFF" />
                    </div>
                    <div className="card-title-group">
                      <h3>2. Amazon OpenSearch Service</h3>
                      <p style={{ color: '#0284C7' }}>Health Knowledge RAG & Semantic Nutrition Retrieval</p>
                    </div>
                  </div>
                  <span className="aws-badge-tool">
                    <FileText size={13} /> Smart Nutrition & Schemes
                  </span>
                </div>

                <div className="aws-card-body">
                  <div className="body-left-content">
                    <span className="feature-tag-pill">HOW IT IS USED IN JANANI SETU</span>
                    <p className="feature-desc">
                      OpenSearch powers the <strong>Retrieval-Augmented Generation (RAG)</strong> knowledge repository. Large Language Models often hallucinate medical guidelines or fail on regional Indian dietary dishes. OpenSearch indexes verified clinical documents, regional Indian food recipes, and welfare programs so the agent only quotes factual, validated medical advice.
                    </p>
                    <div className="bullets-box">
                      <ul>
                        <li><strong>1,014 Indian Foods:</strong> Exact Calories, Protein, Iron, Calcium, and Folate per dish (Dal, Palak, Roti, Khichdi).</li>
                        <li><strong>120 Pregnancy Articles:</strong> Safe exercise, fetal development, and trimester guidelines.</li>
                        <li><strong>Government Schemes:</strong> Real-time eligibility for PMMVY (₹6,000 cash), JSY (₹1,400 rural), and free IFA tablets.</li>
                        <li><strong>12 Bilingual Medical Q&As:</strong> Curated emergency red-flag guidance in English & Hindi.</li>
                      </ul>
                    </div>
                  </div>

                  <div className="micro-diagram">
                    <div className="diagram-step">
                      <span className="diagram-step-num">1</span>
                      <span>User asks: <em>"What should I eat for low hemoglobin?"</em></span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step">
                      <span className="diagram-step-num">2</span>
                      <span>OpenSearch executes BM25 search across <code>janani-nutrition</code> index</span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step">
                      <span className="diagram-step-num">3</span>
                      <span>Returns top items: Palak Dal, Moong Cheela, Roasted Chana</span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step" style={{ borderColor: '#0284C7', background: '#F0F9FF' }}>
                      <span className="diagram-step-num" style={{ background: '#0284C7', color: '#fff' }}>4</span>
                      <span>Agent cites accurate iron content without guessing</span>
                    </div>
                  </div>
                </div>

                <div className="interactive-bar">
                  <div className="interactive-bar-top">
                    <span style={{ fontSize: '12px', fontWeight: '700', color: '#4B5563' }}>File: <code>janani_agent_server/opensearch/client.py</code></span>
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                      <input 
                        type="text" 
                        value={searchQuery} 
                        onChange={(e) => setSearchQuery(e.target.value)}
                        style={{ padding: '6px 10px', borderRadius: '6px', border: '1px solid #CBD5E1', fontSize: '12px' }}
                      />
                      <button className="sim-btn" onClick={runOpenSearchSimulation}>
                        <Play size={13} /> Search RAG Docs
                      </button>
                    </div>
                  </div>
                  {consoleOutputs['opensearch'] && (
                    <pre className="output-console">{consoleOutputs['opensearch']}</pre>
                  )}
                </div>
              </div>
            )}

            {/* 3. AWS CEDAR POLICY ENGINE */}
            {(activeTab === 'all' || activeTab === 'cedar') && (
              <div className="aws-card theme-cedar highlighted">
                <div className="aws-card-header">
                  <div className="aws-card-header-left">
                    <div className="aws-icon-bubble">
                      <ShieldCheck size={26} color="#FFFFFF" />
                    </div>
                    <div className="card-title-group">
                      <h3>3. AWS Cedar Authorization Engine</h3>
                      <p style={{ color: '#059669' }}>Fine-Grained Role Privacy (Mother vs ASHA vs Doctor)</p>
                    </div>
                  </div>
                  <span className="aws-badge-tool">
                    <Users size={13} /> Tri-Party Role Privacy
                  </span>
                </div>

                <div className="aws-card-body">
                  <div className="body-left-content">
                    <span className="feature-tag-pill">HOW IT IS USED IN JANANI SETU</span>
                    <p className="feature-desc">
                      Maternal data is strictly confidential. <strong>AWS Cedar</strong> enforces mathematical, fine-grained access control before every single API call or AI tool invocation. It guarantees that a pregnant mother can only see her own records, an ASHA worker can only view assigned village mothers, and doctors have write access to clinical prescriptions.
                    </p>
                    <div className="bullets-box">
                      <ul>
                        <li><strong>Mother:</strong> Can chat freely, view her own vitals, risk scores, and diet logs. <em>FORBIDDEN</em> from seeing other mothers.</li>
                        <li><strong>ASHA Worker:</strong> Can view assigned patients, log new vitals, and view risk alerts. <em>FORBIDDEN</em> from altering doctor prescriptions.</li>
                        <li><strong>Doctor:</strong> Full read and write authorization for all medical diagnostics.</li>
                      </ul>
                    </div>
                  </div>

                  <div className="micro-diagram">
                    <div className="diagram-step">
                      <span className="diagram-step-num">1</span>
                      <span>Request: <code>POST /chat</code> (role: {cedarRole})</span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step">
                      <span className="diagram-step-num">2</span>
                      <span>Cedar checks: <code>is_authorized(User, Action, Resource)</code></span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step">
                      <span className="diagram-step-num">3</span>
                      <span>Returns <strong>cedar_permit</strong> or <strong>cedar_forbid</strong></span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step" style={{ borderColor: '#10B981', background: '#ECFDF5' }}>
                      <span className="diagram-step-num" style={{ background: '#10B981', color: '#fff' }}>4</span>
                      <span>Strict data boundary maintained across village patients</span>
                    </div>
                  </div>
                </div>

                <div className="interactive-bar">
                  <div className="interactive-bar-top">
                    <span style={{ fontSize: '12px', fontWeight: '700', color: '#4B5563' }}>File: <code>janani_agent_server/cedar_auth.py</code></span>
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                      <select 
                        value={cedarRole} 
                        onChange={(e) => setCedarRole(e.target.value)}
                        style={{ padding: '6px 10px', borderRadius: '6px', border: '1px solid #CBD5E1', fontSize: '12px', fontWeight: 'bold' }}
                      >
                        <option value="Mother">Role: Mother</option>
                        <option value="ASHA">Role: ASHA Worker</option>
                        <option value="Doctor">Role: Doctor</option>
                      </select>
                      <button className="sim-btn" onClick={() => runCedarSimulation(cedarRole)}>
                        <Play size={13} /> Evaluate Cedar Policy
                      </button>
                    </div>
                  </div>
                  {consoleOutputs['cedar'] && (
                    <pre className="output-console">{consoleOutputs['cedar']}</pre>
                  )}
                </div>
              </div>
            )}

            {/* 4. AMAZON DYNAMODB */}
            {(activeTab === 'all' || activeTab === 'dynamodb') && (
              <div className="aws-card theme-dynamodb highlighted">
                <div className="aws-card-header">
                  <div className="aws-card-header-left">
                    <div className="aws-icon-bubble">
                      <Database size={26} color="#FFFFFF" />
                    </div>
                    <div className="card-title-group">
                      <h3>4. Amazon DynamoDB (Local / Cloud)</h3>
                      <p style={{ color: '#4F46E5' }}>High-Performance NoSQL Patient Health & ANC Checkup Store</p>
                    </div>
                  </div>
                  <span className="aws-badge-tool">
                    <Activity size={13} /> Mother Profile & Risk Dashboard
                  </span>
                </div>

                <div className="aws-card-body">
                  <div className="body-left-content">
                    <span className="feature-tag-pill">HOW IT IS USED IN JANANI SETU</span>
                    <p className="feature-desc">
                      Replaces bulky relational databases with a fast, serverless NoSQL datastore. DynamoDB stores longitudinal patient health records, Antenatal Care (ANC) visit checkups, blood pressure measurements, and nutrition tracking.
                    </p>
                    <div className="bullets-box">
                      <ul>
                        <li><strong>JananiPatients Table:</strong> Partition Key <code>user_id</code>. Real-time systolic/diastolic BP, blood glucose, gestational week, risk level, and assigned ASHA.</li>
                        <li><strong>JananiVisits Table:</strong> Composite Key (<code>user_id</code> + <code>visit_id</code>). Chronological tracking across ANC-1, ANC-2, ANC-3, and ANC-4 checkups.</li>
                        <li><strong>JananiNutritionLogs Table:</strong> Daily meal logs with calorie, calcium, and iron tracking.</li>
                      </ul>
                    </div>
                  </div>

                  <div className="micro-diagram">
                    <div className="diagram-step">
                      <span className="diagram-step-num">1</span>
                      <span>ASHA logs BP: 118/76 mmHg, Glucose: 98 mg/dL at Anganwadi</span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step">
                      <span className="diagram-step-num">2</span>
                      <span>Written to DynamoDB Local (<code>JananiVisits</code> + <code>JananiPatients</code>)</span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step">
                      <span className="diagram-step-num">3</span>
                      <span>DynamoDB stores composite key for longitudinal visit trends</span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step" style={{ borderColor: '#4F46E5', background: '#EEF2FF' }}>
                      <span className="diagram-step-num" style={{ background: '#4F46E5', color: '#fff' }}>4</span>
                      <span>Instantly updates ASHA Risk Priority Dashboard & Doctor Alert</span>
                    </div>
                  </div>
                </div>

                <div className="interactive-bar">
                  <div className="interactive-bar-top">
                    <span style={{ fontSize: '12px', fontWeight: '700', color: '#4B5563' }}>File: <code>janani_agent_server/dynamodb/client.py</code></span>
                    <button className="sim-btn" onClick={runDynamoDBSimulation}>
                      <Play size={13} /> Query DynamoDB Patient Record
                    </button>
                  </div>
                  {consoleOutputs['dynamodb'] && (
                    <pre className="output-console">{consoleOutputs['dynamodb']}</pre>
                  )}
                </div>
              </div>
            )}

            {/* 5. AWS FIRECRACKER MICROVM */}
            {(activeTab === 'all' || activeTab === 'firecracker') && (
              <div className="aws-card theme-firecracker highlighted">
                <div className="aws-card-header">
                  <div className="aws-card-header-left">
                    <div className="aws-icon-bubble">
                      <Cpu size={26} color="#FFFFFF" />
                    </div>
                    <div className="card-title-group">
                      <h3>5. AWS Firecracker MicroVM</h3>
                      <p style={{ color: '#E11D48' }}>Sensitive AI Processing & Hardware-Isolated Clinical Sandboxing</p>
                    </div>
                  </div>
                  <span className="aws-badge-tool">
                    <Lock size={13} /> Sensitive Triage & PHI
                  </span>
                </div>

                <div className="aws-card-body">
                  <div className="body-left-content">
                    <span className="feature-tag-pill">HOW IT IS USED IN JANANI SETU</span>
                    <p className="feature-desc">
                      Maternal emergencies (such as <strong>preeclampsia</strong>, eclamptic convulsions, and antepartum hemorrhage) involve highly sensitive Protected Health Information (PHI). AWS Firecracker runs these sensitive workloads inside lightweight, hardware-isolated microVMs with sub-5ms boot times and strict memory confinement.
                    </p>
                    <div className="bullets-box">
                      <ul>
                        <li><strong>Sub-5ms Boot Latency:</strong> Boots an isolated microVM in ~4.2 ms with dedicated vCPU and 128 MiB ceiling.</li>
                        <li><strong>Multi-Factor Obstetric Triage:</strong> Detects preeclampsia triad (BP &gt; 140/90 + headache + swelling) → Returns emergency RED triage code.</li>
                        <li><strong>PHI Redaction:</strong> Strips Indian phone numbers, 12-digit Aadhaar numbers, and MCP IDs inside the microVM before cloud dispatch.</li>
                        <li><strong>Ephemeral Storage:</strong> All memory and scratch files are securely shredded on task termination.</li>
                      </ul>
                    </div>
                  </div>

                  <div className="micro-diagram">
                    <div className="diagram-step">
                      <span className="diagram-step-num">1</span>
                      <span>Emergency Vitals: BP 150/96, severe headache, swollen feet</span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step">
                      <span className="diagram-step-num">2</span>
                      <span>Firecracker microVM boots in <strong>4.2ms</strong> with 128 MiB boundary</span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step">
                      <span className="diagram-step-num">3</span>
                      <span>Calculates Preeclampsia Risk Score + Flags NSAID Contraindications</span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step" style={{ borderColor: '#E11D48', background: '#FFF1F2' }}>
                      <span className="diagram-step-num" style={{ background: '#E11D48', color: '#fff' }}>4</span>
                      <span>Emits RED Alert: <em>Urgent hospital referral within 2 hours</em></span>
                    </div>
                  </div>
                </div>

                <div className="interactive-bar">
                  <div className="interactive-bar-top">
                    <span style={{ fontSize: '12px', fontWeight: '700', color: '#4B5563' }}>File: <code>janani_agent_server/firecracker/sandbox.py</code></span>
                    <button className="sim-btn" onClick={runFirecrackerSimulation} disabled={isBootingVM}>
                      <Play size={13} /> {isBootingVM ? 'Booting MicroVM...' : 'Boot Firecracker MicroVM & Triage'}
                    </button>
                  </div>
                  {consoleOutputs['firecracker'] && (
                    <pre className="output-console">{consoleOutputs['firecracker']}</pre>
                  )}
                </div>
              </div>
            )}

            {/* 6. AMAZON SQS (VIA LOCALSTACK) */}
            {(activeTab === 'all' || activeTab === 'sqs') && (
              <div className="aws-card theme-sqs highlighted">
                <div className="aws-card-header">
                  <div className="aws-card-header-left">
                    <div className="aws-icon-bubble">
                      <Layers size={26} color="#FFFFFF" />
                    </div>
                    <div className="card-title-group">
                      <h3>6. Amazon SQS (via LocalStack)</h3>
                      <p style={{ color: '#D97706' }}>SOS & High-Risk Case Processing Pipeline</p>
                    </div>
                  </div>
                  <span className="aws-badge-tool">
                    <Zap size={13} /> Emergency Triage Queue
                  </span>
                </div>

                <div className="aws-card-body">
                  <div className="body-left-content">
                    <span className="feature-tag-pill">HOW IT IS USED IN JANANI SETU</span>
                    <p className="feature-desc">
                      Rural mobile networks can be unreliable, but obstetric emergencies (such as eclampsia seizures, antepartum hemorrhage, or sudden maternal collapse) require a zero-failure delivery guarantee. <strong>Amazon SQS</strong> provides a fault-tolerant message queue. High-risk alerts and SOS panic triggers are buffered with guaranteed FIFO ordering, decoupling the mobile app from downstream ASHA alerts, doctor triage consoles, and hospital dispatch systems.
                    </p>
                    <div className="bullets-box" style={{ borderLeftColor: '#F59E0B', background: '#FFFDF7' }}>
                      <ul>
                        <li><strong>Proper Reliable Emergency Pipeline:</strong> Asynchronous queuing prevents dropped alerts if village cellular networks drop packets.</li>
                        <li><strong>FIFO Order & Deduplication:</strong> Exactly-once delivery prevents redundant emergency alarms during panic button clicks.</li>
                        <li><strong>LocalStack Emulation:</strong> Runs 100% offline via LocalStack on port 4566, with seamless zero-code transition to AWS cloud.</li>
                        <li><strong>Automated Emergency Cascade:</strong> Immediately dispatches SMS to the assigned ASHA worker, alerts the nearest PHC hospital, and spins up a Firecracker microVM.</li>
                      </ul>
                    </div>
                  </div>

                  <div className="micro-diagram">
                    <div className="diagram-step" style={{ borderColor: '#F87171', background: '#FEF2F2' }}>
                      <span className="diagram-step-num" style={{ background: '#EF4444', color: '#fff' }}>!</span>
                      <span><strong>HIGH RISK</strong>: Severe BP Spike / Mother Presses SOS</span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step" style={{ borderColor: '#F59E0B', background: '#FFFBEB' }}>
                      <span className="diagram-step-num" style={{ background: '#F59E0B', color: '#fff' }}>Q</span>
                      <span><strong>SQS Queue</strong>: <code>janani-high-risk-sos.fifo</code> via LocalStack (:4566)</span>
                    </div>
                    <div className="diagram-arrow">↓</div>
                    <div className="diagram-step" style={{ borderColor: '#10B981', background: '#F0FDF4' }}>
                      <span className="diagram-step-num" style={{ background: '#10B981', color: '#fff' }}>⚡</span>
                      <span><strong>Risk processing</strong>: ASHA Alert + Ambulance + Firecracker</span>
                    </div>
                  </div>
                </div>

                <div className="interactive-bar">
                  <div className="interactive-bar-top">
                    <span style={{ fontSize: '12px', fontWeight: '700', color: '#4B5563' }}>File: <code>janani_agent_server/sqs/queue.py</code></span>
                    <button className="sim-btn" onClick={runSqsSimulation} style={{ borderColor: '#F59E0B', color: '#B45309' }}>
                      <Play size={13} /> Simulate SOS & High-Risk SQS Message Pipeline
                    </button>
                  </div>
                  {consoleOutputs['sqs'] && (
                    <pre className="output-console">{consoleOutputs['sqs']}</pre>
                  )}
                </div>
              </div>
            )}

          </div>

          <footer className="footer-bar">
            Janani Setu Architecture Demonstration • 6 AWS Ecosystem Pillars • Academic & Review Presentation
          </footer>
        </main>
      </div>

    </div>
  );
}
