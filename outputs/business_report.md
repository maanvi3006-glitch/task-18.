# Market Basket Analysis — Business Report
*Generated 2026-09-06 05:20 · Algorithm: apriori · min_support=0.005, min_confidence=0.25, min_lift=1.15*

## 1. Executive Summary

- Analysed **5,197** transactions across **64** unique items.
- After mining and filtering, **64** vetted, actionable rules were retained (27 flagged **Noteworthy**, 37 flagged **Obvious/known**).
- Proposed **3** concrete cross-sell bundles from the strongest rules.
- Estimated combined incremental revenue opportunity across the top rules: **$3,939** over the analysis period (see methodology note below — this is a clearly-labelled, conservative estimate meant to prioritise action, not a guarantee).

## 2. Data Quality Notes (validation performed before analysis)

- Rows: 21124 in → 20983 out after cleaning.
- Transactions: 5200 in → 5197 out.
- Basket size: mean **4.04** items, median **4**, max **14**.
  - ⚠️ Dropped 63 row(s) with blank/invalid item names (likely scanner errors).
  - ⚠️ Removed 78 duplicate line-item scan(s) (same item scanned twice in the same basket).
  - ⚠️ 449 transaction(s) (8.6%) have fewer than 2 distinct item(s) and cannot contribute association rules on their own.

## 3. Algorithm Choice: Apriori vs FP-Growth

Both algorithms were run on the identical encoded transaction matrix at the same `min_support` threshold, to make the comparison fair:

| Algorithm | Runtime (s) | Frequent itemsets found | Max itemset size |
|---|---|---|---|
| apriori | 0.1278 | 925 | 4 |
| fpgrowth | 0.0855 | 925 | 4 |

**Recommendation:** at this dataset scale both return identical itemsets (same support definition), so the choice comes down to runtime. FP-Growth avoids Apriori's candidate-generation step and typically scales better as the item catalog and basket sizes grow; Apriori is simpler to reason about and debug at small scale. For a catalog this size (tens of items), the difference is marginal — but FP-Growth is the safer default if the catalog grows into the thousands of SKUs.

## 4. Answering the Brief's Brainstorming Questions

**Which rule is obvious vs genuinely surprising and valuable?** Most top-lift rules here are intuitive (pasta + pasta sauce, peanut butter + jam) — real, but not news to a merchandiser. The genuinely non-obvious finding is:

> **Diapers Pack → Beer 6-Pack** (confidence 31%, lift 3.80). This pairing has no obvious shelf-logic reason to co-occur, which is exactly what makes it worth a merchandising team's attention — the classic 'diapers & beer' style insight: a behavioural pattern (e.g. a parent sent shopping) rather than a culinary one.

**What's the dollar impact of acting on the top rule?** The top-ranked rule (**Spaghetti → Tomato Pasta Sauce**) has an estimated incremental revenue opportunity of **$12** over the analysis period, under the conservative capture-rate assumption described below.

**How do you avoid recommending things people already buy together anyway?** Every rule below is explicitly tagged `Obvious` or `Noteworthy` (see methodology in `business_interpretation.py: classify_novelty`), so a stakeholder can filter straight to the non-obvious findings rather than re-discovering common sense.

## 5. Vetted Association Rules — Business Interpretation

Full detail is given for the top 15 rules by **actionability score** (a blend of lift, support, and confidence — see methodology note). The remaining vetted rules that cleared all thresholds are listed in the appendix table for completeness and are also available in full in `rules_filtered_vetted.csv`.

### Rule 1: Spaghetti → Tomato Pasta Sauce  `[Obvious (known pattern)]`
- **Support:** 0.015  ·  **Confidence:** 79.6%  ·  **Lift:** 16.16  ·  **Actionability score:** 8.61
- **Business insight:** Customers who buy **Spaghetti** buy **Tomato Pasta Sauce** 80% of the time — that's 16.16x more often than if the two were unrelated (lift=16.16). Closing this gap for even a fraction of missed baskets could add roughly **$12** in incremental revenue over the analysis period.
- **Recommended action:** High priority: co-locate Tomato Pasta Sauce next to Spaghetti, or bundle them at a small discount; this is a strong, reliable pattern.

### Rule 2: Penne → Tomato Pasta Sauce  `[Obvious (known pattern)]`
- **Support:** 0.015  ·  **Confidence:** 66.9%  ·  **Lift:** 13.59  ·  **Actionability score:** 8.38
- **Business insight:** Customers who buy **Penne** buy **Tomato Pasta Sauce** 67% of the time — that's 13.59x more often than if the two were unrelated (lift=13.59). Closing this gap for even a fraction of missed baskets could add roughly **$24** in incremental revenue over the analysis period.
- **Recommended action:** High priority: co-locate Tomato Pasta Sauce next to Penne, or bundle them at a small discount; this is a strong, reliable pattern.

