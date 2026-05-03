from typing import TypedDict, Optional

class HospitalState(TypedDict):
    patient_name: str
    phone_number: str
    symptoms: str
    department: Optional[str]
    urgency: Optional[str]
    doctor_id: Optional[int]
    doctor_name: Optional[str]
    slot_time: Optional[str]
    booking_status: Optional[str]
    queue_token: Optional[int]
    estimated_wait: Optional[str]