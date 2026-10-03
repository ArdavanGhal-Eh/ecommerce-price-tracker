"""
Price Trend Forecaster & Predictive Analytics Module
Part of Automated E-Commerce Price Intelligence Suite
Author: Ardavan Ghal-Eh | Sharif University of Technology
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime, timedelta


class PriceTrendForecaster:
    """
    Time-series forecasting and buy-timing recommendation engine
    using Exponential Moving Average (EMA) and trend velocity analysis.
    """

    def __init__(self, alpha: float = 0.35):
        self.alpha = alpha  # Smoothing factor for EMA

    def calculate_ema(self, prices: List[float]) -> List[float]:
        """Calculates Exponential Moving Average across price history."""
        if not prices:
            return []
        ema = [prices[0]]
        for price in prices[1:]:
            ema_val = self.alpha * price + (1 - self.alpha) * ema[-1]
            ema.append(ema_val)
        return ema

    def forecast_next_period(self, prices: List[float], days_ahead: int = 7) -> Dict[str, any]:
        """
        Projects future price trajectory, expected price band,
        and generates an algorithmic buy timing recommendation.
        """
        if len(prices) < 3:
            current_p = prices[-1] if prices else 0
            return {
                "current_price": current_p,
                "forecasted_price_7d": current_p,
                "trend_direction": "نامشخص (داده ناکافی)",
                "trend_slope_percent": 0.0,
                "recommendation": "داده‌های تاریخی کافی نیست",
                "confidence_score": 0.50
            }

        prices_arr = np.array(prices, dtype=float)
        ema_series = self.calculate_ema(prices)
        
        # Calculate velocity (slope per interval)
        x = np.arange(len(prices_arr))
        slope, intercept = np.polyfit(x, prices_arr, 1)
        slope_pct = (slope / prices_arr[-1]) * 100.0

        # Forecasted price
        forecast_price = max(0.0, prices_arr[-1] + slope * (days_ahead / 3.0))
        historical_min = np.min(prices_arr)
        historical_max = np.max(prices_arr)
        current_price = prices_arr[-1]

        # Recommendation logic
        if current_price <= historical_min * 1.03:
            rec = "🔥 زمان طلایی خرید (قیمت در کف تاریخی کانال)"
            direction = "کف قیمت (Strong Buy)"
        elif slope_pct < -1.5:
            rec = "⏳ صبر کنید (روند نزولی است، احتمال کاهش بیشتر تا هفته آینده)"
            direction = "نزولی (Downtrend)"
        elif slope_pct > 1.5:
            rec = "⚠️ خرید زودتر توصیه می‌شود (روند افزایشی است)"
            direction = "صعودی (Uptrend)"
        else:
            rec = "⚖️ قیمت باثبات (خرید با قیمت منصفانه)"
            direction = "باثبات (Sideways)"

        volatility = np.std(prices_arr) / np.mean(prices_arr)
        confidence = max(0.60, min(0.95, 1.0 - volatility))

        return {
            "current_price": int(current_price),
            "forecasted_price_7d": int(forecast_price),
            "historical_min": int(historical_min),
            "historical_max": int(historical_max),
            "trend_direction": direction,
            "trend_slope_percent": round(slope_pct, 2),
            "recommendation": rec,
            "confidence_score": round(confidence, 2)
        }


def run_demo_forecast():
    """Demonstrates price forecast on realistic laptop pricing history."""
    forecaster = PriceTrendForecaster(alpha=0.35)
    
    # 14-day price sample (in Toman) for ASUS Vivobook
    asus_prices = [
        42500000, 42000000, 41800000, 41200000, 40900000, 
        40500000, 40000000, 39800000, 39500000, 39200000, 
        38900000, 38700000, 38500000
    ]
    
    forecast = forecaster.forecast_next_period(asus_prices, days_ahead=7)
    print("=" * 60)
    print("📈 نتیجه تحلیل سری زمانی و پیش‌بینی هوشمند قیمت:")
    print("=" * 60)
    print(f"قیمت فعلی: {forecast['current_price']:,} تومان")
    print(f"پیش‌بینی قیمت ۷ روز آینده: {forecast['forecasted_price_7d']:,} تومان")
    print(f"جهت روند: {forecast['trend_direction']} (شیب: {forecast['trend_slope_percent']}%)")
    print(f"توصیه هوشمند خرید: {forecast['recommendation']}")
    print(f"ضریب اطمینان پیش‌بینی: {forecast['confidence_score'] * 100:.0f}%")
    print("=" * 60)


if __name__ == "__main__":
    run_demo_forecast()
