
from sqlalchemy import text

from app.database.connection import engine


class AnalyticsService:

    # 1. Calculate total revenue
    def get_total_revenue(self):
        query = text("""
            SELECT
                ROUND(COALESCE(SUM(revenue), 0), 2) AS total_revenue,
                COUNT(*) AS total_transactions
            FROM sales_transactions
            WHERE LOWER(status) = 'completed'
        """)

        with engine.connect() as connection:
            result = connection.execute(query).mappings().first()

        return dict(result)

    # 2. Find the product with the highest revenue
    def get_top_product(self):
        query = text("""
            SELECT
                product,
                ROUND(SUM(revenue), 2) AS total_revenue,
                SUM(quantity) AS units_sold
            FROM sales_transactions
            WHERE LOWER(status) = 'completed'
            GROUP BY product
            ORDER BY total_revenue DESC, product ASC
            LIMIT 1
        """)

        with engine.connect() as connection:
            result = connection.execute(query).mappings().first()

        return dict(result) if result else {}

    # 3. Calculate monthly revenue
    def get_monthly_revenue(self):
        query = text("""
            SELECT
                SUBSTR(order_date, 1, 7) AS month,
                ROUND(SUM(revenue), 2) AS revenue
            FROM sales_transactions
            WHERE LOWER(status) = 'completed'
            GROUP BY SUBSTR(order_date, 1, 7)
            ORDER BY month
        """)

        with engine.connect() as connection:
            results = connection.execute(query).mappings().all()

        return [dict(row) for row in results]

    # 4. Find the region with highest revenue
    def get_top_region(self):
        query = text("""
            SELECT
                region,
                ROUND(SUM(revenue), 2) AS total_revenue,
                COUNT(*) AS total_transactions
            FROM sales_transactions
            WHERE LOWER(status) = 'completed'
            GROUP BY region
            ORDER BY total_revenue DESC, region ASC
            LIMIT 1
        """)

        with engine.connect() as connection:
            result = connection.execute(query).mappings().first()

        return dict(result) if result else {}

    # 5. Compare revenue between two months
    def compare_months(self, month1: str, month2: str):

        for month in [month1, month2]:
            if (
                len(month) != 7
                or month[4] != "-"
                or not month[:4].isdigit()
                or not month[5:].isdigit()
                or not 1 <= int(month[5:]) <= 12
            ):
                raise ValueError(
                    "Month must use YYYY-MM format"
                )

        query = text("""
            SELECT
                SUBSTR(order_date, 1, 7) AS month,
                ROUND(SUM(revenue), 2) AS revenue
            FROM sales_transactions
            WHERE LOWER(status) = 'completed'
              AND SUBSTR(order_date, 1, 7) IN (:month1, :month2)
            GROUP BY SUBSTR(order_date, 1, 7)
        """)

        with engine.connect() as connection:
            results = connection.execute(
                query,
                {
                    "month1": month1,
                    "month2": month2
                }
            ).mappings().all()

        revenue_by_month = {
            row["month"]: row["revenue"]
            for row in results
        }

        revenue1 = revenue_by_month.get(month1, 0) or 0
        revenue2 = revenue_by_month.get(month2, 0) or 0

        difference = round(revenue2 - revenue1, 2)

        percentage_change = (
            round((difference / revenue1) * 100, 2)
            if revenue1 else None
        )

        return {
            "month1": month1,
            "revenue1": revenue1,
            "month2": month2,
            "revenue2": revenue2,
            "difference": difference,
            "percentage_change": percentage_change
        }
