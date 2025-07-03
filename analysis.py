import numpy as np
import krippendorff

# --- 1) Define your two raters' annotations ---------------------------

labeler1 = [
    [0],
    [15, 16, 40],
    [38, 39, 14],
    [0],
    [16],
    [44, 40],
    [8],
    [3],
    [0],
    [21],
    [44],
    [16, 40],
    [0],
    [44, 38, 27, 21],
    [0],
    [3],
    [45],
    [45],
    [45],
    [16, 3],
    [30],
    [30],
    [0],
    [0],
    [0],
    [44],
    [15, 16],
    [0],
    [44, 43],
    [0],
    [43, 44],
    [30],
    [30, 14],
    [44, 43],
    [0],
    [0],
    [30, 45]
]

labeler2 = [
    [0],
    [16, 21],
    [38, 39],
    [0],
    [16],
    [16, 44],
    [0],
    [3],
    [0],
    [21, 14],
    [44],
    [16, 40, 28],
    [21],
    [44, 38, 27, 21],
    [0],
    [3],
    [28],
    [45, 21, 16],
    [16],
    [16],
    [30],
    [30, 24],
    [0],
    [21],
    [0],
    [44],
    [21, 16],
    [0],
    [43, 28],
    [0],
    [16, 43, 28],
    [30],
    [30],
    [16, 43],
    [0],
    [0],
    [30, 24]
]

n_widgets = 37
n_cats    = 46

# --- 2) Build binary matrices M1, M2 of shape (37, 46) -----------------
M1 = np.zeros((n_widgets, n_cats), dtype=int)
M2 = np.zeros((n_widgets, n_cats), dtype=int)

for i, cats in enumerate(labeler1):
    M1[i, cats] = 1
for i, cats in enumerate(labeler2):
    M2[i, cats] = 1

# --- 3) Flatten to two vectors of length n_widgets * n_cats ----------
v1 = M1.flatten()
v2 = M2.flatten()

# --- 4) Stack into reliability_data (shape: n_coders × n_units) -------
# krippendorff.alpha expects shape (coders, units)
reliability_data = np.vstack([v1, v2])

# --- 5) Compute Krippendorff's alpha for nominal data -----------------
alpha = krippendorff.alpha(
    reliability_data=reliability_data,
    level_of_measurement='nominal'
)

print(f"Krippendorff's α (nominal) = {alpha:.3f}")
