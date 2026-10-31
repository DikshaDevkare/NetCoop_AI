# NETCOOP AI — Multi-Agent Network Fault Diagnosis & Interoperability Platform

> **Final-Round Hackathon Flagship Project**  
> Futuristic 3D Network Command Centre • Collaborative Multi-Agent AI Engine • Four Genuinely Trained Machine Learning Models • Open Standard Agent Interoperability Protocol (RFC-compliant JSON Schema)

---

## 1. System Architecture Overview

NetCoop AI automates campus network telemetry investigation across distributed network infrastructure (switches, edge routers, wireless access points, and core services).

```
                      ┌────────────────────────────────────────┐
                      │          Campus Network Telemetry      │
                      │   (PCAP, CSV, NetFlow, SNMP, Telemetry)│
                      └───────────────────┬────────────────────┘
                                          │ Ingestion
                                          ▼
                      ┌────────────────────────────────────────┐
                      │    Schema Validation & Normalization   │
                      │  (Canonical Units: ms, %, drops, Mbps) │
                      └───────────────────┬────────────────────┘
                                          │
                  ┌───────────────────────┴────────────────────────┐
                  ▼                                                ▼
     ┌────────────────────────┐                       ┌────────────────────────┐
     │ 4 Trained ML Models    │                       │  Chronological Analysis│
     │ 1. Isolation Forest    │                       │  • Rolling averages    │
     │ 2. XGBoost Classifier  │                       │  • Rate of change      │
     │ 3. Random Forest Infra │                       │  • Volatility & trends │
     │ 4. Gradient Boosting   │                       │  • Recovery detection  │
     └────────────┬───────────┘                       └────────────┬───────────┘
                  │                                                │
                  └───────────────────────┬────────────────────────┘
                                          │ Inferred States
                                          ▼
                      ┌────────────────────────────────────────┐
                      │    Central Orchestration Bus           │
                      │    (NetCoop Agent Protocol v1.0)       │
                      └───────┬───────────┬────────────┬───────┘
                              │           │            │
            ┌─────────────────┴───┐       │       ┌────┴────────────────┐
            ▼                     ▼       ▼       ▼                     ▼
    ┌───────────────┐     ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌──────────────┐
    │  Performance  │     │  Infra    │ │ Connect │ │ Fault   │ │  Recommend   │
    │  Agent        │     │  Health   │ │ Agent   │ │ Correl. │ │  & Reporting │
    │  (Latency,    │     │  (CPU,    │ │ (DNS,   │ │ (Fusion │ │  (Playbooks, │
    │   Loss, Jitter│     │   Mem,    │ │  DHCP,  │ │  & Conf-│ │   Actions,   │
    │   Queue Drops)│     │   Errors) │ │  Wi-Fi) │ │  lict)  │ │   Evidence)  │
    └───────┬───────┘     └─────┬─────┘ └───┬─────┘ └────┬────┘ └──────┬───────┘
            │                   │           │            │             │
            └───────────────────┴─────┬─────┴────────────┘             │
                                      │ Correlated Finding             ▼
                                      └────────────────────────► Comprehensive
                                                                 Report & Actions
```

---

## 2. Seven Core Pages (Matching Visual Specification)

The frontend features a cinematic 3D futuristic theme using deep space navy (`#070711`), neon purple (`#A855F7`), electric blue (`#438BFF`), bright orange (`#FF781F`), and emerald green (`#20E88A`).

1. **Dashboard / Network Command Centre (`/dashboard`)**:
   - Live network health gauge (93%), AI agents online counter, active device metrics, open incident alerts.
   - Interactive 3D network topology platform with central degraded Branch Router, Core Switch, and Access Points.
   - Live telemetry sparklines for latency, packet loss, bandwidth, and CPU usage.

