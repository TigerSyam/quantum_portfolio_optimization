import numpy as np


def load_data():
	"""Returns all required portfolio data."""

	# Expected returns
	mu = np.array([10, 8, 12, 7, 9])

	# Volatility (uncertainty)
	sigma = np.array([5, 4, 6, 3, 5])

	# Covariance matrix
	Sigma = np.array(
		[
			[5, 2, 3, 1, 2],
			[2, 4, 2, 1, 1],
			[3, 2, 6, 2, 3],
			[1, 1, 2, 3, 1],
			[2, 1, 3, 1, 5],
		]
	)

	# Transaction costs
	cost = np.array([1, 1, 2, 1, 1])

	# Previous portfolio
	x_old = np.array([1, 0, 1, 0, 0])

	# Tail risk (worst-case returns)
	tail_returns = np.array([8, 6, 12, 5, 7])

	return mu, sigma, Sigma, cost, x_old, tail_returns
