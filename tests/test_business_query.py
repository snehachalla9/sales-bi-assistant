from unittest.mock import Mock
import pytest

from app.services.business_query_service import BusinessQueryService


@pytest.fixture
def service():
    instance = BusinessQueryService()
    instance.interpreter = Mock()
    return instance


@pytest.mark.parametrize(
    "question,intent",
    [
        ("What is the total revenue?", "total_revenue"),
        ("Which product generated the highest revenue?", "top_product"),
        ("Show me monthly revenue", "monthly_revenue"),
        ("Which region has the highest sales?", "top_region"),
    ],
)
def test_supported_questions(service, question, intent):
    service.interpreter.interpret.return_value = {
        "intent": intent,
        "month1": None,
        "month2": None,
    }

    result = service.answer_question(question)

    assert result["success"] is True
    assert result["intent"] == intent
    assert result["question"] == question


def test_empty_question():
    service = BusinessQueryService()

    with pytest.raises(ValueError):
        service.answer_question("")


def test_unsupported_question(service):
    service.interpreter.interpret.return_value = {
        "intent": "unsupported",
        "month1": None,
        "month2": None,
    }

    result = service.answer_question("Tell me a joke")

    assert result["success"] is False
    assert "message" in result