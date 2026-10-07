import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import sqlite3
import numpy as np
from competitor_basket_index import CompetitorBasketIndex
from price_trend_forecaster import PriceTrendForecaster
from scraper import PriceScraper


def test_competitor_basket_indices():
    analyzer = CompetitorBasketIndex()
    basket = [
        {"title": "Laptop A", "p0": 100.0, "q0": 10, "p1": 110.0, "q1": 10, "category": "Laptops"},
        {"title": "Phone B", "p0": 50.0, "q0": 20, "p1": 55.0, "q1": 20, "category": "Mobile"},
    ]
    res = analyzer.compute_basket_indices(basket)

    assert res["laspeyres_index"] == pytest.approx(110.0, rel=1e-2)
    assert res["paasche_index"] == pytest.approx(110.0, rel=1e-2)
    assert res["fisher_ideal_index"] == pytest.approx(110.0, rel=1e-2)
    assert res["basket_inflation_rate_percent"] == pytest.approx(10.0, rel=1e-2)
    assert "Laptops" in res["category_inflation_breakdown"]
    assert "Mobile" in res["category_inflation_breakdown"]


def test_competitor_basket_empty():
    analyzer = CompetitorBasketIndex()
    res = analyzer.compute_basket_indices([])
    assert res["laspeyres_index"] == 100.0
    assert res["fisher_ideal_index"] == 100.0
    assert res["basket_inflation_rate_percent"] == 0.0


def test_price_trend_forecaster_ema():
    forecaster = PriceTrendForecaster(alpha=0.5)
    prices = [10.0, 20.0, 30.0]
    ema = forecaster.calculate_ema(prices)
    assert len(ema) == 3
    assert ema[0] == 10.0
    assert ema[1] == 15.0  # 0.5 * 20 + 0.5 * 10
    assert ema[2] == 22.5  # 0.5 * 30 + 0.5 * 15


def test_price_trend_forecast_recommendation():
    forecaster = PriceTrendForecaster(alpha=0.35)
    # Downtrend prices
    prices = [100.0, 95.0, 90.0, 85.0, 80.0, 75.0]
    res = forecaster.forecast_next_period(prices, days_ahead=7)
    assert res["current_price"] == 75
    assert res["trend_slope_percent"] < 0
    assert "نزولی" in res["trend_direction"] or "کف" in res["trend_direction"]
    assert res["confidence_score"] > 0


def test_price_scraper_deal_score():
    scraper = PriceScraper(db_path=":memory:")
    great = scraper.calculate_deal_score(price=80, original_price=100, discount=20.0)
    assert "ارزش خرید بالا" in great

    fair = scraper.calculate_deal_score(price=92, original_price=100, discount=8.0)
    assert "منصفانه" in fair

    standard = scraper.calculate_deal_score(price=98, original_price=100, discount=2.0)
    assert "عادی" in standard


def test_price_scraper_database_roundtrip():
    scraper = PriceScraper(db_path=":memory:")
    records = scraper.generate_demo_dataset(category="TestCat", count=5)
    saved = scraper.save_to_db(records)
    assert saved == 5

    with scraper._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM product_snapshots")
        count = cursor.fetchone()[0]
        assert count == 5
