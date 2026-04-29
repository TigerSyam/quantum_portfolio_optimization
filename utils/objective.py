import numpy as np
from config import ALPHA, BETA, GAMMA, DELTA, ETA, TAU, LAMBDA, K, KAPPA


def compute_adjusted_return(mu, sigma):
	"""
	Uncertainty-adjusted return: mu - kappa * sigma
	"""
	return mu - KAPPA * sigma


def compute_variance(x, Sigma):
	return x.T @ Sigma @ x


def compute_diversification(x, Sigma):
	"""
	Penalize correlated asset selection (off-diagonal terms)
	"""
	div = 0
	n = len(x)
	for i in range(n):
		for j in range(i + 1, n):
			div += Sigma[i][j] * x[i] * x[j]
	return div


def compute_transaction_cost(x, cost):
	return np.dot(cost, x)


def compute_stability(x, x_old):
	"""
	Penalize deviation from previous portfolio
	"""
	return np.sum((x - x_old) ** 2)


def compute_tail_risk(x, tail_returns):
	"""
	CVaR approximation: weighted worst-case losses
	"""
	return np.dot(tail_returns, x)


def compute_cardinality_penalty(x):
	return (np.sum(x) - K) ** 2


def objective(x, mu, sigma, Sigma, cost, x_old, tail_returns):
	"""
	Full composite objective function
	"""
	x = np.array(x)

	# Adjusted return
	mu_tilde = compute_adjusted_return(mu, sigma)

	# Individual components
	ret = -ALPHA * np.dot(mu_tilde, x)
	var = BETA * compute_variance(x, Sigma)
	div = GAMMA * compute_diversification(x, Sigma)
	cst = DELTA * compute_transaction_cost(x, cost)
	stab = ETA * compute_stability(x, x_old)
	tail = TAU * compute_tail_risk(x, tail_returns)
	card = LAMBDA * compute_cardinality_penalty(x)

	total = ret + var + div + cst + stab + tail + card

	return total
