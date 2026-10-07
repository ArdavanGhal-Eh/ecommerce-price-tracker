<a id="readme-top"></a>

<div align="center">

[![English Documentation](https://img.shields.io/badge/Documentation-English-blue.svg?style=for-the-badge)](README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Go Worker](https://img.shields.io/badge/Go-Fast_Fetcher-00ADD8.svg?style=for-the-badge&logo=go&logoColor=white)](https://golang.org/)
[![Storage](https://img.shields.io/badge/Database-SQLite3-003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Reporting](https://img.shields.io/badge/Reporting-OpenPyXL-217346.svg?style=for-the-badge&logo=microsoft-excel&logoColor=white)](https://openpyxl.readthedocs.io/)

<br />

# 🛒 سامانه هوشمند رصد و تحلیل قیمت‌های تجارت الکترونیک (E-Commerce Price Intelligence)
### *موتور خزش وب با همزمانی بالا، امتیازدهی الگوریتمی تخفیف‌ها و پیش‌بینی روندهای قیمتی ۷ روزه با Python و Go*

<p align="center">
  <b>موتور تحلیل رقابتی در مقیاس صنعتی برای پایش لحظه‌ای و همزمان فروشگاه‌های بزرگ اینترنتی (نظیر دیجی‌کالا، ترب، ایمالز، آمازون). این معماری ترکیبی از خزشگر پایتون و کارگران همزمان سریع Go، ذخیره‌سازی داده‌های طولی در SQLite، ارزیابی تورم سبد کالا با شاخص لاسپیرز (Laspeyres Index)، پیش‌بینی سری‌های زمانی قیمت و گزارش‌گیری تحلیلی خودکار در اکسل است.</b>
  <br /><br />
  <a href="#-معماری-سیستم-و-خط-لوله-داده"><strong>معماری خط لوله داده »</strong></a>
  &nbsp;•&nbsp;
  <a href="#-مدل‌های-ریاضی-و-فرمولاسیون-الگوریتمی"><strong>فرمولاسیون ریاضی قیمت »</strong></a>
  &nbsp;•&nbsp;
  <a href="#-راهنمای-نصب-و-راه‌اندازی-سریع"><strong>راه‌اندازی سریع »</strong></a>
</p>

</div>

---

<details open>
  <summary><h2 style="display: inline-block;">📑 فهرست مطالب</h2></summary>
  <ol>
    <li><a href="#-چکیده-اجرایی-و-مسئله-مهندسی">چکیده اجرایی و مسئله مهندسی</a></li>
    <li><a href="#-قابلیت‌ها-و-ویژگی‌های-محوری">قابلیت‌ها و ویژگی‌های محوری</a></li>
    <li><a href="#-معماری-سیستم-و-خط-لوله-داده">معماری سیستم و خط لوله داده</a></li>
    <li><a href="#-مدل‌های-ریاضی-و-فرمولاسیون-الگوریتمی">مدل‌های ریاضی و فرمولاسیون الگوریتمی</a></li>
    <li><a href="#-پشته-فناوری">پشته فناوری (Technology Stack)</a></li>
    <li><a href="#-ساختار-مخزن">ساختار مخزن</a></li>
    <li><a href="#-طرح‌واره-پایگاه-داده-sqlite">طرح‌واره پایگاه داده (SQLite Schema)</a></li>
    <li><a href="#-راهنمای-نصب-و-راه‌اندازی-سریع">راهنمای نصب و راه‌اندازی سریع</a></li>
    <li><a href="#-مرجع-دستورات-cli">مرجع دستورات CLI</a></li>
    <li><a href="#-مسیر-توسعه-آتی">مسیر توسعه آتی</a></li>
    <li><a href="#-مجوز-و-مشارکت">مجوز و مشارکت</a></li>
  </ol>
</details>

---

## 📌 چکیده اجرایی و مسئله مهندسی

در اکوسیستم‌های رقابتی خرده‌فروشی آنلاین و پلتفرم‌های چندفروشگاهی، نوسانات آنی قیمت و تخفیف‌های ساختگی یکی از چالش‌های بنیادین خریداران و مدیران مارکتینگ است. این سامانه با هدف حل چالش‌های زیر پیاده‌سازی شده است:
1. **خزش همزمان مقاوم (High-Concurrency Resilient Crawling):** استخراج قیمت از صدها کالا در ثانیه بدون بلاک شدن از طریق کارگران ناهمگام و مدیریت صف Go Routines.
2. **کشف تقلب و اصالت تخفیف (Discount Fraud Detection):** محاسبه میانگین متحرک وزنی و انحراف معیار قیمت‌های ۳۰ روزه برای شناسایی قیمت‌گذاری‌های فریبنده پیش از حراجی‌ها.
3. **پیش‌بینی کمینه‌های قیمتی آینده:** استفاده از رگرسیون بردار پشتیبان و تحلیل روند هولت-وینترز جهت تخمین زمان بهینه برای خرید.

---

## 🚀 قابلیت‌ها و ویژگی‌های محوری

- **معماری تلفیقی دو زبانه (Python + Go):** منطق هوش مصنوعی و بصری‌سازی با Python 3.10+ و هسته دانلود شبکه‌ای فوق‌سریع با Go Goroutines.
- **پایداری داده‌های طولی (Longitudinal Price Tracking):** ایجاد تاریخچه دقیق تغییرات قیمت با کلیدهای خارجی و ایندکس‌گذاری بهینه در SQLite3.
- **شاخص تورمی لاسپیرز (Laspeyres Basket Inflation):** محاسبه نرخ رشد واقعی قیمت یک سبد کالایی ثابت در طول بازه‌های زمانی ماهانه و فصلی.
- **تولید گزارش‌های حرفه‌ای Excel با OpenPyXL:** خروجی خودکار با فرمت‌بندی شرطی (Conditional Formatting)، نمودارهای توکار درون‌سلولی و برچسب‌های خرید طلایی (Golden Deal Badges).

---

## 🏗 معماری سیستم و خط لوله داده

```
[Target URLs / Product Registry]
               │
               ▼
   [Go Concurrent Fetcher] ─── (HTTP Keep-Alive / Proxy Rotation)
               │
               ▼ (Raw JSON / HTML Payloads)
    [Python Parsing & Extraction Engine]
               │
         ┌─────┴────────────────┐
         ▼                      ▼
[SQLite Storage Engine]    [Pricing Analytics Core]
(Historical Time-Series)    ├─ Laspeyres Price Index
                            ├─ Anomaly & Pseudo-Discount Filter
                            └─ 7-Day ARIMA/Regression Trend
                                        │
                                        ▼
                         [OpenPyXL Automated Reports]
                         (Executive XLSX + Visual Badges)
```

---

## 📐 مدل‌های ریاضی و فرمولاسیون الگوریتمی

### ۱. شاخص قیمت لاسپیرز (Laspeyres Price Index)
برای سنجش تغییرات کلی قیمت سبد کالایی در زمان $t$ نسبت به زمان مبنا $0$:
$$I_L = \frac{\sum_{i=1}^{n} P_{i,t} \cdot Q_{i,0}}{\sum_{i=1}^{n} P_{i,0} \cdot Q_{i,0}} \times 100$$
که در آن $P_{i,t}$ قیمت کالای $i$ در زمان جاری و $Q_{i,0}$ وزن پایه کالا است.

### ۲. امتیاز اصالت تخفیف (Deal Authenticity Score - DAS)
$$DAS_i = \frac{\mu_{30}(P_i) - P_{i,t}}{\sigma_{30}(P_i)}$$
- اگر $DAS_i > 2.0$: تخفیف فوق‌العاده واقعی (بیش از دو انحراف معیار زیر میانگین تاریخی).
- اگر $DAS_i \approx 0$: قیمت معمولی و بدون تخفیف موثر.
- اگر قیمت پایه پیش از تخفیف به طور ناگهانی افزایش یافته باشد، پرچم تقلب (Fake Discount Flag) فعال می‌گردد.

---

## 💻 پشته فناوری (Technology Stack)

| بخش | فناوری / کتابخانه | هدف و کاربرد |
| :--- | :--- | :--- |
| **هسته خزش همزمان** | Go 1.21+ / Goroutines | دانلود با همروندی بالا، مصرف ناچیز رم |
| **استخراج و تحلیل داده** | Python 3.10+, BeautifulSoup4 | تجزیه ساختار HTML/DOM و استخراج داده‌های معنایی |
| **پایگاه داده** | SQLite3 | ذخیره‌سازی محلی سریع و سبک تاریخچه قیمت‌ها |
| **گزارش‌گیری** | OpenPyXL | تولید شیت‌های پیشرفته اکسل با فرمت‌بندی شرطی |

---

## 📂 ساختار مخزن

```
01-ecommerce-price-tracker/
├── scraper.py            # هسته استخراج و خزش در پایتون
├── fetcher.go            # کارگر همزمان Go برای دانلود با فرکانس بالا
├── database.py           # ارتباط با پایگاه داده SQLite و تعاریف Schema
├── analytics.py          # پیاده‌سازی شاخص‌های لاسپیرز و الگوریتم‌های DAS
├── report_generator.py   # تولید گزارش‌های پیشرفته اکسل
├── requirements.txt      # پیش‌نیازهای پایتونی
├── README.md             # مستندات انگلیسی
└── README_FA.md          # مستندات جامع دانشگاهی فارسی
```

---

## ⚙️ راهنمای نصب و راه‌اندازی سریع

### ۱. راه‌اندازی محیط پایتون
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### ۲. اجرای پایپ‌لاین رصد قیمت
```bash
python scraper.py --config config.json --run-analysis --export-excel
```

---

## 📄 مجوز
این پروژه تحت مجوز [MIT](https://opensource.org/licenses/MIT) منتشر شده است.
