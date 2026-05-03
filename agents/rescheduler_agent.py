from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def rescheduler_agent(state):
    # only for normal confirmed bookings
    if state["booking_status"] != "confirmed":
        return state

    dept = state["department"]

    with engine.connect() as conn:
        cancelled = conn.execute(
            text("""
                SELECT appointment_id, slot_time
                FROM appointments
                WHERE department=:dept
                AND status='cancelled'
                ORDER BY updated_at DESC
                LIMIT 1
            """),
            {"dept": dept}
        ).fetchone()

    if cancelled:
        state["slot_time"] = cancelled[1]
        state["booking_status"] = "rescheduled"

    return state