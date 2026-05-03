from langgraph.graph import StateGraph, END
from models.state import HospitalState
from agents.triage_agent import triage_agent
from agents.urgency_agent import urgency_agent
from agents.booking_agent import booking_agent
from agents.queue_agent import queue_agent
from agents.load_balancer_agent import load_balancer_agent
from agents.rescheduler_agent import rescheduler_agent
from agents.reminder_agent import reminder_agent

def build_graph():
    workflow = StateGraph(HospitalState)

    workflow.add_node("triage", triage_agent)
    workflow.add_node("urgency", urgency_agent)
    workflow.add_node("booking", booking_agent)
    workflow.add_node("load_balancer", load_balancer_agent)
    workflow.add_node("rescheduler", rescheduler_agent)
    workflow.add_node("queue", queue_agent)
    workflow.add_node("reminder", reminder_agent)

    workflow.set_entry_point("triage")

    workflow.add_edge("triage", "urgency")
    workflow.add_edge("urgency", "booking")
    workflow.add_edge("booking", "load_balancer")
    workflow.add_edge("load_balancer", "rescheduler")
    workflow.add_edge("rescheduler", "queue")
    workflow.add_edge("queue", "reminder")
    workflow.add_edge("reminder", END)

    return workflow.compile()