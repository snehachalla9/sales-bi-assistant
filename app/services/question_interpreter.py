
import json
import os
import re
from datetime import datetime

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

ALLOWED_INTENTS = {
    "total_revenue",
    "top_product",
    "monthly_revenue",
    "top_region",
    "compare_months",
    "unsupported"
}


class QuestionInterpreter:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not configured")

        self.client = Groq(api_key=api_key)
        self.model = os.getenv(
            "LLM_MODEL",
            "openai/gpt-oss-20b"
        )

    def interpret(self, question: str):

        prompt = f"""
You are a business analytics question classifier.

Identify the user's requested analytics operation.

Supported intents:
1. total_revenue
2. top_product
3. monthly_revenue
4. top_region
5. compare_months
6. unsupported

Return ONLY a JSON object with these fields:
- intent
- month1
- month2

For questions comparing two months, extract both months
in YYYY-MM format.

For all other intents, month1 and month2 must be null.

If the question does not match the supported analytics,
use unsupported.

Examples:

Question: What is the total revenue?
JSON: {{"intent":"total_revenue","month1":null,"month2":null}}

Question: Which product sold the most?
JSON: {{"intent":"top_product","month1":null,"month2":null}}

Question: Show monthly revenue.
JSON: {{"intent":"monthly_revenue","month1":null,"month2":null}}

Question: Which region has the highest sales?
JSON: {{"intent":"top_region","month1":null,"month2":null}}

Question: Compare January 2026 and February 2026.
JSON: {{"intent":"compare_months","month1":"2026-01","month2":"2026-02"}}

User question:
{question}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Classify analytics questions. Return valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )

        result = json.loads(
            response.choices[0].message.content
        )

        intent = result.get("intent")

        if intent not in ALLOWED_INTENTS:
            raise ValueError("Unsupported analytics intent")

        month1 = result.get("month1")
        month2 = result.get("month2")

        if intent == "compare_months":
            for month in [month1, month2]:
                if not isinstance(month, str):
                    raise ValueError("Two valid months are required")

                if not re.fullmatch(r"\d{4}-\d{2}", month):
                    raise ValueError("Invalid month format")

                try:
                    datetime.strptime(month, "%Y-%m")
                except ValueError:
                    raise ValueError("Invalid calendar month")

            if month1 == month2:
                raise ValueError("Please provide two different months")

        return {
            "intent": intent,
            "month1": month1,
            "month2": month2
        }
