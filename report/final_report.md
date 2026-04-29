# Hybrid Quantum–Classical Multi-Objective Portfolio Optimization (QUBO + QAOA)

## 1. Introduction
Portfolio optimization is a foundational problem in quantitative finance: selecting a subset of assets that balances expected return against multiple notions of risk and operational constraints. While classical mean–variance formulations (e.g., Markowitz) are widely used, they often under-represent real-world concerns such as parameter uncertainty, tail risk, transaction costs, and turnover.

This project builds a hybrid quantum–classical pipeline for **multi-objective portfolio optimization** by (i) formulating a composite objective capturing realistic financial terms and (ii) mapping it into a **Quadratic Unconstrained Binary Optimization (QUBO)** form so it can be solved by quantum optimization methods such as **QAOA**. We benchmark quantum results against an exact classical baseline.

## 2. Problem Formulation
### Decision variables
Let $x \in \{0,1\}^N$ be a binary selection vector where $x_i=1$ indicates asset $i$ is selected.

### Inputs
- Expected returns: $\mu \in \mathbb{R}^N$
- Uncertainty (volatility proxy): $\sigma \in \mathbb{R}^N$
- Covariance matrix: $\Sigma \in \mathbb{R}^{N\times N}$
- Transaction costs: $c \in \mathbb{R}^N$
- Previous portfolio: $x^{\text{old}} \in \{0,1\}^N$
- Tail-risk proxy (worst-case returns): $r^{\text{tail}} \in \mathbb{R}^N$

### Constraint
Cardinality constraint (select exactly $K$ assets):
$$\sum_{i=1}^N x_i = K$$

## 3. Mathematical Model
We use an uncertainty-adjusted return:
$$\tilde\mu = \mu - \kappa\,\sigma$$

The composite objective minimized is:
$$
\min_{x\in\{0,1\}^N}\;\underbrace{-\alpha\,\tilde\mu^\top x}_{\text{return}} +
\underbrace{\beta\,x^\top\Sigma x}_{\text{variance}} +
\underbrace{\gamma\,\sum_{i<j}\Sigma_{ij}x_ix_j}_{\text{diversification}} +
\underbrace{\delta\,c^\top x}_{\text{transaction cost}} +
\underbrace{\eta\,\|x-x^{\text{old}}\|_2^2}_{\text{stability}} +
\underbrace{\tau\,(r^{\text{tail}})^\top x}_{\text{tail risk}} +
\underbrace{\lambda\,(\sum_i x_i - K)^2}_{\text{cardinality penalty}}
$$

Where $(\alpha,\beta,\gamma,\delta,\eta,\tau,\lambda,\kappa)$ are tunable weights.

## 4. QUBO Formulation
To solve the binary optimization using quantum algorithms, the objective is mapped to QUBO form.

We construct a matrix $Q$ such that the QUBO energy is
$$E(x) = \sum_{i\le j} Q_{ij} x_i x_j$$

Key mapping ideas:
- Linear terms become diagonal entries (since $x_i^2=x_i$ for binary variables).
- Quadratic interactions contribute to off-diagonal entries.
- The cardinality constraint is encoded as a penalty term $(\sum_i x_i - K)^2$, producing both diagonal and off-diagonal contributions.

This yields a single matrix $Q$ that aggregates all terms, enabling quantum-ready optimization.

## 5. Classical Approach
### Method
A brute-force baseline enumerates all $2^N$ portfolios and evaluates the composite objective for each configuration. For $N=5$, this is 32 portfolios and is computationally trivial.

### Result (N=5)
- Best portfolio: $x=[1,0,0,1,0]$ (select assets 1 and 4 in 0-indexed vector form)
- Objective value (composite objective): **2.9000**
- Feasible ($\sum x_i = K=2$): **Yes**

## 6. Quantum Approach
### Method
We solve the QUBO using **QAOA** (Quantum Approximate Optimization Algorithm) as implemented in Qiskit:
1. Convert the QUBO matrix to a `QuadraticProgram`.
2. Use QAOA (parameterized quantum circuit) and a classical optimizer (COBYLA) to minimize the QUBO energy.
3. Extract the best measured solution bitstring.

### Result (simulation-based)
- QAOA solution: $x=[1,0,0,1,0]$
- Objective value (composite objective): **2.9000**
- Feasible ($\sum x_i = K=2$): **Yes**

Note: QAOA minimizes QUBO energy; we report the *original composite objective* for a direct apples-to-apples comparison against the classical baseline.

## 7. Comparative Analysis
A compact summary:

| Method | Solution (x) | #Assets | Objective (original) | Feasible (K=2?) |
|---|---:|---:|---:|---|
| Classical (Brute Force) | [1,0,0,1,0] | 2 | 2.9000 | ✔ |
| QAOA | [1,0,0,1,0] | 2 | 2.9000 | ✔ |

Interpretation:
- The classical method provides an exact global optimum for small $N$.
- QAOA is approximate in general but matched the global optimum in this simulation-scale experiment.
- Constraint satisfaction under QAOA is not guaranteed in principle because constraints are encoded via penalties; feasibility depends on correct encoding and penalty scaling.

## 8. Critical Evaluation
**Core question:** Did this experiment demonstrate quantum advantage?

**Answer:** **No (for this experiment).**

Reasons:
1. **Small problem size (N=5):** exhaustive classical search is trivial and yields an exact optimum.
2. **QAOA is approximate:** solution quality depends on circuit depth (`reps`), optimizer behavior, and parameter initialization.
3. **Penalty-based constraints:** QUBO constraints are embedded as penalties rather than enforced exactly; feasibility can be sensitive to penalty scaling and encoding conventions.
4. **Hardware/realism limitations:** results here are produced via simulator-style primitives; real hardware noise and limited depth typically degrade performance.

Report-ready paragraph:
> The proposed hybrid quantum-classical framework does not demonstrate a clear quantum advantage for the given problem size. Classical brute-force enumeration provides exact solutions efficiently for small-scale instances, while QAOA is an approximate method whose performance depends on circuit depth, optimizer dynamics, and penalty-based constraint encoding. Nevertheless, the study demonstrates a complete and scalable workflow for reformulating realistic portfolio objectives into QUBO form and solving them with quantum-ready optimization tools, which becomes increasingly relevant as problem sizes grow beyond the reach of exhaustive classical methods.

## 9. Conclusion
This project implemented a realistic multi-objective portfolio optimization model and successfully mapped it into a QUBO formulation suitable for quantum optimization. A classical brute-force baseline provided a ground-truth optimum, and QAOA matched that optimum for the tested instance.

Future work:
- Scale $N$ and use stronger classical baselines (MILP/MIQP solvers, heuristics) for meaningful comparisons.
- Systematically tune penalty weights and analyze feasibility/optimality trade-offs.
- Test deeper QAOA circuits and alternative optimizers.
- Execute on real quantum hardware and quantify noise impact.
