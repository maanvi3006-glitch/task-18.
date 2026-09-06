"""
mba_pipeline.py
----------------
Core market-basket-analysis pipeline. Implements the full step-by-step
execution required by the task brief:

  1. Shape data into transactions (baskets of items).
  2. Run frequent-itemset mining (Apriori AND FP-Growth - both implemented
     so we can compare and justify a choice, per "alternative approaches").
  3. Generate association rules with support/confidence/lift.
  4. Filter to high-lift, high-support, actionable, non-redundant rules.
  5. Interpret top rules in business terms (business_interpretation.py).
  6. Recommend bundles/cross-sells (bundles.py).

Also implements the simplest alternative approach named in the brief:
an item-item co-occurrence matrix, for comparison.
"""

import time
import warnings
import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

warnings.filterwarnings("ignore", category=DeprecationWarning)


def transactions_to_basket_list(df: pd.DataFrame) -> list[list[str]]:
    """Step 1: shape long-format (transaction_id, item) rows into a list of
    baskets (list of item lists), one basket per transaction."""
    grouped = df.groupby("transaction_id")["item"].apply(lambda s: sorted(set(s)))
    return grouped.tolist()


def encode_transactions(baskets: list[list[str]]) -> pd.DataFrame:
    """One-hot encode baskets into the boolean matrix mlxtend expects."""
    te = TransactionEncoder()
    te_array = te.fit(baskets).transform(baskets)
    return pd.DataFrame(te_array, columns=te.columns_)


def mine_frequent_itemsets(onehot_df: pd.DataFrame, algorithm: str = "apriori",
                            min_support: float = 0.02):
    """Step 2: frequent itemset mining. Supports both Apriori and FP-Growth
    so the two can be compared directly (same input, same min_support)."""
    algorithm = algorithm.lower()
    start = time.perf_counter()
    if algorithm == "apriori":
        itemsets = apriori(onehot_df, min_support=min_support, use_colnames=True)
    elif algorithm == "fpgrowth":
        itemsets = fpgrowth(onehot_df, min_support=min_support, use_colnames=True)
    else:
        raise ValueError(f"Unknown algorithm '{algorithm}'. Use 'apriori' or 'fpgrowth'.")
    elapsed = time.perf_counter() - start
    itemsets = itemsets.sort_values("support", ascending=False).reset_index(drop=True)
    itemsets["itemset_size"] = itemsets["itemsets"].apply(len)
    return itemsets, elapsed


def compare_algorithms(onehot_df: pd.DataFrame, min_support: float = 0.02) -> pd.DataFrame:
    """Runs both algorithms and returns a timing/result comparison table -
    direct evidence for the 'alternative approaches, justify your choice'
    learning objective."""
    rows = []
    for algo in ("apriori", "fpgrowth"):
        itemsets, elapsed = mine_frequent_itemsets(onehot_df, algorithm=algo, min_support=min_support)
        rows.append({
            "algorithm": algo,
            "runtime_seconds": round(elapsed, 4),
            "n_frequent_itemsets": len(itemsets),
            "max_itemset_size": int(itemsets["itemset_size"].max()) if len(itemsets) else 0,
        })
    return pd.DataFrame(rows)


def generate_rules(itemsets: pd.DataFrame, min_confidence: float = 0.3,
                    min_lift: float = 1.0, n_transactions: int | None = None) -> pd.DataFrame:
    """Step 3: association rules with support/confidence/lift (+ extra
    metrics mlxtend provides: leverage, conviction, zhangs_metric)."""
    if itemsets.empty:
        return pd.DataFrame(columns=[
            "antecedents", "consequents", "support", "confidence", "lift"
        ])
    kwargs = dict(metric="confidence", min_threshold=min_confidence)
    if n_transactions is not None:
        try:
            kwargs["num_itemsets"] = n_transactions
        except TypeError:
            pass
    rules = association_rules(itemsets, **kwargs)
    rules = rules[rules["lift"] >= min_lift].copy()
    rules["antecedents_str"] = rules["antecedents"].apply(lambda s: ", ".join(sorted(s)))
    rules["consequents_str"] = rules["consequents"].apply(lambda s: ", ".join(sorted(s)))
    rules["antecedent_len"] = rules["antecedents"].apply(len)
    rules["consequent_len"] = rules["consequents"].apply(len)
    rules = rules.sort_values(["lift", "confidence"], ascending=False).reset_index(drop=True)
    return rules


