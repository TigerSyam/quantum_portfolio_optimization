import os
import sys

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import K
from classical.bruteforce import run_bruteforce
from quantum.qaoa import run_qaoa
from quantum.qubo import build_qubo
from utils.data_loader import load_data
from utils.objective import objective


def qubo_energy_upper_tri(Q: np.ndarray, x: np.ndarray) -> float:
    """Energy convention: E(x) = sum_{i<=j} Q[i,j] x_i x_j."""

    x = np.asarray(x).astype(float)
    return float(x @ np.triu(Q) @ x)


def main() -> None:
    mu, sigma, Sigma, cost, x_old, tail = load_data()
    Q = build_qubo(mu, sigma, Sigma, cost, x_old, tail)

    best_x, best_val, _ = run_bruteforce()
    best_x = np.asarray(best_x)

    qaoa_result = run_qaoa(Q)
    qaoa_x = np.asarray(qaoa_result.x)

    classical_obj = float(best_val)
    classical_qubo = qubo_energy_upper_tri(Q, best_x)

    qaoa_obj = float(objective(qaoa_x, mu, sigma, Sigma, cost, x_old, tail))
    qaoa_qubo = qubo_energy_upper_tri(Q, qaoa_x)

    print("\n==============================")
    print("COMPARISON SUMMARY")
    print("==============================")
    print(f"Classical best x: {best_x.astype(int)} | sum={int(best_x.sum())} | feasible(K={K})={int(best_x.sum())==K}")
    print(f"  Objective (original): {classical_obj:.4f}")
    print(f"  QUBO energy:          {classical_qubo:.4f}")

    print(f"QAOA x:           {qaoa_x.astype(int)} | sum={int(qaoa_x.sum())} | feasible(K={K})={int(qaoa_x.sum())==K}")
    print(f"  Objective (original): {qaoa_obj:.4f}")
    print(f"  QUBO energy:          {qaoa_qubo:.4f}")


if __name__ == "__main__":
    main()