### Rule 3: Diapers Pack → Baby Wipes  `[Noteworthy]`
- **Support:** 0.012  ·  **Confidence:** 71.1%  ·  **Lift:** 25.31  ·  **Actionability score:** 8.08
- **Business insight:** Customers who buy **Diapers Pack** buy **Baby Wipes** 71% of the time — that's 25.31x more often than if the two were unrelated (lift=25.31). Closing this gap for even a fraction of missed baskets could add roughly **$24** in incremental revenue over the analysis period.
- **Recommended action:** High priority: co-locate Baby Wipes next to Diapers Pack, or bundle them at a small discount; this is a strong, reliable pattern.

### Rule 4: Parmesan Cheese, Tomato Pasta Sauce → Spaghetti  `[Obvious (known pattern)]`
- **Support:** 0.006  ·  **Confidence:** 100.0%  ·  **Lift:** 53.03  ·  **Actionability score:** 7.85
- **Business insight:** Customers who buy **Parmesan Cheese, Tomato Pasta Sauce** buy **Spaghetti** 100% of the time — that's 53.03x more often than if the two were unrelated (lift=53.03).
- **Recommended action:** High priority: co-locate Spaghetti next to Parmesan Cheese, Tomato Pasta Sauce, or bundle them at a small discount; this is a strong, reliable pattern.

### Rule 5: Parmesan Cheese, Spaghetti → Tomato Pasta Sauce  `[Obvious (known pattern)]`
- **Support:** 0.006  ·  **Confidence:** 100.0%  ·  **Lift:** 20.30  ·  **Actionability score:** 7.85
- **Business insight:** Customers who buy **Parmesan Cheese, Spaghetti** buy **Tomato Pasta Sauce** 100% of the time — that's 20.3x more often than if the two were unrelated (lift=20.3).
- **Recommended action:** High priority: co-locate Tomato Pasta Sauce next to Parmesan Cheese, Spaghetti, or bundle them at a small discount; this is a strong, reliable pattern.

### Rule 6: Peanut Butter → Strawberry Jam  `[Obvious (known pattern)]`
- **Support:** 0.013  ·  **Confidence:** 50.0%  ·  **Lift:** 14.93  ·  **Actionability score:** 7.73
- **Business insight:** Customers who buy **Peanut Butter** buy **Strawberry Jam** 50% of the time — that's 14.93x more often than if the two were unrelated (lift=14.93). Closing this gap for even a fraction of missed baskets could add roughly **$48** in incremental revenue over the analysis period.
- **Recommended action:** High priority: co-locate Strawberry Jam next to Peanut Butter, or bundle them at a small discount; this is a strong, reliable pattern.

### Rule 7: Tomato Pasta Sauce → Penne  `[Obvious (known pattern)]`
- **Support:** 0.015  ·  **Confidence:** 30.9%  ·  **Lift:** 13.59  ·  **Actionability score:** 7.66
- **Business insight:** Customers who buy **Tomato Pasta Sauce** buy **Penne** 31% of the time — that's 13.59x more often than if the two were unrelated (lift=13.59). Closing this gap for even a fraction of missed baskets could add roughly **$67** in incremental revenue over the analysis period.
- **Recommended action:** Feature 'Penne' in a 'frequently bought with Tomato Pasta Sauce' recommendation slot online and on receipts.

### Rule 8: BBQ Sauce, Charcoal Bag, Ground Beef → Burger Buns  `[Obvious (known pattern)]`
- **Support:** 0.005  ·  **Confidence:** 96.6%  ·  **Lift:** 30.05  ·  **Actionability score:** 7.66
- **Business insight:** Customers who buy **BBQ Sauce, Charcoal Bag, Ground Beef** buy **Burger Buns** 97% of the time — that's 30.05x more often than if the two were unrelated (lift=30.05). Closing this gap for even a fraction of missed baskets could add roughly **$1** in incremental revenue over the analysis period.
- **Recommended action:** High priority: co-locate Burger Buns next to BBQ Sauce, Charcoal Bag, Ground Beef, or bundle them at a small discount; this is a strong, reliable pattern.

