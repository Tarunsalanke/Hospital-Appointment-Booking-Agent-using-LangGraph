from tools.notification import send_sms

def reminder_agent(state):
    if state["booking_status"] in ["confirmed", "rescheduled"]:
        msg = (
            f"Hello {state['patient_name']},\n"
            f"Your appointment is confirmed.\n\n"
            f"👨‍⚕️ Doctor: {state['doctor_name']}\n"
            f"🏥 Department: {state['department']}\n"
            f"⏰ Time: {state['slot_time']}\n"
            f"🎟️ Token: {state['queue_token']}\n"
            f"⏳ Wait: {state['estimated_wait']}"
        )

        send_sms(state["phone_number"], msg)

    return state