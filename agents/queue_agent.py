from tools.redis_client import redis_client
import redis

def queue_agent(state):
    try:
        if state["booking_status"] == "redirect_to_emergency_room":
            state["queue_token"] = 0
            state["estimated_wait"] = "0 mins"
            return state

        dept = state["department"]
        urgency = state["urgency"]
        queue_name = f"{dept}_queue"

        if urgency in ["HIGH", "EMERGENCY"]:
            redis_client.lpush(queue_name, state["patient_name"])
        else:
            redis_client.rpush(queue_name, state["patient_name"])

        token = redis_client.llen(queue_name)

        state["queue_token"] = token
        state["estimated_wait"] = f"{token * 10} mins"

    except redis.exceptions.ConnectionError:
        state["queue_token"] = -1
        state["estimated_wait"] = "Queue service unavailable"

    return state