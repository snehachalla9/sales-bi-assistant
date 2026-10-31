from pprint import pprint

from app.services.business_query_service import BusinessQueryService

service = BusinessQueryService()

questions = [
    "What is the total revenue?",
    "Which product generated the highest revenue?",
    "Show me monthly revenue",
    "Which region has the highest sales?",
    "Compare January 2026 and February 2026"
]

for question in questions:
    print("\nQUESTION:", question)

    try:
        result = service.answer_question(question)
        pprint(result)
    except Exception as error:
        print("ERROR:", error)