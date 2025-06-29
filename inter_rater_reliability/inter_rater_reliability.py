from sklearn.metrics import jaccard_score
from itertools import combinations
import numpy as np
import json

labels = ["immortal-accounts-vote", "dead-end-vote", "no-way-back", "price-comparison-prevention-vote", "intermediate-currency-vote", "discount-framing-manipulation", "privacy-maze-vote", "extra-burden", "disguised-ad-vote", "sneak-into-basket-vote", "drip-pricing-vote", "reference-pricing-vote", "conflicting-information-vote", "information-without-context-vote", "false-hierarchy-vote", "visual-prominence-vote", "bundling-vote", "pressured-selling-vote", "bad-defaults-sum", "cuteness-vote", "positive-vote", "trick-questions-sum", "choice-overload-sum", "hidden-information-sum", "wrong-language-vote", "complex-language-vote", "feedward-ambiguity-sum", "nagging-sum", "forced-continuity-sum", "forced-registration-sum", "privacy-zukering-vote", "friend-spam-vote", "address-book-leeching-vote", "social-pyramid-vote", "pay-to-play-vote", "grinding-vote", "auto-play-vote", "high-demand-vote", "low-stock-vote", "endorsement-vote", "parasocial-vote", "activity-messages-vote", "countdown-timer-vote", "limited-time-vote", "confirmshaming-vote"]
idx  = {lab: i for i, lab in enumerate(labels)}
L = len(labels) # Vector length

# 1. load ONE dataset
with open("qualified.json") as fh:
    units = json.load(fh)     

# def to_vec(label_dict):
#     """Convert one coder dict (possibly empty) to 0/1 vector length L."""
#     v = np.zeros(L, dtype=int)
#     for lab in label_dict:               # {} means no labels → loop skipped
#         if lab not in idx:
#             raise KeyError(f"Unknown label {lab!r}")
#         v[idx[lab]] = 1
#     return v

# def jaccard_dist(v1, v2):
#     if v1.sum() == 0 and v2.sum() == 0:       # both empty → perfect match
#         return 0.0
#     return 1 - jaccard_score(v1, v2, zero_division=0)
      
# # -----------------------------------------------------------------
# # 2. observed disagreement Do
# sq_sum, pair_ct = 0.0, 0
# for coder_list in units.values():
#     vecs = [to_vec(d) for d in coder_list]
#     for i, j in combinations(range(len(vecs)), 2):   # unordered
#         d = jaccard_dist(vecs[i], vecs[j])
#         sq_sum += 2 * d * d                         # (i,j) and (j,i)
#         pair_ct += 2
# Do = sq_sum / pair_ct

# # -----------------------------------------------------------------
# # 3. expected disagreement De
# all_vecs = [to_vec(d) for coder_list in units.values() for d in coder_list]
# n = len(all_vecs)
# exp_sum = 0.0
# for i, v1 in enumerate(all_vecs):
#     for j, v2 in enumerate(all_vecs):
#         if i != j:
#             d = jaccard_dist(v1, v2)
#             exp_sum += d * d
# De = exp_sum / (n * (n - 1))

# # -----------------------------------------------------------------
# alpha = 1 - Do / De
# print(f"Krippendorff’s α (Jaccard) = {alpha:.3f}")

# 1. helpers -----------------------------------------------------------
def to_vec(label_dict):
    """Convert coder dict (maybe empty) -> fixed-length 0/1 vector."""
    v = np.zeros(L, dtype=int)
    for lab in label_dict:
        if lab not in idx:
            raise KeyError(f"Unknown label: {lab}")
        v[idx[lab]] = 1
    return v

def jaccard_dist(v1, v2):
    """Squared Jaccard distance for two 0/1 vectors."""
    if v1.sum() == 0 and v2.sum() == 0:
        return 0.0                         # perfect agreement on ∅
    d = 1 - jaccard_score(v1, v2, zero_division=0)
    return d * d                           # Krippendorff uses δ²

def masi_dist(s1, s2):
    """Squared MASI distance for two Python sets of labels."""
    if not s1 and not s2:
        return 0.0
    inter = len(s1 & s2)
    union = len(s1 | s2)
    j     = inter / union                 # Jaccard similarity
    # monotone weight
    if   s1 == s2:                  M = 1.0
    elif s1.issubset(s2) or s2.issubset(s1):
        M = 2/3
    elif inter:                     M = 1/3
    else:                           M = 0.0
    return (1 - j * M) ** 2         # square for α

# ---------------------------------------------------------------------
def alpha(distance_fn, encoder):
    """Generic Krippendorff α using a custom distance and encoder."""
    # observed
    sq_sum = pair_ct = 0
    for coder_list in units.values():
        items = [encoder(d) for d in coder_list]
        for i, j in combinations(range(len(items)), 2):
            d2 = distance_fn(items[i], items[j])
            sq_sum += 2 * d2            # ordered pairs
            pair_ct += 2
    Do = sq_sum / pair_ct

    # expected
    all_items = [encoder(d) for cl in units.values() for d in cl]
    n = len(all_items)
    exp = sum(
        distance_fn(all_items[i], all_items[j])
        for i in range(n) for j in range(n) if i != j
    )
    De = exp / (n * (n - 1))
    return 1 - Do / De

# ---------------------------------------------------------------------
# 2. load data ---------------------------------------------------------
with open("qualified.json", encoding="utf-8") as fh:
    units = json.load(fh)          # dict: unit_id -> list of coder dicts

# ---------------------------------------------------------------------
alpha_jac  = alpha(jaccard_dist, lambda d: to_vec(d))
alpha_masi = alpha(masi_dist,    lambda d: set(d.keys()))

print(f"Krippendorff α  (Jaccard) = {alpha_jac:.3f}")
print(f"Krippendorff α  (MASI)    = {alpha_masi:.3f}")