2. **New Diagnosis / Investigation Setup (`/new-diagnosis`)**:
   - 4-step investigation workflow (Scenario, Telemetry, Validate, Run).
   - 6 selectable diagnostic fault scenarios: Network Congestion, Link/Interface Failure, DNS/DHCP Failure, Device Overload, Wi-Fi Signal Issue, Custom Scenario.
   - Drag & drop telemetry upload with automated schema compatibility validation checklist.

3. **Incident Details / Network Investigation (`/incidents/:id`)**:
   - Investigation topology showing affected nodes (`Building A (Affected)` in crimson, `Core B`, `Building B (Healthy)`, `Branch C (Degraded)`).
   - Device inspection HUD (`SWI-03 (Building A)`): CPU (78%), Memory (64%), Interface Errors (126), Queue Drops (34), Link Utilization (92%).

4. **Agent Monitor / Multi-Agent Orchestration (`/agent-monitor`)**:
   - Center glowing Orchestrator with 5 surrounding connected agents in radial laser mesh.
   - Live execution timeline tracking agent milestones.
   - Live agent message terminal with JSON payload inspector.

5. **Diagnosis Report / Evidence & Insights (`/diagnosis-report/:id`)**:
   - Root cause identification: *Interface congestion on SW-03*.
   - Animated circular Confidence Gauge (87% confidence).
   - Evidence Correlation graph mapping high bandwidth (0.82), latency (0.76), queue drops (0.71), correlated traffic (0.81), and interface errors (0.64).
   - Actionable remediation playbook and Export JSON / PDF capabilities.

6. **Incident History (`/incident-history`)**:
   - Filterable, searchable incident dashboard with severity badges and status.
   - Incident trend area chart (Last 30 Days) and Root Cause Distribution donut chart.

7. **Interoperability Lab (`/interoperability-lab`)**:
   - Live protocol playground to test agent message schema compliance.
   - Validates required fields, sender/receiver roles, timestamp format, and canonical metric unit conversion.
   - Real-time message exchange logs and simulated agent handshake acknowledgments.

---

## 3. Four Genuinely Trained Machine Learning Models

All 4 models were trained using reproducible multi-incident synthetic datasets (70% train, 15% validation, 15% test split strictly by incident id to prevent data leakage).

| Model | Algorithm | Primary Task | Test Metrics |
|---|---|---|---|
| **Model 1** | Isolation Forest | Multi-metric network anomaly detection | Precision: 0.99+, Recall: 0.42, Accuracy: 73.9% |
| **Model 2** | XGBoost Classifier | 7-class network fault classification | Weighted F1: 1.00, Accuracy: 100% (synthetic) |
| **Model 3** | Random Forest Classifier | Infrastructure component state classification | Weighted F1: 1.00, Accuracy: 100% (synthetic) |
| **Model 4** | Gradient Boosting Classifier | Campus network tri-state health classification | Weighted F1: 1.00, Accuracy: 100% (synthetic) |

> **Honesty & Integrity Statement**: While evaluation scores on synthetic simulation datasets achieve near-perfect classification due to clear mathematical parameter boundaries, real-world campus telemetry exhibits noise, multi-path routing jitter, and partial monitoring coverage. The platform explicitly labels simulated metrics.

---

## 4. Five Specialized Diagnostic Agents

1. **Performance Agent**: Evaluates transport performance (latency, jitter, packet loss, bandwidth saturation, queue drops).
2. **Infrastructure Health Agent**: Analyzes physical equipment state (control-plane CPU, memory pressure, interface CRC errors, hardware drops).
3. **Connectivity Analysis Agent**: Investigates name resolution, DHCP leasing, gateway reachability, and 802.11 RF signal metrics (strictly ensures wired devices are never falsely flagged for missing Wi-Fi RSSI).
4. **Fault Correlation Agent**: Central intelligence fusion module. Compares temporal trends, ML probabilities, and agent findings to pinpoint root cause while preserving alternative hypotheses and reducing confidence if evidence conflicts.
5. **Recommendation & Reporting Agent**: Compiles explainable incident reports with structured JSON output, remediation playbooks, and operational limitations.

