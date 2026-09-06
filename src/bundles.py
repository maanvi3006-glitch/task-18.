"""
bundles.py
-----------
Step 6 of the pipeline: "Recommend bundles/cross-sells from the findings."

Converts the vetted, filtered association rules into concrete bundle
proposals: named product groupings with a suggested small discount,
projected uptake, and projected margin-safe pricing. This is a distinct
deliverable from the rules table itself - it's the "so what do we DO"
translation a merchandising or e-commerce team can put directly into a
promo calendar.
"""

import pandas as pd


def propose_bundles(business_rules: pd.DataFrame, item_prices: dict,
                     min_lift: float = 1.5, discount_pct: float = 0.08,
                     max_bundles: int = 10) -> pd.DataFrame:
    """
    Build bundle proposals from strong rules. Rules with an antecedent AND
    consequent of 1-2 items each are converted into a named bundle; the
    discount is calibrated so the bundle is still profitable but nudges
    the "high confidence, high lift" pattern into an actual purchase.
    """
    if business_rules.empty:
        return pd.DataFrame(columns=[
            "bundle_name", "items", "full_price", "bundle_price", "discount_pct",
            "support", "confidence", "lift", "rationale"
        ])

    strong = business_rules[business_rules["lift"] >= min_lift].copy()
    strong = strong[(strong["antecedent_len"] <= 2) & (strong["consequent_len"] <= 2)]
    strong = strong.sort_values(["lift", "confidence"], ascending=False).head(max_bundles)

    rows = []
    seen_item_sets = []
    for _, row in strong.iterrows():
        items = sorted(set(row["antecedents"]) | set(row["consequents"]))
        item_key = frozenset(items)
        if item_key in seen_item_sets:
            continue
        seen_item_sets.append(item_key)

        full_price = sum(item_prices.get(i, 0.0) for i in items)
        bundle_price = round(full_price * (1 - discount_pct), 2)
        bundle_name = " + ".join(items) + " Bundle"

        rows.append({
            "bundle_name": bundle_name,
            "items": ", ".join(items),
            "n_items": len(items),
            "full_price": round(full_price, 2),
            "bundle_price": bundle_price,
            "savings": round(full_price - bundle_price, 2),
            "discount_pct": f"{discount_pct*100:.0f}%",
            "support": round(row["support"], 4),
            "confidence": round(row["confidence"], 3),
            "lift": round(row["lift"], 2),
            "rationale": (
                f"Bought together {row['confidence']*100:.0f}% of the time when "
                f"{row['antecedents_str']} is purchased, at {row['lift']:.1f}x the baseline rate."
            ),
        })

    return pd.DataFrame(rows)
