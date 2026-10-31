
from pprint import pprint

from app.services.analytics_service import AnalyticsService

analytics = AnalyticsService()

print("\n1. TOTAL REVENUE")
pprint(analytics.get_total_revenue())

print("\n2. TOP PRODUCT")
pprint(analytics.get_top_product())

print("\n3. MONTHLY REVENUE")
pprint(analytics.get_monthly_revenue())

print("\n4. TOP REGION")
pprint(analytics.get_top_region())

print("\n5. MONTH COMPARISON")
months = analytics.get_monthly_revenue()

if len(months) >= 2:
    pprint(
        analytics.compare_months(
            months[0]["month"],
            months[1]["month"]
        )
    )
else:
    print("Not enough months available for comparison")
