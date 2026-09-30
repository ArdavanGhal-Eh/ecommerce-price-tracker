# 🛒 Automated E-Commerce Price & Market Data Scraper

A modular, production-ready Python scraping pipeline for tracking competitor prices, inventory availability, and product discounts across e-commerce marketplaces.

---

## 🌟 Key Features
- **Intelligent Scraping & Backoff:** Uses random user-agent rotation, dynamic request headers, and exponential backoff retry mechanisms to prevent rate limits.
- **Relational Persistence (SQLite):** Automatically creates tables and logs historical snapshots of product prices and availability over time.
- **Automated Excel Export:** Formats extracted records into clean, business-ready `.xlsx` spreadsheets with Persian and English column mappings using `Pandas` and `openpyxl`.
- **CLI & Demo Mode:** Supports instant execution with realistic simulation data as well as live target website parsing.

---

## 🚀 Installation & Setup

1. **Clone repository:**
   ```bash
   git clone https://github.com/your-username/ecommerce-price-tracker.git
   cd ecommerce-price-tracker
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

Run the data extraction pipeline:
```bash
python scraper.py --category "Digital-Electronics" --output "market_price_report.xlsx"
```

### CLI Arguments
- `--category`: Target product category (default: `Digital-Electronics`).
- `--output`: Name of generated Excel file (default: `market_price_report.xlsx`).
- `--db`: SQLite database file path (default: `market_data.db`).

---

## 📊 Sample Output Schema
| عنوان کالا (Title) | دسته‌بندی (Category) | قیمت نهایی (Price) | تخفیف (Discount) | وضعیت موجودی (Stock) | فروشنده (Seller) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| لپ‌تاپ 15.6 اینچی ایسوس | Electronics | 42,500,000 تومان | 10% | موجود | بازرگانی پارس تک |

---

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **HTTP & Parsing:** `requests`, `BeautifulSoup4`, `lxml`
- **Data Engineering:** `pandas`, `openpyxl`
- **Database:** `sqlite3`

---

## 👨‍💻 Author
**Ardavan Ghal-eh**  
Mechanical Engineering Student, Sharif University of Technology  
*Specialized in Python Automation & Industrial Computing*
