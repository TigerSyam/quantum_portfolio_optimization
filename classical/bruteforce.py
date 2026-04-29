from itertools import product

import numpy as np

from utils.data_loader import load_data
from utils.objective import objective


def run_bruteforce():
	# Load data
	mu, sigma, Sigma, cost, x_old, tail = load_data()

	n = len(mu)

	best_x = None
	best_val = float("inf")

	all_results = []

	print("\nEvaluating all portfolios...\n")

	# Generate all combinations
	for x in product([0, 1], repeat=n):
		x = np.array(x)

		val = objective(x, mu, sigma, Sigma, cost, x_old, tail)

		all_results.append((x, val))

		print(f"Portfolio: {x} -> Objective: {val:.2f}")

		if val < best_val:
			best_val = val
			best_x = x

	print("\n==============================")
	print("BEST PORTFOLIO FOUND")
	print("==============================")
	print("Portfolio:", best_x)
	print("Objective value:", round(best_val, 4))

	return best_x, best_val, all_results
