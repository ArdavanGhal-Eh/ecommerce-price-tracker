<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Go Worker](https://img.shields.io/badge/Go-Fast_Fetcher-00ADD8.svg?style=for-the-badge&logo=go&logoColor=white)](https://golang.org/)
[![Storage](https://img.shields.io/badge/Database-SQLite3-003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Reporting](https://img.shields.io/badge/Reporting-OpenPyXL-217346.svg?style=for-the-badge&logo=microsoft-excel&logoColor=white)](https://openpyxl.readthedocs.io/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg?style=for-the-badge)](https://github.com/ArdavanGhal-Eh/ecommerce-price-tracker)
[![Stars](https://img.shields.io/github/stars/ArdavanGhal-Eh/ecommerce-price-tracker?style=for-the-badge&color=gold)](https://github.com/ArdavanGhal-Eh/ecommerce-price-tracker/stargazers)
[![Issues](https://img.shields.io/github/issues/ArdavanGhal-Eh/ecommerce-price-tracker?style=for-the-badge&color=red)](https://github.com/ArdavanGhal-Eh/ecommerce-price-tracker/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](https://github.com/ArdavanGhal-Eh/ecommerce-price-tracker/pulls)

<br />

# 🛒 Automated E-Commerce Price Intelligence & Market Scraper
### *High-Concurrency Web Crawling, Algorithmic Deal Scoring & 7-Day Trend Forecasting in Python & Go*

<p align="center">
  <b>A production-grade competitive intelligence engine designed to monitor multi-seller e-commerce marketplaces. Combines resilient Python scraping with a high-throughput Go concurrent worker pool, persists longitudinal price histories in SQLite, evaluates competitor basket inflation via the Laspeyres index, forecasts 7-day price trajectories, and generates executive Excel reports with conditional deal badges.</b>
  <br /><br />
  <a href="#-system-architecture--data-pipeline"><strong>Pipeline Architecture »</strong></a>
  &nbsp;•&nbsp;
  <a href="#-algorithmic-formulation--pricing-models"><strong>Pricing Analytics »</strong></a>
  &nbsp;•&nbsp;
  <a href="#-quickstart--installation"><strong>Quickstart Guide »</strong></a>
  &nbsp;•&nbsp;
  <a href="https://github.com/ArdavanGhal-Eh/ecommerce-price-tracker/issues"><strong>Report Issue</strong></a>
</p>

</div>

---

<!-- TABLE OF CONTENTS -->
<details open>
  <summary><h2 style="display: inline-block;">📑 Table of Contents</h2></summary>
  <ol>
    <li><a href="#-executive-summary--business-problem">Executive Summary & Business Problem</a></li>
    <li><a href="#-key-features--capabilities">Key Features & Capabilities</a></li>
    <li><a href="#-system-architecture--data-pipeline">System Architecture & Data Pipeline</a></li>
    <li><a href="#-algorithmic-formulation--pricing-models">Algorithmic Formulation & Pricing Models</a></li>
    <li><a href="#-technology-stack">Technology Stack</a></li>
    <li><a href="#-repository-structure">Repository Structure</a></li>
    <li><a href="#-database-schema">Database Schema</a></li>
    <li><a href="#-quickstart--installation">Quickstart & Installation</a></li>
    <li><a href="#-cli-reference--usage-guide">CLI Reference & Usage Guide</a></li>
    <li><a href="#-roadmap--future-enhancements">Roadmap & Future Enhancements</a></li>
    <li><a href="#-contributing--license">Contributing & License</a></li>
    <li><a href="#-author--contact">Author & Contact</a></li>
  </ol>
</details>

---

## 📌 Executive Summary & Business Problem

In fast-paced retail and e-commerce ecosystems (Digikala, Amazon, Torob, Emalls):
1. **Dynamic Pricing Friction:** Competitors alter product prices multiple times per day. Manual price auditing fails to catch flash sales, predatory undercutting, or sudden stock-outs.
2. **Anti-Scraping Defenses & Rate Limits:** Fragile scrapers get blocked by IP throttles and Cloudflare bot detection. A robust engine must rotate User-Agents, apply exponential backoff retries, and support concurrent distributed fetching.
3. **Data Without Action:** Simply dumping raw HTML is useless to commercial directors. Teams need algorithmic deal evaluation, competitor price basket inflation indices, and automated Excel workbooks highlighting immediate margin opportunities.

This project delivers an end-to-end price intelligence pipeline integrating resilient Python scraping, a high-concurrency Go worker pool, predictive forecasting, and executive reporting.

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## ✨ Key Features & Capabilities

- 🔄 **Resilient Multi-Threaded Crawler (`scraper.py`):** Configurable User-Agent rotation, automatic HTTP retry adapters with exponential backoff, and robust error handling.
- ⚡ **High-Concurrency Go Worker Pool (`fast_fetcher_go`):** Lightweight Go binary performing concurrent HTTP requests and JSON stream parsing at 1,000+ pages/minute.
- 🎯 **Algorithmic Deal Quality Scoring:** Classifies price cuts using historical distributions (`EXCELLENT_DEAL`, `MODERATE_DISCOUNT`, `OVERPRICED`, `FAKE_DISCOUNT`).
- 📈 **Predictive Price Trend Forecaster (`price_trend_forecaster.py`):** Calculates 7-day predictive moving average trends and linear regression price velocities ($dp/dt$).
- 🧺 **Competitor Basket Inflation Index (`competitor_basket_index.py`):** Computes Laspeyres inflation metrics to measure whether an entire competitor catalog is getting cheaper or more expensive.
- 📊 **Executive Excel Dashboard:** Generates styled `.xlsx` reports with green/red status badges, formatted currency values, and discount distribution charts using OpenPyXL.

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 🏗️ System Architecture & Data Pipeline

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Target E-Commerce Product Listings                   │
│             (Digikala / Torob / Competitor Marketplaces)               │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   Ingestion & Extraction Engine                        │
│         - Python Scraper with User-Agent Rotation                      │
│         - High-Concurrency Go Worker Pool (Goroutines)                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Structured Product Payloads
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   Longitudinal SQLite Persistence                      │
│         Table: products (id, title, price, seller, rating, time)       │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
                    ▼                                ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────┐
│    Price Forecaster & Deal Engine    │  │ Competitor Basket Inflation  │
│  - 7-Day Moving Average Trajectory   │  │ - Laspeyres Index (I_L)      │
│  - Anomaly & Fake-Discount Detection │  │ - Cross-Store Price Spreads  │
└───────────────────┬──────────────────┘  └──────────────┬───────────────┘
                    │                                    │
                    ▼                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                Executive Excel Reporting (OpenPyXL)                    │
│         Color-coded Deal Badges, Price Spread Alerts & KPI Charts      │
└────────────────────────────────────────────────────────────────────────┘
```

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 📐 Algorithmic Formulation & Pricing Models

### 1. Laspeyres Competitor Basket Price Index
To quantify overall competitor basket price shifts relative to base period $t=0$:

$$I_L = \frac{\sum_{i=1}^M p_{i,t} \cdot q_{i,0}}{\sum_{i=1}^M p_{i,0} \cdot q_{i,0}} \times 100$$

Where $p_{i,t}$ is the price of product $i$ at time $t$ and $q_{i,0}$ is the baseline product weight.

### 2. Deal Quality Scoring & Fake Discount Detection
Given current price $p_t$, list price $p_{\text{list}}$, and historical 30-day mean price $\bar{p}_{30}$:

$$\text{True Discount Ratio: } D_{\text{true}} = \frac{\bar{p}_{30} - p_t}{\bar{p}_{30}}$$

$$\text{Classification: } \begin{cases}
\text{FAKE DISCOUNT} & \text{if } p_{\text{list}} > \bar{p}_{30} \text{ and } p_t \ge \bar{p}_{30} \\
\text{EXCELLENT DEAL} & \text{if } D_{\text{true}} \ge 0.15 \text{ and } p_t < \min(p_{\text{history}}) \\
\text{FAIR PRICE} & \text{otherwise}
\end{cases}$$

### 3. Predictive Linear Trend Slope
Using least-squares regression over the past $N$ observations:

$$m = \frac{N \sum (t \cdot p_t) - \sum t \sum p_t}{N \sum t^2 - (\sum t)^2}, \quad p_{\text{forecast}}(t + \Delta t) = p_t + m \cdot \Delta t$$

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 🛠️ Technology Stack

| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Scraper Core** | Python 3.10+ | Requests, BeautifulSoup4, HTTP adapter retries |
| **High-Speed Fetcher**| Go (Golang 1.22+) | Concurrent HTTP worker pool for high-volume catalogs |
| **Storage** | SQLite3 | Local, zero-configuration relational persistence |
| **Analytics** | NumPy & Pandas | Price velocity calculation and Laspeyres basket indexing |
| **Reporting** | OpenPyXL | Stylized Excel reporting with color-coded conditional badges |

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 📂 Repository Structure

```text
ecommerce-price-tracker/
├── competitor_basket_index.py  # Laspeyres basket inflation & cross-store indexing
├── market_data.db              # SQLite relational product database
├── market_price_report.xlsx    # Sample generated executive Excel report
├── price_trend_forecaster.py   # 7-day linear price forecasting & deal scoring
├── README.md                   # Master engineering documentation
├── requirements.txt            # Python dependencies
├── scraper.py                  # Primary Python scraping and data extraction pipeline
└── fast_fetcher_go/
    ├── go.mod                  # Go module definition
    └── main.go                 # High-concurrency Go HTTP worker pool
```

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 🗄️ Database Schema

```sql
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_title TEXT NOT NULL,
    current_price REAL NOT NULL,
    original_price REAL,
    discount_percent REAL,
    seller_name TEXT,
    rating REAL,
    stock_status TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_title ON products(product_title);
CREATE INDEX idx_products_timestamp ON products(timestamp);
```

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 🚀 Quickstart & Installation

### Prerequisites
- Python `3.10+` installed
- Go `1.20+` (optional, for high-speed fetcher)

### Setup Instructions
```bash
# 1. Clone repository
git clone https://github.com/ArdavanGhal-Eh/ecommerce-price-tracker.git
cd ecommerce-price-tracker

# 2. Create virtual environment & install requirements
python -m venv venv
source venv/bin/activate   # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 💻 CLI Reference & Usage Guide

### 1. Crawl Listings & Persist to SQLite
```bash
python scraper.py --query "laptop" --pages 3 --export-excel
```

### 2. Run 7-Day Predictive Forecaster & Deal Quality Analyzer
```bash
python price_trend_forecaster.py --db market_data.db --min-discount 10
```

### 3. Compute Competitor Basket Inflation Index
```bash
python competitor_basket_index.py --base-date 2026-09-01 --current-date 2026-10-01
```

### 4. Running the High-Speed Go Fetcher
```bash
cd fast_fetcher_go
go run main.go -workers 16 -input urls.txt
```

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 🗺️ Roadmap & Future Enhancements

- [x] Resilient multi-page Python scraper with retry adapters
- [x] High-concurrency Go worker pool
- [x] Laspeyres basket price inflation index
- [x] 7-day predictive price trend forecaster
- [x] Automated OpenPyXL Excel reporting with deal badges
- [ ] Headless Playwright / Selenium support for dynamic JS hydration
- [ ] Telegram Bot webhook integration for instantaneous price drop alerts
- [ ] Docker containerized daily cron scheduler

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 🤝 Contributing & License

Contributions, bug reports, and optimizations are welcome! Feel free to open an issue or submit a Pull Request.

Distributed under the **MIT License**. See `LICENSE` for details.

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 👤 Author & Contact

**Ardavan Ghal-Eh**  
*Department of Mechanical Engineering, Sharif University of Technology*  
- **GitHub:** [@ArdavanGhal-Eh](https://github.com/ArdavanGhal-Eh)
- **Profile:** [github.com/ArdavanGhal-Eh](https://github.com/ArdavanGhal-Eh)

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>
