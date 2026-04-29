"""Central configuration for the portfolio optimization project."""

import numpy as np

# -----------------------------
# Problem Size
# -----------------------------
N_ASSETS = 5
K = 2  # number of assets to select

# -----------------------------
# Hyperparameters (tunable)
# -----------------------------
ALPHA = 1.0  # return weight
BETA = 0.5  # variance weight
GAMMA = 0.3  # diversification weight
DELTA = 0.2  # transaction cost weight
ETA = 0.5  # stability weight
TAU = 0.4  # tail risk weight
LAMBDA = 2.0  # cardinality penalty

# -----------------------------
# Uncertainty parameter
# -----------------------------
KAPPA = 1.0  # confidence level for return adjustment
