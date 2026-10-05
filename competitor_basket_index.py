"""
Multi-Item Competitor Basket Inflation & Price Elasticity Index Module
Part of Automated E-Commerce Price Intelligence Suite
Author: Ardavan Ghal-Eh | Sharif University of Technology
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any


class CompetitorBasketIndex:
    """
    Computes economic price indices (Laspeyres, Paasche, Fisher) across multi-item
    product baskets to detect macro category inflation vs vendor-specific discounts.
    """

    def __init__(self, base_period_label: str = "T0"):
        self.base_period_label = base_period_label

    def compute_basket_indices(
        self,
        basket_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        basket_items: list of dicts with:
        {'title': 'ASUS Laptop', 'p0': 38_000_000, 'q0': 10, 'p1': 41_500_000, 'q1': 12, 'category': 'Laptops'}
        """
        sum_p0_q0 = 0.0
        sum_p1_q0 = 0.0
        sum_p1_q1 = 0.0
        sum_p0_q1 = 0.0

        category_analysis = {}

        for item in basket_items:
            p0 = item['p0']
            q0 = item['q0']
            p1 = item['p1']
            q1 = item['q1']
            cat = item.get('category', 'General')

            sum_p0_q0 += p0 * q0
            sum_p1_q0 += p1 * q0
            sum_p1_q1 += p1 * q1
            sum_p0_q1 += p0 * q1

            if cat not in category_analysis:
                category_analysis[cat] = {'p0_total': 0.0, 'p1_total': 0.0, 'count': 0}
            category_analysis[cat]['p0_total'] += p0
            category_analysis[cat]['p1_total'] += p1
            category_analysis[cat]['count'] += 1

        # Laspeyres Price Index (Base-weighted)
        laspeyres = (sum_p1_q0 / sum_p0_q0) * 100.0 if sum_p0_q0 > 0 else 100.0

        # Paasche Price Index (Current-weighted)
        paasche = (sum_p1_q1 / sum_p0_q1) * 100.0 if sum_p0_q1 > 0 else 100.0

        # Fisher Ideal Index (Geometric mean)
        fisher = np.sqrt(laspeyres * paasche)

        inflation_rate_pct = fisher - 100.0

        category_inflation = {}
        for cat, val in category_analysis.items():
            cat_inf = ((val['p1_total'] - val['p0_total']) / val['p0_total']) * 100.0 if val['p0_total'] > 0 else 0.0
            category_inflation[cat] = round(cat_inf, 2)

        # Market trend status
        if inflation_rate_pct > 5.0:
            status = "🔴 تورم ساختاری دسته کالا (Macro Inflation Surge)"
            action = "افزایش قیمت فروش هماهنگ با بازار جهت حفظ حاشیه سود"
        elif inflation_rate_pct < -3.0:
            status = "🟢 موج تخفیفات تهاجمی رقبا (Aggressive Price War)"
            action = "نیاز به مذاکره با تأمین‌کننده یا تنظیم آفر تخفیف موقت"
        else:
            status = "🟡 پایداری نسبی سبد قیمت (Market Stability)"
            action = "تداوم رصد روتین هفتگی بدون نیاز به اصلاحات فوری"

        return {
            "laspeyres_index": round(laspeyres, 2),
            "paasche_index": round(paasche, 2),
            "fisher_ideal_index": round(fisher, 2),
            "basket_inflation_rate_percent": round(inflation_rate_pct, 2),
            "category_inflation_breakdown": category_inflation,
            "market_verdict": status,
            "recommended_strategy": action
        }


def run_demo_basket():
    analyzer = CompetitorBasketIndex()
    sample_basket = [
        {"title": "لپ‌تاپ ایسوس Vivobook 15", "p0": 38_500_000, "q0": 15, "p1": 41_200_000, "q1": 14, "category": "Laptops"},
        {"title": "مک‌بوک ایر اپل M2", "p0": 89_000_000, "q0": 8, "p1": 94_500_000, "q1": 7, "category": "Laptops"},
        {"title": "گوشی سامسونگ S24 Ultra", "p0": 72_000_000, "q0": 20, "p1": 71_500_000, "q1": 22, "category": "Mobile"},
        {"title": "مانیتور شیائومی 27 اینچ 165Hz", "p0": 14_200_000, "q0": 30, "p1": 15_800_000, "q1": 28, "category": "Monitors"}
    ]

    res = analyzer.compute_basket_indices(sample_basket)

    print("=" * 65)
    print("📊 شاخص تورم سبد رقبا و تحلیل کشش قیمت (Laspeyres / Fisher):")
    print("=" * 65)
    print(f"شاخص لاسپیرز (Laspeyres): {res['laspeyres_index']}")
    print(f"شاخص فیشر (Fisher Ideal): {res['fisher_ideal_index']}")
    print(f"نرخ تورم تجمیعی سبد کالا: {res['basket_inflation_rate_percent']}%")
    print(f"تفکیک تورم به دسته‌ها: {res['category_inflation_breakdown']}")
    print(f"تحلیل وضعیت بازار: {res['market_verdict']}")
    print(f"راهبرد پیشنهادی: {res['recommended_strategy']}")
    print("=" * 65)


if __name__ == "__main__":
    run_demo_basket()
