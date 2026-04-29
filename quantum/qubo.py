import numpy as np
from config import ALPHA, BETA, GAMMA, DELTA, ETA, TAU, LAMBDA, K, KAPPA


def build_qubo(mu, sigma, Sigma, cost, x_old, tail_returns):
	"""Build an *upper-triangular* QUBO matrix Q.

	Convention used throughout this project:
	- Energy is computed as E(x) = sum_{i<=j} Q[i, j] * x_i * x_j.
	- Linear terms live on the diagonal (since x_i^2 = x_i for binary x).
	- Quadratic terms are stored only in the upper triangle (i < j).

	This convention matches how we map Q into Qiskit's QuadraticProgram.
	"""

	n = len(mu)
	Q = np.zeros((n, n))

	# -----------------------------
	# (1) Adjusted return (linear → diagonal)
	# -----------------------------
	mu_tilde = mu - KAPPA * sigma
	for i in range(n):
		Q[i, i] += -ALPHA * mu_tilde[i]

	# -----------------------------
	# (2) Variance (quadratic)
	# -----------------------------
	# BETA * x^T Sigma x = BETA * (sum_i Sigma_ii x_i + 2*sum_{i<j} Sigma_ij x_i x_j)
	for i in range(n):
		Q[i, i] += BETA * Sigma[i][i]
	for i in range(n):
		for j in range(i + 1, n):
			Q[i, j] += 2 * BETA * Sigma[i][j]

	# -----------------------------
	# (3) Diversification (off-diagonal only)
	# -----------------------------
	for i in range(n):
		for j in range(i + 1, n):
			Q[i, j] += GAMMA * Sigma[i][j]

	# -----------------------------
	# (4) Transaction cost (linear)
	# -----------------------------
	for i in range(n):
		Q[i, i] += DELTA * cost[i]

	# -----------------------------
	# (5) Stability (turnover)
	# (x_i - x_old)^2 = x_i - 2*x_i*x_old + x_old^2
	# x_old^2 is constant → ignore
	# -----------------------------
	for i in range(n):
		Q[i, i] += ETA * (1 - 2 * x_old[i])

	# -----------------------------
	# (6) Tail risk (linear)
	# -----------------------------
	for i in range(n):
		Q[i, i] += TAU * tail_returns[i]

	# -----------------------------
	# (7) Cardinality constraint
	# (sum x_i - K)^2
	# = sum x_i^2 + 2 sum_{i<j} x_i x_j - 2K sum x_i + K^2
	# ignore constant K^2
	# -----------------------------
	for i in range(n):
		Q[i, i] += LAMBDA * (1 - 2 * K)

	for i in range(n):
		for j in range(i + 1, n):
			Q[i, j] += 2 * LAMBDA

	return Q
