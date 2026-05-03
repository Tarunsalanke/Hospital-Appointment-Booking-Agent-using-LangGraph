import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import requests
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

# ----------------- SETUP -----------------
load_dotenv()
db_url = os.getenv("DATABASE_URL")
if db_url:
    engine = create_engine(db_url)
else:
    engine = None
    st.error("DATABASE_URL is not configured. Set it in .env and restart Streamlit.")

st.set_page_config(page_title="Hospital AI Dashboard", layout="wide")
st.title("🏥 Agentic AI Hospital Operations Dashboard")

# 🔄 Auto refresh every 3 sec
# st_autorefresh(interval=3000, key="refresh")

# ----------------- BOOKING FORM -----------------
st.sidebar.title("🧾 Book Appointment")

patient_name = st.sidebar.text_input("Patient Name")
phone_number = st.sidebar.text_input("Phone Number")
symptoms = st.sidebar.text_area("Symptoms")

if st.sidebar.button("Book Appointment"):
    if patient_name and symptoms and phone_number:
        response = requests.post(
            "http://127.0.0.1:8000/book",
            json={
                "patient_name": patient_name,
                "phone_number": phone_number,
                "symptoms": symptoms
            }
        )

        if response.status_code == 200:
            st.sidebar.success("✅ Appointment Booked!")
            st.rerun()
        else:
            st.sidebar.error("❌ Failed to book")

# ----------------- LOAD DATA (SAFE QUERY) -----------------
if engine is not None:
    try:
        query = """
        SELECT appointment_id, department, status, doctor_id, slot_time, created_at
        FROM appointments
        ORDER BY appointment_id DESC
        """
        df = pd.read_sql(query, engine)
        time_col = "created_at"
    except Exception:
        # fallback if created_at doesn't exist or query fails
        try:
            query = """
            SELECT appointment_id, department, status, doctor_id, slot_time, updated_at
            FROM appointments
            ORDER BY appointment_id DESC
            """
            df = pd.read_sql(query, engine)
            time_col = "updated_at"
        except Exception as exc:
            st.error("Unable to load appointments from the database. Check DATABASE_URL and database connectivity.")
            st.error(str(exc))
            df = pd.DataFrame(columns=["appointment_id", "department", "status", "doctor_id", "slot_time", "created_at"])
            time_col = "created_at"
else:
    df = pd.DataFrame(columns=["appointment_id", "department", "status", "doctor_id", "slot_time", "created_at"])
    time_col = "created_at"

st.subheader("❌ Cancel Appointment")

if not df.empty:
    appointment_ids = df["appointment_id"].tolist()

    selected_id = st.selectbox("Select Appointment ID to Cancel", appointment_ids)

    if st.button("Cancel Appointment"):
        response = requests.post(
            "http://127.0.0.1:8000/cancel",
            params={"appointment_id": selected_id}
        )

        if response.status_code == 200:
            st.success(f"Appointment {selected_id} cancelled!")
            st.rerun()
        else:
            st.error("Failed to cancel")
else:
    st.info("No appointments available")

# ----------------- DATA PREP -----------------
df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
df["hour"] = df[time_col].dt.hour

st.write("📊 Live Data")
st.dataframe(df)

# ----------------- KPIs -----------------
total_patients = len(df)
emergency_cases = len(df[df["status"] == "emergency"])
completed = len(df[df["status"] == "completed"])
cancelled = len(df[df["status"] == "cancelled"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", total_patients)
col2.metric("Emergency Cases", emergency_cases)
col3.metric("Completed", completed)
col4.metric("Cancelled", cancelled)

# ----------------- DEPARTMENT LOAD -----------------
st.subheader("🏥 Department Load")

if not df.empty:
    dept_counts = df.groupby("department").size()
    st.bar_chart(dept_counts)
else:
    st.info("No data available")
