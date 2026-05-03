# 🏥 MediFlow AI

### Agentic AI Hospital Queue & Appointment Management System

---

## 🚀 Overview

**MediFlow AI** is an end-to-end **agentic AI-powered hospital workflow system** designed to automate real-world hospital operations.

It intelligently handles:

* Symptom understanding
* Department routing
* Urgency detection
* Doctor assignment
* Queue management
* Appointment booking
* Cancellation & rescheduling
* Patient notifications
* Analytics dashboard

Unlike traditional systems, MediFlow AI uses a **multi-agent architecture** to autonomously complete tasks end-to-end.

---

## 🎯 Key Features

### 🤖 AI-Powered Triage

* Uses LLM (Groq) to interpret patient symptoms
* Automatically assigns correct department

### 🚨 Urgency Detection

* Classifies into:

  * LOW
  * MEDIUM
  * HIGH
  * EMERGENCY
* Hybrid rule-based + AI logic

### 🩺 Smart Doctor Allocation

* Selects optimal doctor
* Balances workload across doctors

### 🎟️ Queue Management

* Real-time queue using Redis
* Generates token numbers
* Estimates waiting time

### 🔄 Auto Rescheduling

* Reuses cancelled slots
* Minimizes doctor idle time

### ❌ Appointment Cancellation

* Cancel appointments via frontend
* Updates database instantly

### 📲 Notifications

* Sends SMS via Twilio
* Includes:

  * Doctor name
  * Slot time
  * Queue token
  * Wait time

### 📊 Analytics Dashboard

* Built using Streamlit
* Displays:

  * Total patients
  * Emergency cases
  * Department load
  * Doctor utilization
  * Wait-time prediction

---

## 🧠 Architecture

```
User (Streamlit UI)
        ↓
FastAPI Backend
        ↓
LangGraph Workflow
        ↓
Agents:
  - Triage Agent
  - Urgency Agent
  - Load Balancer
  - Queue Agent
  - Rescheduler
  - Reminder Agent
        ↓
PostgreSQL Database
        ↓
Redis Queue System
        ↓
Twilio Notifications
```

---

## 🛠️ Tech Stack

* **LLM**: Groq (GPT-OSS)
* **Framework**: LangChain + LangGraph
* **Backend**: FastAPI
* **Database**: PostgreSQL
* **Queue System**: Redis
* **Frontend**: Streamlit
* **Notifications**: Twilio
* **ORM**: SQLAlchemy

---

## 📂 Project Structure

```
hospital-agent/
│
├── agents/
├── app/
├── frontend/
├── graph/
├── models/
├── tools/
├── .env
├── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/Tarunsalanke/Hospital-Appointment-Booking-Agent-using-LangGraph.git
cd Hospital-Appointment-Booking-Agent-using-LangGraph
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv .venv
.venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create `.env` file:

```
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://postgres:password@localhost/hospital_ai

TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_twilio_number
```

---

### 5️⃣ Setup PostgreSQL Database

Run:

```
CREATE DATABASE hospital_ai;
```

Then create tables:

```
CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(100),
    available_slots JSONB
);

CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_name VARCHAR(100),
    phone_number VARCHAR(20),
    symptoms TEXT,
    department VARCHAR(100),
    doctor_id INT,
    slot_time VARCHAR(50),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 6️⃣ Insert Sample Doctors

```
INSERT INTO doctors (name, department, available_slots)
VALUES
('Dr Kumar', 'Cardiology', '["10:00","11:00"]'),
('Dr Meena', 'Cardiology', '["10:30","11:30"]'),
('Dr Priya', 'Dermatology', '["12:00","2:00"]'),
('Dr Arjun', 'General', '["9:00","1:00"]');
```

---

### 7️⃣ Start Redis Server

```
redis-server
```

---

### 8️⃣ Run Backend

```
uvicorn app.main:app --reload
```

---

### 9️⃣ Run Frontend

```
streamlit run frontend/dashboard.py
```

---

## 🧪 Testing

### ✅ Normal Booking

* Enter symptoms like "fever"
* Expected: department assigned, booking confirmed

### 🚨 Emergency Case

* Enter "chest pain, breathing difficulty"
* Expected: EMERGENCY, immediate handling

### ❌ Cancellation

* Select appointment ID in UI
* Status updates to cancelled

### 📊 Dashboard

* Metrics update in real-time
* Graphs reflect live data

---

## 📸 Demo Flow

1. Enter patient details
2. AI processes symptoms
3. Appointment booked
4. Queue token generated
5. SMS notification sent
6. Dashboard updates

---

## 💡 Future Enhancements

* Voice-based AI receptionist
* Multilingual support
* ML-based wait-time prediction
* Cloud deployment
* Mobile application

---

## 🏆 Highlights

* Real-world problem solving
* Agentic AI architecture
* End-to-end automation
* Scalable system design

---

## 📄 License

For educational and demonstration purposes.

---

## 👨‍💻 Author

**Tarun S**
Final Year AIML Student

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
