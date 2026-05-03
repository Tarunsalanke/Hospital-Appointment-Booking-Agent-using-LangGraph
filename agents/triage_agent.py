from tools.llm import llm

def triage_agent(state):
    symptoms = state["symptoms"]

    prompt = f"""
    You are a hospital triage assistant.

    Based on the symptoms, return ONLY the hospital department.

    Symptoms: {symptoms}

    Allowed departments:
    Cardiology
    Dermatology
    Orthopedics
    Neurology
    General
    """

    response = llm.invoke(prompt)
    state["department"] = response.content.strip()
    return state