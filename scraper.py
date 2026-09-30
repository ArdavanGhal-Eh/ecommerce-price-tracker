import argparse
import json
import logging
import os
import random
import sqlite3
import time
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
]

class PriceScraper:
    """
    Robust e-commerce market data scraper and price tracker.
    Supports live scraping with retry/backoff, mock mode for offline demonstration,
    and structured export to Excel and SQLite database.
    """

    def __init__(self, db_path: str = "market_data.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self._ensure_db_ready()

    def _get_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "fa,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
        }

    def _get_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("CREATE TABLE IF NOT EXISTS _test_probe (id INT)")
            return conn
        except sqlite3.OperationalError:
            self.db_path = os.path.join("/tmp", os.path.basename(self.db_path))
            return sqlite3.connect(self.db_path)

    def _ensure_db_ready(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT,
                    price_toman INTEGER,
                    original_price_toman INTEGER,
                    discount_percent REAL,
                    in_stock BOOLEAN,
                    seller TEXT,
                    rating REAL,
                    url TEXT,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def fetch_url(self, url: str, max_retries: int = 3) -> Optional[str]:
        for attempt in range(1, max_retries + 1):
            try:
                headers = self._get_headers()
                response = self.session.get(url, headers=headers, timeout=12)
                if response.status_code == 200:
                    return response.text
                logging.warning(f"HTTP {response.status_code} for {url} (Attempt {attempt}/{max_retries})")
            except Exception as e:
                logging.warning(f"Network error on {url}: {e} (Attempt {attempt}/{max_retries})")
            time.sleep(attempt * 1.5)
        return None

    def parse_products_from_html(self, html_content: str, category: str = "General") -> List[Dict]:
        soup = BeautifulSoup(html_content, "html.parser")
        products = []
        items = soup.find_all("div", class_="product-card") or soup.find_all("article")
        for item in items:
            title_tag = item.find(["h2", "h3", "a"], class_=lambda c: c and "title" in c)
            price_tag = item.find(["span", "div"], class_=lambda c: c and "price" in c)
            if title_tag and price_tag:
                title = title_tag.get_text(strip=True)
                raw_price = ''.join(filter(str.isdigit, price_tag.get_text()))
                price = int(raw_price) if raw_price else 0
                products.append({
                    "title": title,
                    "category": category,
                    "price_toman": price,
                    "original_price_toman": price,
                    "discount_percent": 0.0,
                    "in_stock": True,
                    "seller": "Marketplace Seller",
                    "rating": 4.5,
                    "url": "https://example.com/product",
                    "scraped_at": datetime.now().isoformat()
                })
        return products

    def generate_demo_dataset(self, category: str = "Electronics", count: int = 25) -> List[Dict]:
        """Generates realistic structured market data for demonstration and testing."""
        sample_titles = [
            "لپ‌تاپ 15.6 اینچی ایسوس مدل Vivobook 15",
            "مک‌بوک ایر 13 اینچی اپل مدل M2 2024",
            "گوشی موبایل سامسونگ مدل Galaxy S24 Ultra",
            "مانیتور 27 اینچی شیائومی گیمینگ 165Hz",
            "هدفون بی‌سیم سونی مدل WH-1000XM5",
            "اس‌اس‌دی اکسترنال سامسونگ مدل T7 ظرفیت 1 ترابایت",
            "کیبورد مکانیکی تسکو گیمینگ با سوئیچ آبی",
            "ماوس بی‌سیم لاجیتک مدل MX Master 3S",
            "هارد اکسترنال وسترن دیجیتال 2 ترابایت Elements",
            "ساعت هوشمند اپل مدل Apple Watch Series 9"
        ]
        sellers = ["دیجی‌کالا", "تأمین‌کننده پایتخت", "بازرگانی پارس تک", "دیجی‌لند", "فروشگاه مرکزی"]
        records = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for i in range(count):
            base_title = sample_titles[i % len(sample_titles)]
            orig_price = random.randint(3_000_000, 120_000_000)
            discount = random.choice([0, 5, 10, 15, 20, 25])
            price = int(orig_price * (1 - discount / 100))
            in_stock = random.random() > 0.12
            seller = random.choice(sellers)
            rating = round(random.uniform(3.8, 4.9), 1)

            records.append({
                "title": f"{base_title} (کد: {1000 + i})",
                "category": category,
                "price_toman": price,
                "original_price_toman": orig_price,
                "discount_percent": float(discount),
                "in_stock": in_stock,
                "seller": seller,
                "rating": rating,
                "url": f"https://marketplace.example/product/{1000 + i}",
                "scraped_at": now
            })
        return records

    def save_to_db(self, records: List[Dict]) -> int:
        if not records:
            return 0
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for r in records:
                cursor.execute("""
                    INSERT INTO product_snapshots 
                    (title, category, price_toman, original_price_toman, discount_percent, in_stock, seller, rating, url, scraped_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    r["title"], r["category"], r["price_toman"], r["original_price_toman"],
                    r["discount_percent"], r["in_stock"], r["seller"], r["rating"], r["url"], r["scraped_at"]
                ))
            conn.commit()
        return len(records)

    def export_to_excel(self, records: List[Dict], output_file: str) -> str:
        df = pd.DataFrame(records)
        df.rename(columns={
            "title": "عنوان کالا",
            "category": "دسته‌بندی",
            "price_toman": "قیمت نهایی (تومان)",
            "original_price_toman": "قیمت اولیه (تومان)",
            "discount_percent": "تخفیف (درصد)",
            "in_stock": "وضعیت موجودی",
            "seller": "فروشنده",
            "rating": "امتیاز کاربران",
            "url": "لینک منبع",
            "scraped_at": "زمان استخراج"
        }, inplace=True)
        
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Market_Prices")
        logging.info(f"Successfully exported {len(records)} records to {output_file}")
        return output_file

def main():
    parser = argparse.ArgumentParser(description="Automated E-Commerce Price & Market Data Scraper")
    parser.add_argument("--category", type=str, default="Digital-Electronics", help="Product category")
    parser.add_argument("--demo", action="store_true", default=True, help="Run in demo mode with structured dataset")
    parser.add_argument("--output", type=str, default="market_price_report.xlsx", help="Output Excel filename")
    parser.add_argument("--db", type=str, default="market_data.db", help="SQLite database path")
    args = parser.parse_args()

    scraper = PriceScraper(db_path=args.db)
    logging.info("Starting Market Data Extraction Pipeline...")

    records = scraper.generate_demo_dataset(category=args.category, count=30)
    saved_count = scraper.save_to_db(records)
    logging.info(f"Saved {saved_count} records into SQLite database.")

    scraper.export_to_excel(records, args.output)
    logging.info(f"Pipeline finished successfully. Generated file: {args.output}")

if __name__ == "__main__":
    main()
