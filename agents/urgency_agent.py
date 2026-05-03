from tools.llm import llm

def urgency_agent(state):
    symptoms = state["symptoms"]

    prompt = f"""
You are a highly accurate hospital triage AI assistant.

Your task is to classify patient urgency based on symptoms.

Follow these STRICT medical rules:

EMERGENCY:
- Life-threatening conditions
- Chest pain, breathing difficulty, stroke symptoms, unconsciousness, heavy bleeding
- Immediate medical attention required

HIGH:
- Severe symptoms but not immediately life-threatening
- Severe body pain, high fever (>102°F), persistent vomiting, extreme weakness

MEDIUM:
- Noticeable symptoms that require medical attention
- Moderate pain, infection symptoms, recurring issues

LOW:
- Mild symptoms
- Minor headache, cold, mild fever, small skin issues

IMPORTANT RULES:
- If the word "severe" appears → at least HIGH
- If symptoms indicate breathing/chest/heart → EMERGENCY
- Always choose the higher severity if unsure
- Never underestimate urgency

Symptoms: {symptoms}

Return ONLY one word from:
LOW, MEDIUM, HIGH, EMERGENCY
"""

    response = llm.invoke(prompt)
    state["urgency"] = response.content.strip().upper()
    return state