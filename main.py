from utils.data_loader import load_data
from quantum.qubo import build_qubo
from quantum.qaoa import run_qaoa


if __name__ == "__main__":
    mu, sigma, Sigma, cost, x_old, tail = load_data()

    Q = build_qubo(mu, sigma, Sigma, cost, x_old, tail)

    result = run_qaoa(Q)
