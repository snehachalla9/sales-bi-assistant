
from app.services.analytics_service import AnalyticsService
from app.services.question_interpreter import QuestionInterpreter


class BusinessQueryService:

    def __init__(self):
        self.interpreter = QuestionInterpreter()
        self.analytics = AnalyticsService()

    def answer_question(self, question: str):

        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        interpretation = self.interpreter.interpret(question)

        intent = interpretation["intent"]

        if intent == "total_revenue":
            result = self.analytics.get_total_revenue()

        elif intent == "top_product":
            result = self.analytics.get_top_product()

        elif intent == "monthly_revenue":
            result = self.analytics.get_monthly_revenue()

        elif intent == "top_region":
            result = self.analytics.get_top_region()

        elif intent == "compare_months":
            result = self.analytics.compare_months(
                interpretation["month1"],
                interpretation["month2"]
            )

        else:
            return {
                "success": False,
                "message": (
                    "I can answer questions about total revenue, "
                    "top products, monthly revenue, regions and "
                    "monthly comparisons."
                )
            }

        return {
            "success": True,
            "intent": intent,
            "question": question,
            "result": result
        }
