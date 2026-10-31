import pytest

from app.services.analytics_service import AnalyticsService


@pytest.fixture
def analytics():
    return AnalyticsService()


def test_total_revenue(analytics):
    result = analytics.get_total_revenue()

    assert result["total_revenue"] == 1439200.0
    assert result["total_transactions"] == 48


def test_top_product(analytics):
    result = analytics.get_top_product()

    assert result["product"] == "Monitor"
    assert result["total_revenue"] == 473000.0
    assert result["units_sold"] == 50


def test_monthly_revenue(analytics):
    result = analytics.get_monthly_revenue()

    assert len(result) == 6
    assert result[0]["month"] == "2026-01"
    assert result[0]["revenue"] == 210250.0
    assert result[-1]["month"] == "2026-06"


def test_top_region(analytics):
    result = analytics.get_top_region()

    assert result["region"] == "South"
    assert result["total_revenue"] == 411200.0
    assert result["total_transactions"] == 13


def test_compare_months(analytics):
    result = analytics.compare_months("2026-01", "2026-02")

    assert result["revenue1"] == 210250.0
    assert result["revenue2"] == 234600.0
    assert result["difference"] == 24350.0
    assert result["percentage_change"] == 11.58


def test_invalid_month_format(analytics):
    with pytest.raises(ValueError):
        analytics.compare_months("January", "2026-02")