from sklearn.metrics import jaccard_score
from itertools import combinations
import numpy as np
import json

labels = ["immortal-accounts-vote", "dead-end-vote", "no-way-back", "price-comparison-prevention-vote", "intermediate-currency-vote", "discount-framing-manipulation", "privacy-maze-vote", "extra-burden", "disguised-ad-vote", "sneak-into-basket-vote", "drip-pricing-vote", "reference-pricing-vote", "conflicting-information-vote", "information-without-context-vote", "false-hierarchy-vote", "visual-prominence-vote", "bundling-vote", "pressured-selling-vote", "bad-defaults-sum", "cuteness-vote", "positive-vote", "trick-questions-sum", "choice-overload-sum", "hidden-information-sum", "wrong-language-vote", "complex-language-vote", "feedward-ambiguity-sum", "nagging-sum", "forced-continuity-sum", "forced-registration-sum", "privacy-zukering-vote", "friend-spam-vote", "address-book-leeching-vote", "social-pyramid-vote", "pay-to-play-vote", "grinding-vote", "auto-play-vote", "high-demand-vote", "low-stock-vote", "endorsement-vote", "parasocial-vote", "activity-messages-vote", "countdown-timer-vote", "limited-time-vote", "confirmshaming-vote"]
idx  = {lab: i for i, lab in enumerate(labels)}
L = len(labels) # Vector length

def to_vec(label_dict):
    """Convert one coder dict (possibly empty) to 0/1 vector length L."""
    v = np.zeros(L, dtype=int)
    for lab in label_dict:               # {} means no labels → loop skipped
        if lab not in idx:
            raise KeyError(f"Unknown label {lab!r}")
        v[idx[lab]] = 1
    return v

def jaccard_dist(v1, v2):
    if v1.sum() == 0 and v2.sum() == 0:       # both empty → perfect match
        return 0.0
    return 1 - jaccard_score(v1, v2, zero_division=0)

# -----------------------------------------------------------------
# 1. load ONE dataset
with open("qualified.json") as fh:
    units = json.load(fh)           
# -----------------------------------------------------------------
# 2. observed disagreement Do
sq_sum, pair_ct = 0.0, 0
for coder_list in units.values():
    vecs = [to_vec(d) for d in coder_list]
    for i, j in combinations(range(len(vecs)), 2):   # unordered
        d = jaccard_dist(vecs[i], vecs[j])
        sq_sum += 2 * d * d                         # (i,j) and (j,i)
        pair_ct += 2
Do = sq_sum / pair_ct

# -----------------------------------------------------------------
# 3. expected disagreement De
all_vecs = [to_vec(d) for coder_list in units.values() for d in coder_list]
n = len(all_vecs)
exp_sum = 0.0
for i, v1 in enumerate(all_vecs):
    for j, v2 in enumerate(all_vecs):
        if i != j:
            d = jaccard_dist(v1, v2)
            exp_sum += d * d
De = exp_sum / (n * (n - 1))

# -----------------------------------------------------------------
alpha = 1 - Do / De
print(f"Krippendorff’s α (Jaccard) = {alpha:.3f}")