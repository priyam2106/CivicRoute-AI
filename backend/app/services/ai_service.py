
from typing import Any


CATEGORIES = {
    "pothole",
    "road_damage",
    "open_manhole",
    "flooding",
    "traffic_signal",
    "signage",
    "debris",
    "drainage",
    "public_transport",
    "other",
}


def analyze_complaint(description: str) -> dict[str, Any]:
    """
    Mock AI service for development.

    This uses keyword rules, not a real AI model.
    Later, we can replace it with an LLM adapter.
    """

    text = description.lower()

    # Default values
    category = "other"
    urgency = 2
    severity = "LOW"
    recommended_action = "Review the complaint and verify the location."

    # Classify the complaint
    if any(word in text for word in ["open manhole", "uncovered manhole"]):
        category = "open_manhole"
        urgency = 5
        severity = "CRITICAL"
        recommended_action = "Inspect and secure the open manhole urgently."

    elif any(word in text for word in ["flood", "waterlogging", "water logged"]):
        category = "flooding"
        urgency = 4
        severity = "HIGH"
        recommended_action = "Inspect the affected area and assess flooding risks."

    elif any(word in text for word in ["traffic light", "traffic signal"]):
        category = "traffic_signal"
        urgency = 4
        severity = "HIGH"
        recommended_action = "Inspect the traffic signal and manage traffic safely."

    elif any(word in text for word in ["pothole", "road hole"]):
        category = "pothole"
        urgency = 3
        severity = "MEDIUM"
        recommended_action = "Inspect the pothole and schedule appropriate repairs."

    elif any(word in text for word in ["broken road", "damaged road", "road damage"]):
        category = "road_damage"
        urgency = 3
        severity = "MEDIUM"
        recommended_action = "Inspect the damaged road and assess repair requirements."

    elif any(word in text for word in ["drain", "blocked drainage", "sewer"]):
        category = "drainage"
        urgency = 3
        severity = "MEDIUM"
        recommended_action = "Inspect the drainage system for blockage or damage."

    elif any(word in text for word in ["fallen tree", "debris", "rubble"]):
        category = "debris"
        urgency = 3
        severity = "MEDIUM"
        recommended_action = "Inspect the obstruction and arrange safe removal if needed."

    elif any(word in text for word in ["bus", "public transport", "bus stop"]):
        category = "public_transport"
        urgency = 2
        severity = "LOW"
        recommended_action = "Review the public transport complaint and verify the details."

    elif any(word in text for word in ["signboard", "road sign", "missing sign"]):
        category = "signage"
        urgency = 2
        severity = "LOW"
        recommended_action = "Inspect the road signage and arrange repair or replacement if needed."

    # Create a short summary
    words = description.strip().split()
    summary = " ".join(words[:20])

    if len(words) > 20:
        summary += "..."

    return {
        "predicted_category": category,
        "urgency": urgency,
        "severity": severity,
        "summary": summary,
        "recommended_action": recommended_action,
        "review_status": "PENDING",
        "model_name": "mock-keyword-v1",
        "prompt_version": "mock-rules-v1",
    }