---

## 5. Agent Interoperability Protocol (JSON Schema)

Every inter-agent communication complies with the NetCoop Protocol v1.0 standard:

```json
{
  "message_id": "MSG-7042",
  "incident_id": "INC-1024",
  "sender": "performance_agent",
  "receiver": "fault_correlation_agent",
  "message_type": "diagnostic_finding",
  "schema_version": "1.0",
  "timestamp": "2026-11-01T10:30:00Z",
  "payload": {
    "finding": "high_network_latency",
    "severity": "high",
    "metric": "latency_ms",
    "value": 240.0,
    "unit": "ms",
    "device_id": "SWI-03",
    "evidence": [
      "Latency exceeds configured threshold (240ms > 50ms)",
      "Elevated egress queue drops on switch interface"
    ]
  }
}
```

### Canonical Metric Normalization

| Raw Field Name | Canonical Field Name | Normalized Unit |
|---|---|---|
| `latency`, `delay`, `ping` | `latency_ms` | Milliseconds (ms) |
| `cpu`, `cpu_usage`, `cpu_utilization_pct` | `cpu_usage_pct` | Percentage (%) |
| `memory`, `mem`, `memory_utilization_pct` | `memory_usage_pct` | Percentage (%) |
| `packetLoss`, `packet_loss`, `packet_loss_pct` | `packet_loss_pct` | Percentage (%) |
| `jitter` | `jitter_ms` | Milliseconds (ms) |
| `bandwidth_utilization`, `link_utilization_pct` | `link_utilization_pct` | Percentage (%) |

---

## 6. How to Run Locally

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm

### Backend Setup & Execution
```bash
# Navigate to backend directory
cd backend

# Install Python requirements
pip install -r requirements.txt

# (Optional) Re-train all 4 ML models & seed database
python -m app.ml.training.train_all_models

# Run Backend Unit & Integration Tests
python -m tests.test_direct

# Launch FastAPI Backend Server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be live at: `http://127.0.0.1:8000/docs`

### Frontend Setup & Execution
```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite Development Server
npm run dev
```
The application will be accessible at: `http://localhost:5173`

---

## 7. REST API Endpoints Reference

| Method | Route | Description |
|---|---|---|
| `GET` | `/api/health` | Service health & model readiness status |
| `GET` | `/api/dashboard/stats` | Network health, agent count, active devices |
| `GET` | `/api/dashboard/telemetry` | Live time-series telemetry stream |
| `GET` | `/api/dashboard/topology` | 3D network topology graph nodes & edges |
| `POST` | `/api/auth/register` | Register new campus network operator |
| `POST` | `/api/auth/login` | JWT authentication and operator access token |
| `GET` | `/api/incidents` | Filterable incident history & trend statistics |
| `GET` | `/api/incidents/{id}` | Detailed incident investigation records |
| `POST` | `/api/diagnosis/run` | Execute end-to-end multi-agent diagnosis |
| `GET` | `/api/diagnosis/{id}/report` | Retrieve explainable root cause report & evidence |
| `GET` | `/api/agents/status` | Active status of the 5 diagnostic agents |
| `GET` | `/api/agents/messages/{id}` | Structured inter-agent message audit trail |
| `POST` | `/api/interoperability/validate`| Protocol validation gateway |
| `POST` | `/api/interoperability/send` | Send test message across protocol mesh |
| `GET` | `/api/models/status` | Check 4 ML model artifact status |
| `GET` | `/api/models/metrics` | Retrieve evaluation metrics & confusion matrices |

---

## 8. License & Acknowledgements
Developed for the NetCoop AI Final-Round Hackathon. Built with FastAPI, PyTorch/Scikit-Learn/XGBoost, React, TypeScript, Vite, and Tailwind CSS.
