from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def load_balancer_agent(state):

    # 🚨 Emergency case
    if state["booking_status"] == "redirect_to_emergency_room":
        with engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO appointments (
                        patient_name,
                        symptoms,
                        department,
                        doctor_id,
                        slot_time,
                        status
                    )
                    VALUES (
                        :name, :symptoms, :dept, NULL, 'IMMEDIATE', 'emergency'
                    )
                """),
                {
                    "name": state["patient_name"],
                    "symptoms": state["symptoms"],
                    "dept": state["department"]
                }
            )
            conn.commit()

        return state

    dept = state["department"]

    with engine.connect() as conn:
        doctors = conn.execute(
            text("""
                SELECT doctor_id, name, available_slots
                FROM doctors
                WHERE department=:dept
            """),
            {"dept": dept}
        ).fetchall()

    if not doctors:
        state["booking_status"] = "failed"
        return state

    # 🎯 pick earliest slot doctor
    selected = doctors[0]
    for doctor in doctors:
        if doctor[2][0] < selected[2][0]:
            selected = doctor

    state["doctor_id"] = selected[0]
    state["doctor_name"] = selected[1]
    state["slot_time"] = selected[2][0]
    state["booking_status"] = "confirmed"

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO appointments (
                    patient_name,
                    symptoms,
                    department,
                    doctor_id,
                    slot_time,
                    status
                )
                VALUES (
                    :name, :symptoms, :dept, :doc, :slot, :status
                )
            """),
            {
                "name": state["patient_name"],
                "symptoms": state["symptoms"],
                "dept": state["department"],
                "doc": state["doctor_id"],
                "slot": state["slot_time"],
                "status": state["booking_status"]
            }
        )
        conn.commit()

    return state