### Rule 9: Charcoal Bag, Ground Beef → Burger Buns  `[Obvious (known pattern)]`
- **Support:** 0.006  ·  **Confidence:** 89.2%  ·  **Lift:** 27.76  ·  **Actionability score:** 7.64
- **Business insight:** Customers who buy **Charcoal Bag, Ground Beef** buy **Burger Buns** 89% of the time — that's 27.76x more often than if the two were unrelated (lift=27.76). Closing this gap for even a fraction of missed baskets could add roughly **$2** in incremental revenue over the analysis period.
- **Recommended action:** High priority: co-locate Burger Buns next to Charcoal Bag, Ground Beef, or bundle them at a small discount; this is a strong, reliable pattern.

### Rule 10: Burger Buns, Ketchup → Ground Beef  `[Obvious (known pattern)]`
- **Support:** 0.007  ·  **Confidence:** 100.0%  ·  **Lift:** 9.45  ·  **Actionability score:** 7.63
- **Business insight:** Customers who buy **Burger Buns, Ketchup** buy **Ground Beef** 100% of the time — that's 9.45x more often than if the two were unrelated (lift=9.45).
- **Recommended action:** High priority: co-locate Ground Beef next to Burger Buns, Ketchup, or bundle them at a small discount; this is a strong, reliable pattern.

### Rule 11: Tomato Pasta Sauce → Spaghetti  `[Obvious (known pattern)]`
- **Support:** 0.015  ·  **Confidence:** 30.5%  ·  **Lift:** 16.16  ·  **Actionability score:** 7.63
- **Business insight:** Customers who buy **Tomato Pasta Sauce** buy **Spaghetti** 30% of the time — that's 16.16x more often than if the two were unrelated (lift=16.16). Closing this gap for even a fraction of missed baskets could add roughly **$68** in incremental revenue over the analysis period.
- **Recommended action:** Feature 'Spaghetti' in a 'frequently bought with Tomato Pasta Sauce' recommendation slot online and on receipts.

### Rule 12: BBQ Sauce, Burger Buns → Charcoal Bag  `[Noteworthy]`
- **Support:** 0.006  ·  **Confidence:** 91.2%  ·  **Lift:** 41.20  ·  **Actionability score:** 7.63
- **Business insight:** Customers who buy **BBQ Sauce, Burger Buns** buy **Charcoal Bag** 91% of the time — that's 41.2x more often than if the two were unrelated (lift=41.2). Closing this gap for even a fraction of missed baskets could add roughly **$5** in incremental revenue over the analysis period.
- **Recommended action:** High priority: co-locate Charcoal Bag next to BBQ Sauce, Burger Buns, or bundle them at a small discount; this is a strong, reliable pattern.

### Rule 13: BBQ Sauce, Burger Buns, Ground Beef → Charcoal Bag  `[Obvious (known pattern)]`
- **Support:** 0.005  ·  **Confidence:** 93.3%  ·  **Lift:** 42.18  ·  **Actionability score:** 7.59
- **Business insight:** Customers who buy **BBQ Sauce, Burger Buns, Ground Beef** buy **Charcoal Bag** 93% of the time — that's 42.18x more often than if the two were unrelated (lift=42.18). Closing this gap for even a fraction of missed baskets could add roughly **$3** in incremental revenue over the analysis period.
- **Recommended action:** High priority: co-locate Charcoal Bag next to BBQ Sauce, Burger Buns, Ground Beef, or bundle them at a small discount; this is a strong, reliable pattern.

### Rule 14: Baby Wipes → Diapers Pack  `[Noteworthy]`
- **Support:** 0.012  ·  **Confidence:** 43.8%  ·  **Lift:** 25.31  ·  **Actionability score:** 7.53
- **Business insight:** Customers who buy **Baby Wipes** buy **Diapers Pack** 44% of the time — that's 25.31x more often than if the two were unrelated (lift=25.31). Closing this gap for even a fraction of missed baskets could add roughly **$244** in incremental revenue over the analysis period.
- **Recommended action:** High priority: co-locate Diapers Pack next to Baby Wipes, or bundle them at a small discount; this is a strong, reliable pattern.

### Rule 15: Strawberry Jam → Peanut Butter  `[Obvious (known pattern)]`
- **Support:** 0.013  ·  **Confidence:** 38.5%  ·  **Lift:** 14.93  ·  **Actionability score:** 7.50
- **Business insight:** Customers who buy **Strawberry Jam** buy **Peanut Butter** 39% of the time — that's 14.93x more often than if the two were unrelated (lift=14.93). Closing this gap for even a fraction of missed baskets could add roughly **$96** in incremental revenue over the analysis period.
- **Recommended action:** Feature 'Peanut Butter' in a 'frequently bought with Strawberry Jam' recommendation slot online and on receipts.

