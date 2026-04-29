import numpy as np

import warnings

try:  # pragma: no cover
	from scipy.sparse import SparseEfficiencyWarning

	warnings.filterwarnings("ignore", category=SparseEfficiencyWarning)
except Exception:  # pragma: no cover
	pass

try:
	# Qiskit >= 1.0 style
	from qiskit_algorithms.minimum_eigensolvers import QAOA
	from qiskit_algorithms.optimizers import COBYLA
except Exception:  # pragma: no cover
	# Older Qiskit style (imported dynamically to avoid static-analysis failures)
	import importlib

	QAOA = importlib.import_module("qiskit.algorithms").QAOA
	COBYLA = importlib.import_module("qiskit.algorithms.optimizers").COBYLA

try:
	from qiskit.primitives import Sampler

	def _make_sampler():
		return Sampler()

except Exception:  # pragma: no cover
	# Some Qiskit versions expose StatevectorSampler instead.
	from qiskit.primitives import StatevectorSampler

	def _make_sampler():
		return StatevectorSampler()

from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer


def qubo_to_quadratic_program(Q: np.ndarray) -> QuadraticProgram:
	"""Convert a QUBO matrix Q into a Qiskit QuadraticProgram.

	Convention: Q is upper-triangular and energy is
	E(x) = sum_{i<=j} Q[i, j] * x_i * x_j.

	Since QuadraticProgram's quadratic objective stores each pair once
	(i < j), we map off-diagonal terms directly as Q[i, j].
	"""

	n = Q.shape[0]
	qp = QuadraticProgram()

	for i in range(n):
		qp.binary_var(name=f"x{i}")

	linear = {f"x{i}": float(Q[i, i]) for i in range(n)}
	quadratic = {}

	for i in range(n):
		for j in range(i + 1, n):
			coeff = float(Q[i, j])
			if coeff != 0.0:
				quadratic[(f"x{i}", f"x{j}")] = coeff

	qp.minimize(linear=linear, quadratic=quadratic)
	return qp


def run_qaoa(Q: np.ndarray):
	"""Run QAOA on a given QUBO matrix."""

	qp = qubo_to_quadratic_program(Q)

	optimizer = COBYLA(maxiter=100)
	sampler = _make_sampler()
	qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=2)

	qaoa_solver = MinimumEigenOptimizer(qaoa)
	result = qaoa_solver.solve(qp)

	print("\nQAOA Result")
	print("====================")
	print("Solution:", result.x)
	print("Objective value:", result.fval)

	return result
