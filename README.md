# 🛒 Automated E-Commerce Price Intelligence & Market Scraper

A robust, production-grade Python web scraper and market intelligence pipeline designed to monitor competitor product catalogs, track price fluctuations, evaluate deal quality, and maintain historical price snapshots in SQLite and Excel.

---

## 📌 Project Overview
Online retailers and businesses need real-time awareness of market price trends and stock availability to maintain competitive pricing strategies. This project provides an autonomous data extraction engine that:
1. Crawls e-commerce product pages and search listings.
2. Extracts clean structured data (Product Title, Current Price, Original Price, Discount Percentage, Seller Name, User Rating, and Stock Status).
3. Evaluates deals algorithmically (*Great Deal*, *Fair Deal*, or *Standard Pricing*) based on historical margins and discount depths.
4. Generates business-ready Excel reports (`.xlsx`) with Persian/English headings and logs structured records into an SQLite relational database.

---

## 🌟 Architecture & Data Flow

```text
┌─────────────────────────┐
│ Target Product Listings │
└────────────┬────────────┘
             │ HTTP GET (Random User-Agents, Dynamic Headers)
             ▼
┌─────────────────────────┐
│   HTTP Request Engine   │ <─── Exponential Backoff Retry (Max 3 retries)
└────────────┬────────────┘
             │ HTML Response
             ▼
┌─────────────────────────┐
│ BeautifulSoup4 & Parser │ ───> Regex Price Cleaning & Digits Extraction
└────────────┬────────────┘
             │ Structured Dictionaries
             ▼
┌─────────────────────────┐
│   Deal Scoring Engine   │ ───> Discount Evaluation (>=15% -> High Value Deal)
└────────────┬────────────┘
             ├──────────────────────────────────────┐
             ▼                                      ▼
┌─────────────────────────┐            ┌─────────────────────────┐
│   SQLite Database       │            │   Excel Exporter        │
│   (product_snapshots,   │            │   (Pandas & openpyxl,   │
│    price_drop_alerts)   │            │    Market_Prices sheet) │
└─────────────────────────┘            └─────────────────────────┘
```

---

## 🔑 Key Engineering Features

- **Anti-Bot Resilience:** Implements randomized desktop User-Agent header rotation, natural request delays, and retry loops with exponential backoff to handle rate limits and transient connection drops.
- **Deal Scoring Algorithm:**
  - `🔥 ارزش خرید بالا (Great Deal)`: Applied to products with $\ge 15\%$ discount or selling below 85% of market baseline.
  - `⚖️ قیمت منصفانه (Fair Deal)`: Applied to products with $5\% \le \text{Discount} < 15\%$.
  - `📌 قیمت عادی (Standard)`: Standard list pricing.
- **Automated Price Drop Alerting:** When a price drop $\ge 15\%$ is detected, an event is logged in the `price_drop_alerts` database table for webhook/notification dispatching.
- **Dual Persistence:** Automatically populates a local SQLite relational database and exports a formatted `.xlsx` workbook.
- **High-Concurrency Go Module (`fast_fetcher_go/`):** Optional companion crawler written in Go utilizing Goroutines and channels to scrape dozens of endpoints concurrently without Python GIL overhead.
- **Automated CI/CD (`.github/workflows/ci.yml`):** Fully integrated GitHub Actions workflow verifying Python scraping, database insertion, and Excel export on every commit.

---

## 📊 Database Schema (`market_data.db`)

### `product_snapshots` Table
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | Unique auto-incrementing snapshot identifier |
| `title` | TEXT | Cleaned product title |
| `category` | TEXT | Product category classification |
| `price_toman` | INTEGER | Final selling price in Toman |
| `original_price_toman` | INTEGER | Base price before discount |
| `discount_percent` | REAL | Calculated discount percentage |
| `deal_score` | TEXT | Algorithmic deal quality rating |
| `in_stock` | BOOLEAN | Inventory availability flag |
| `seller` | TEXT | Marketplace merchant / vendor name |
| `rating` | REAL | User review score (out of 5.0) |
| `url` | TEXT | Canonical product URL |
| `scraped_at` | TIMESTAMP | ISO timestamp of data capture |

---


---

## 📈 Module 3: Predictive Price Trend Forecaster ()
- **Exponential Moving Average (EMA) Smoothing:** Evaluates price velocity over historical time-series data.
- **7-Day Price Trajectory:** Calculates linear trend slope ($\Delta P / \Delta t$) and projects upcoming 7-day price bands.
- **Algorithmic Buy-Timing Recommendation:**
  - : Triggered when current price reaches historical channel lows ($\le 1.03 	imes P_{min}$).
  - : High velocity negative slope ($	ext{Slope} < -1.5\%$) advising delay for deeper discounts.
  - : Rising supplier pricing indicating imminent price hikes.
- **Quick Run:**
  

## 🚀 Installation & Usage

### 1. Clone Repository
```bash
git clone https://github.com/ArdavanGhal-Eh/ecommerce-price-tracker.git
cd ecommerce-price-tracker
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Scraper Pipeline
```bash
# Run with default settings (Demo dataset & Excel generation):
python scraper.py --category "Digital-Electronics" --output "market_price_report.xlsx"

# Run with custom database file:
python scraper.py --category "Laptops" --output "laptops_report.xlsx" --db "my_catalog.db"
```

### 4. (Optional) Run High-Concurrency Go Fetcher
```bash
cd fast_fetcher_go
go run main.go
```

---

## 📋 CLI Arguments Reference
| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--category` | `string` | `Digital-Electronics` | Product category filter |
| `--output` | `string` | `market_price_report.xlsx` | Output Excel workbook filename |
| `--db` | `string` | `market_data.db` | SQLite database file path |
| `--demo` | `flag` | `True` | Runs pipeline with structured realistic dataset |

---

## 📄 Sample Excel Output Schema
| عنوان کالا | دسته‌بندی | قیمت نهایی (تومان) | تخفیف (%) | ارزیابی قیمت (Deal Score) | وضعیت موجودی | فروشنده |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| لپ‌تاپ 15.6 اینچی ایسوس Vivobook 15 | لپ‌تاپ | ۳۸,۵۰۰,۰۰۰ | ۱۰٪ | ⚖️ قیمت منصفانه | موجود | دیجی‌کالا |
| مک‌بوک ایر 13 اینچی اپل M2 | لپ‌تاپ | ۸۹,۰۰۰,۰۰۰ | ۵٪ | ⚖️ قیمت منصفانه | موجود | بازرگانی پارس |
| گوشی موبایل سامسونگ Galaxy S24 Ultra | موبایل | ۷۲,۰۰۰,۰۰۰ | ۱۲٪ | ⚖️ قیمت منصفانه | موجود | دیجی‌لند |
| مانیتور 27 اینچی شیائومی 165Hz | مانیتور | ۱۴,۲۰۰,۰۰۰ | ۱۶٪ | 🔥 ارزش خرید بالا | موجود | دیجی‌کالا |

---

## 🛠️ Tech Stack
- **Core Language:** Python 3.10+
- **HTTP & Parsing:** `requests`, `beautifulsoup4`, `lxml`
- **Data Engineering:** `pandas`, `openpyxl`, `sqlite3`
- **Concurrency (Optional):** Go 1.21+ (`net/http`, Goroutines)
- **CI/CD Automation:** GitHub Actions

---

## 👨‍💻 Author
**Ardavan Ghal-Eh**  
Mechanical Engineering Student, Sharif University of Technology  
*Focus: Data Pipelines, Industrial Automation & Computational Engineering*
