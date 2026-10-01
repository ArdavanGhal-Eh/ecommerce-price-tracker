# 🛒 Advanced E-Commerce Price & Market Intelligence Engine

A modular, production-ready Python scraping & market intelligence pipeline for tracking competitor prices, automated deal scoring, price-drop alerts, and inventory analytics across e-commerce marketplaces.

---

## 🌟 Key Features
- **Automated Deal Scoring Engine:** Evaluates price fluctuations to classify items into *Great Deal*, *Fair Deal*, or *Standard Pricing*.
- **Price-Drop Event Triggers:** Detects significant drops (>=15%) and logs structured alert records in SQLite for downstream messaging/webhook distribution.
- **Automated CI/CD Testing (GitHub Actions):** Fully integrated `.github/workflows/ci.yml` pipeline testing the entire scraping and database ingestion workflow on every push.
- **Intelligent Anti-Bot Rotation:** Uses random user-agent rotation, dynamic headers, and exponential backoff retry mechanisms.
- **Dual Persistence:** Automatically generates dual outputs: a normalized SQLite database and an executive-ready `.xlsx` spreadsheet.

---

## 🎯 Real-World Applications & Cross-Industry Impact

### ⚙️ E-Commerce & Retail Supply Chain
* **Dynamic Repricing Automation:** Providing real-time price intelligence feeds to automated algorithmic repricers.
* **Competitor Monitoring:** Tracking promotions, flash sales, and inventory stockouts across competitors.

### 🌐 Cross-Industry & Data Engineering
* **Financial Arbitrage & Inflation Tracking:** Quantifying micro-level price indices across consumer electronics categories.
* **Lead Generation & Market Analytics:** Gathering structured product catalogs for market research firms.

---

## 🚀 Installation & Setup

1. **Clone repository:**
   ```bash
   git clone https://github.com/ArdavanGhal-Eh/ecommerce-price-tracker.git
   cd ecommerce-price-tracker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run pipeline:**
   ```bash
   python scraper.py --category "Digital-Electronics" --output "market_price_report.xlsx"
   ```

---

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **HTTP & Parsing:** `requests`, `BeautifulSoup4`, `lxml`
- **Data Engineering:** `pandas`, `openpyxl`
- **Database:** `sqlite3`
- **CI/CD:** GitHub Actions

---

## 👨‍💻 Author
**Ardavan Ghal-Eh**  
Mechanical Engineering Student, Sharif University of Technology  
*Focus: Data Pipelines, Automation & Industrial Computing*
