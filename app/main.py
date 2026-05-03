from fastapi import FastAPI
from pydantic import BaseModel
from graph.workflow import build_graph
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

app = FastAPI()
graph = build_graph()

class PatientRequest(BaseModel):
    patient_name: str
    phone_number: str   # ✅ NEW
    symptoms: str


@app.post("/cancel")
def cancel_appointment(appointment_id: int):
    with engine.connect() as conn:
        conn.execute(
            text("""
                UPDATE appointments
                SET status = 'cancelled'
                WHERE appointment_id = :id
            """),
            {"id": appointment_id}
        )
        conn.commit()

    return {"message": "Appointment cancelled"}


@app.post("/book")
def book_appointment(request: PatientRequest):
    state = {
        "patient_name": request.patient_name,
        "phone_number": request.phone_number,  # ✅ NEW
        "symptoms": request.symptoms,
        "department": None,
        "urgency": None,
        "doctor_id": None,
        "slot_time": None,
        "booking_status": None,
        "queue_token": None,
        "estimated_wait": None
    }
    
    result = graph.invoke(state)
    return result