#### Appendix: remaining 49 vetted rules (ranked, summary form)

| # | Rule | Support | Confidence | Lift | Novelty |
|---|---|---|---|---|---|
| 16 | Burger Buns, Charcoal Bag, Ground Beef → BBQ Sauce | 0.005 | 84.8% | 29.59 | Obvious (known pattern) |
| 17 | BBQ Sauce, Burger Buns → Charcoal Bag, Ground Beef | 0.005 | 82.4% | 115.67 | Obvious (known pattern) |
| 18 | Charcoal Bag, Ground Beef → BBQ Sauce | 0.006 | 78.4% | 27.34 | Noteworthy |
| 19 | BBQ Sauce, Ground Beef → Burger Buns | 0.006 | 76.9% | 23.94 | Obvious (known pattern) |
| 20 | Charcoal Bag, Ground Beef → BBQ Sauce, Burger Buns | 0.005 | 75.7% | 115.67 | Obvious (known pattern) |
| 21 | BBQ Sauce, Ground Beef → Charcoal Bag | 0.006 | 74.4% | 33.60 | Noteworthy |
| 22 | Balloons Pack → Candles | 0.009 | 45.8% | 16.53 | Noteworthy |
| 23 | BBQ Sauce, Ground Beef → Burger Buns, Charcoal Bag | 0.005 | 71.8% | 77.73 | Obvious (known pattern) |
| 24 | Balloons Pack → Paper Plates | 0.009 | 44.9% | 13.71 | Noteworthy |
| 25 | Charcoal Bag → BBQ Sauce | 0.009 | 42.6% | 14.86 | Noteworthy |
| 26 | Burger Buns, Charcoal Bag → BBQ Sauce | 0.006 | 64.6% | 22.53 | Noteworthy |
| 27 | Charcoal Bag → Burger Buns | 0.009 | 41.7% | 12.99 | Noteworthy |
| 28 | BBQ Sauce, Charcoal Bag → Burger Buns | 0.006 | 63.3% | 19.69 | Noteworthy |
| 29 | Candles → Balloons Pack | 0.009 | 34.0% | 16.53 | Noteworthy |
| 30 | BBQ Sauce → Charcoal Bag | 0.009 | 32.9% | 14.86 | Noteworthy |
| 31 | Burger Buns, Charcoal Bag → BBQ Sauce, Ground Beef | 0.005 | 58.3% | 77.73 | Obvious (known pattern) |
| 32 | BBQ Sauce, Charcoal Bag → Burger Buns, Ground Beef | 0.005 | 57.1% | 37.12 | Obvious (known pattern) |
| 33 | Ground Beef, Ketchup → Burger Buns | 0.007 | 46.7% | 14.52 | Obvious (known pattern) |
| 34 | Burger Buns → Charcoal Bag | 0.009 | 28.7% | 12.99 | Noteworthy |
| 35 | Paper Plates → Balloons Pack | 0.009 | 28.2% | 13.71 | Noteworthy |
| 36 | BBQ Sauce, Burger Buns, Charcoal Bag → Ground Beef | 0.005 | 90.3% | 8.53 | Obvious (known pattern) |
| 37 | Burger Buns, Ground Beef → Ketchup | 0.007 | 43.8% | 13.30 | Obvious (known pattern) |
| 38 | BBQ Sauce, Burger Buns → Ground Beef | 0.006 | 88.2% | 8.34 | Obvious (known pattern) |
| 39 | Spaghetti, Tomato Pasta Sauce → Parmesan Cheese | 0.006 | 42.3% | 18.02 | Obvious (known pattern) |
| 40 | Baby Formula → Baby Food Jars | 0.007 | 38.9% | 16.17 | Noteworthy |
| 41 | Burger Buns, Ground Beef → Charcoal Bag | 0.006 | 41.2% | 18.64 | Obvious (known pattern) |
| 42 | Spaghetti → Parmesan Cheese | 0.006 | 33.7% | 14.34 | Noteworthy |
| 43 | Spaghetti → Parmesan Cheese, Tomato Pasta Sauce | 0.006 | 33.7% | 53.03 | Obvious (known pattern) |
| 44 | Burger Buns, Ground Beef → BBQ Sauce | 0.006 | 37.5% | 13.08 | Obvious (known pattern) |
| 45 | Baby Food Jars → Baby Formula | 0.007 | 28.0% | 16.17 | Noteworthy |
| 46 | Charcoal Bag → Burger Buns, Ground Beef | 0.006 | 28.7% | 18.64 | Obvious (known pattern) |
| 47 | Burger Buns, Ground Beef → BBQ Sauce, Charcoal Bag | 0.005 | 35.0% | 37.12 | Obvious (known pattern) |
| 48 | Parmesan Cheese → Spaghetti, Tomato Pasta Sauce | 0.006 | 27.0% | 18.02 | Obvious (known pattern) |
| 49 | Parmesan Cheese → Spaghetti | 0.006 | 27.0% | 14.34 | Noteworthy |
| 50 | Charcoal Bag → BBQ Sauce, Burger Buns | 0.006 | 27.0% | 41.20 | Noteworthy |
| 51 | Charcoal Bag → BBQ Sauce, Ground Beef | 0.006 | 25.2% | 33.60 | Noteworthy |
| 52 | Burger Buns, Charcoal Bag → Ground Beef | 0.006 | 68.8% | 6.50 | Obvious (known pattern) |
| 53 | Burger Buns → Ground Beef | 0.015 | 47.9% | 4.53 | Obvious (known pattern) |
| 54 | Cereal → Milk 1L | 0.022 | 28.5% | 3.03 | Obvious (known pattern) |
| 55 | Ketchup → Ground Beef | 0.014 | 43.9% | 4.14 | Noteworthy |
| 56 | Guacamole Dip, Salsa Dip → Tortilla Chips | 0.005 | 46.7% | 6.30 | Obvious (known pattern) |
| 57 | BBQ Sauce, Charcoal Bag → Ground Beef | 0.006 | 59.2% | 5.59 | Noteworthy |
| 58 | Parmesan Cheese → Tomato Pasta Sauce | 0.006 | 27.0% | 5.49 | Noteworthy |
| 59 | Guacamole Dip, Tortilla Chips → Salsa Dip | 0.005 | 37.8% | 4.25 | Obvious (known pattern) |
| 60 | Salsa Dip, Tortilla Chips → Guacamole Dip | 0.005 | 36.4% | 4.12 | Obvious (known pattern) |
| 61 | Diapers Pack → Beer 6-Pack | 0.005 | 31.1% | 3.80 | Noteworthy |
| 62 | Charcoal Bag → Ground Beef | 0.007 | 32.2% | 3.04 | Noteworthy |
| 63 | Peanut Butter → White Bread | 0.007 | 27.6% | 3.10 | Obvious (known pattern) |
| 64 | BBQ Sauce → Ground Beef | 0.008 | 26.2% | 2.47 | Noteworthy |

