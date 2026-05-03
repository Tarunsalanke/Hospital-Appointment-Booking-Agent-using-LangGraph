from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

def booking_agent(state):
    dept = state["department"]
    urgency = state["urgency"]

    if urgency == "EMERGENCY":
        state["booking_status"] = "redirect_to_emergency_room"
        state["slot_time"] = "IMMEDIATE"
        return state

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT doctor_id, available_slots
                FROM doctors
                WHERE department=:dept
                LIMIT 1
            """),
            {"dept": dept}
        ).fetchone()

    if result:
        state["doctor_id"] = result[0]
        state["slot_time"] = result[1][0]
        state["booking_status"] = "confirmed"
    else:
        state["booking_status"] = "failed"

    return state