def prune_redundant_rules(rules: pd.DataFrame) -> pd.DataFrame:
    """Step 4 (part 1): remove redundant rules - if a smaller antecedent
    already implies the same consequent with >= lift, the larger (superset)
    version adds no new information and is noise ('rule overload' pitfall).
    """
    if rules.empty:
        return rules
    keep = []
    rules_sorted = rules.sort_values("antecedent_len")
    seen = []  # list of (antecedent_frozenset, consequent_frozenset, lift)
    for _, row in rules_sorted.iterrows():
        ants, cons, lift = row["antecedents"], row["consequents"], row["lift"]
        redundant = any(
            ants.issuperset(s_ant) and cons == s_cons and lift <= s_lift * 1.02
            for s_ant, s_cons, s_lift in seen
        )
        if not redundant:
            seen.append((ants, cons, lift))
            keep.append(row.name)
    return rules.loc[keep].sort_values(["lift", "confidence"], ascending=False).reset_index(drop=True)


def filter_actionable_rules(rules: pd.DataFrame, min_support: float = 0.01,
                             min_lift: float = 1.15, min_confidence: float = 0.25,
                             max_antecedent_len: int = 3, top_n: int | None = 50) -> pd.DataFrame:
    """Step 4 (part 2): filter down to high-lift, high-support, ACTIONABLE
    rules, and rank by a composite 'actionability score'. This directly
    guards against the pitfalls listed in the brief:
      - 'Chasing high-confidence/low-lift trivia'    -> min_lift floor
      - 'Rule overload with no prioritisation'        -> top_n + ranked score
    """
    if rules.empty:
        return rules
    f = rules[
        (rules["support"] >= min_support)
        & (rules["lift"] >= min_lift)
        & (rules["confidence"] >= min_confidence)
        & (rules["antecedent_len"] <= max_antecedent_len)
    ].copy()

    f = prune_redundant_rules(f)

    # Composite actionability score: rewards strong lift AND enough support
    # to matter at business scale (a lift-10 rule seen twice a year is not
    # actionable; balance the two).
    if not f.empty:
        f["actionability_score"] = (
            f["lift"].clip(upper=10) * 0.5
            + (f["support"] / f["support"].max()) * 3.0
            + f["confidence"] * 2.0
        )
        f = f.sort_values("actionability_score", ascending=False).reset_index(drop=True)
        if top_n:
            f = f.head(top_n)
    return f


def cooccurrence_matrix(baskets: list[list[str]]) -> pd.DataFrame:
    """The 'simpler alternative' named in the brief: a raw item-item
    co-occurrence count matrix. Useful for quick eyeballing and as a sanity
    check against the apriori/fp-growth rules, but note (for the writeup)
    that it does NOT normalise for item popularity the way lift does - two
    items that are just individually very popular will co-occur a lot
    without being a meaningful *rule*. This is exactly why lift matters.
    """
    all_items = sorted({item for basket in baskets for item in basket})
    idx = {item: i for i, item in enumerate(all_items)}
    mat = np.zeros((len(all_items), len(all_items)), dtype=int)
    for basket in baskets:
        for i, a in enumerate(basket):
            for b in basket[i + 1:]:
                ia, ib = idx[a], idx[b]
                mat[ia, ib] += 1
                mat[ib, ia] += 1
    return pd.DataFrame(mat, index=all_items, columns=all_items)


def top_cooccurring_pairs(cooc: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    pairs = []
    items = cooc.index.tolist()
    for i, a in enumerate(items):
        for b in items[i + 1:]:
            count = cooc.loc[a, b]
            if count > 0:
                pairs.append((a, b, int(count)))
    out = pd.DataFrame(pairs, columns=["item_a", "item_b", "co_occurrences"])
    return out.sort_values("co_occurrences", ascending=False).head(top_n).reset_index(drop=True)