### Dollar-impact methodology (transparency note)
Estimated incremental revenue = (baskets containing the antecedent but missing the consequent) × (an assumed 20% capture rate from a nudge such as placement, bundling, or a recommendation) × (consequent price). The 20% capture rate is an explicit, conservative *assumption* — not a measured result — and should be replaced with real A/B test data once a rule is actioned.

## 6. Bundle & Cross-Sell Recommendations

| Bundle | Full Price | Bundle Price | Savings | Confidence | Lift | Rationale |
|---|---|---|---|---|---|---|
| BBQ Sauce + Burger Buns + Charcoal Bag + Ground Beef Bundle | $21.80 | $20.06 | $1.74 | 76% | 115.67 | Bought together 76% of the time when Charcoal Bag, Ground Beef is purchased, at 115.7x the baseline rate. |
| Parmesan Cheese + Spaghetti + Tomato Pasta Sauce Bundle | $11.50 | $10.58 | $0.92 | 100% | 53.03 | Bought together 100% of the time when Parmesan Cheese, Tomato Pasta Sauce is purchased, at 53.0x the baseline rate. |
| BBQ Sauce + Burger Buns + Charcoal Bag Bundle | $14.90 | $13.71 | $1.19 | 91% | 41.20 | Bought together 91% of the time when BBQ Sauce, Burger Buns is purchased, at 41.2x the baseline rate. |

## 7. Known Limitations & Pitfalls Actively Guarded Against

- **Basket-size effects:** larger baskets mechanically co-occur with more items; support/lift were computed on distinct-item baskets (duplicates removed) to avoid inflating counts.
- **Seasonality:** this dataset spans a full year; rules involving clearly seasonal items (e.g. BBQ charcoal + BBQ sauce) should be re-validated per-season rather than assumed constant year-round — a summer-only rule applied to a January promo calendar would under-deliver.
- **Redundant/subset rules** (a 3-item antecedent that adds nothing over its 2-item subset) were pruned automatically.
- **Rule overload** was avoided by capping the vetted list and ranking by actionability score rather than dumping every rule that cleared the statistical bar.
