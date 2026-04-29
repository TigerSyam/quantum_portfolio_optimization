# Quantum Portfolio Optimization (Hybrid Quantum–Classical, QUBO + QAOA)

A research-style mini-project that formulates a **multi-objective portfolio optimization** problem, maps it into a **QUBO** (Quadratic Unconstrained Binary Optimization) matrix, and solves it using:

- **Classical exact baseline:** brute-force enumeration (ground truth for small N)
- **Quantum approach:** **QAOA** (Quantum Approximate Optimization Algorithm) via **Qiskit**

The goal is to build a **complete, reproducible pipeline** and evaluate when/why quantum advantage does or does not appear.

## Pipeline

1. Problem formulation (multi-objective composite objective)
2. Classical baseline (brute force)
3. QUBO construction
4. QAOA solve (hybrid loop)
5. Comparison + analysis + report artifacts

## Project Structure

```
quantum_portfolio_optimization/
├── classical/
│   └── bruteforce.py
├── quantum/
│   ├── qubo.py
│   └── qaoa.py
├── utils/
│   ├── data_loader.py
│   └── objective.py
├── results/
│   └── compare.py
├── report/
│   ├── final_report.md
│   ├── notes.md
│   ├── panel_qa.md
│   └── ppt_slides.md
├── config.py
└── main.py
```

## Mathematical Model (high level)

Binary decision vector:

- $x \in \{0,1\}^N$, where $x_i=1$ means asset *i* is selected

Composite objective (implemented in `utils/objective.py`) includes:

- uncertainty-adjusted return (\(\mu - \kappa\sigma\))
- variance risk (\(x^\top\Sigma x\))
- diversification penalty (correlation penalty)
- transaction cost
- stability/turnover vs previous portfolio
- tail-risk proxy
- cardinality constraint (\(\sum_i x_i = K\)) encoded via penalty

All weights and hyperparameters live in `config.py`.

## Setup

### 1) Create & activate a virtual environment (recommended)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

## Quickstart

### Run QAOA (current `main.py`)

```bash
python main.py
```

Expected output looks like:

```
QAOA Result
====================
Solution: [...]
Objective value: ...
```

### Run the classical + quantum comparison (recommended)

This prints:
- brute-force evaluation summary
- QAOA result
- side-by-side comparison (solution, feasibility, objective)

```bash
python results/compare.py
```

## Reproducibility Notes

### QUBO coefficient convention

This repo uses an **upper-triangular** QUBO convention:

- Energy: \(E(x) = \sum_{i\le j} Q_{ij} x_i x_j\)
- Linear terms are on the diagonal (since \(x_i^2=x_i\) for binary variables)
- Quadratic terms are stored once for \(i<j\)

This matches the mapping used in `quantum/qaoa.py` when building a Qiskit `QuadraticProgram`.

## Results (current instance)

Dataset: synthetic 5-asset toy instance in `utils/data_loader.py`.

From `python results/compare.py`:

| Method | Solution (x) | #Assets | Objective (original) | Feasible (K=2?) |
|---|---:|---:|---:|---|
| Classical (Brute Force) | [1,0,0,1,0] | 2 | 2.9000 | ✔ |
| QAOA | [1,0,0,1,0] | 2 | 2.9000 | ✔ |

## Report & Presentation Assets

Submission-ready text lives in:

- `report/final_report.md` — full report draft
- `report/ppt_slides.md` — slide-by-slide deck script (12 slides)
- `report/panel_qa.md` — panel Q&A prep

