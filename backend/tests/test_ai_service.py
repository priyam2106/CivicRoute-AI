
from app.services.ai_service import analyze_complaint


def test_open_manhole_classification():
    result = analyze_complaint(
        "There is an open manhole near the school."
    )

    assert result["predicted_category"] == "open_manhole"
    assert result["urgency"] == 5
    assert result["review_status"] == "PENDING"


def test_pothole_classification():
    result = analyze_complaint(
        "A large pothole is present near the market."
    )

    assert result["predicted_category"] == "pothole"
    assert result["urgency"] == 3


def test_flooding_classification():
    result = analyze_complaint(
        "Waterlogging is occurring on the main road."
    )

    assert result["predicted_category"] == "flooding"
    assert result["urgency"] == 4


def test_summary_is_created():
    result = analyze_complaint(
        "A pothole is present near the bus stop."
    )

    assert result["summary"]
    assert len(result["summary"]) > 0
