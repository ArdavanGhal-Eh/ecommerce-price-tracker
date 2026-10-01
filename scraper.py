import argparse
import random
import pandas as pd
from datetime import datetime

class PriceScraper:
    def get_prices(self):
        return [
            {"Title": "لپ‌تاپ ایسوس Vivobook 15", "Price": 38500000, "Discount": 10, "Score": "🔥 عالی"},
            {"Title": "مک‌بوک ایر M2 اپل", "Price": 89000000, "Discount": 5, "Score": "⚖️ منصفانه"},
            {"Title": "گوشی سامسونگ S24 Ultra", "Price": 72000000, "Discount": 12, "Score": "🔥 عالی"}
        ]

if __name__ == "__main__":
    s = PriceScraper()
    df = pd.DataFrame(s.get_prices())
    df.to_excel("market_report.xlsx", index=False)
    print("Market report generated: market_report.xlsx")
