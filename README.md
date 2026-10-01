# 🛒 Hybrid E-Commerce Price & Market Intelligence Engine (Python + Go)

A production-ready polyglot architecture combining a **Go-powered concurrent HTTP fetcher** for multi-threaded crawling with a **Python analytics core** for deal scoring and Excel reporting.

## 🌟 Polyglot Architecture
- **Go Concurrent Fetcher (`fast_fetcher_go/`):** High-speed parallel crawler bypassing Python GIL.
- **Python Intelligence Core (`scraper.py`):** Algorithmic deal scoring and structured Excel reporting.
- **CI/CD (`.github/workflows/ci.yml`):** Automated tests for both Python and Go on every commit.

## 🎯 Real-World Applications & Cross-Industry Impact
### ⚙️ E-Commerce & Supply Chain
- Parallel price scraping across large retail marketplaces for dynamic repricers.
### 🌐 Cross-Industry & Data Engineering
- Real-time tick data ingestion for financial arbitrage and micro-inflation indices.

## 🚀 Execution
```bash
# Go Fast Fetcher:
cd fast_fetcher_go && go run main.go

# Python Analytics:
pip install -r requirements.txt && python scraper.py
```

## 👨‍💻 Author
**Ardavan Ghal-Eh** | Sharif University of Technology
