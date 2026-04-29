# Notes

## Checkpoint 7 — Comparative Analysis (Classical vs Quantum)

Reproducibility command:

```bash
python results/compare.py
```

### 1) Results Summary

| Method                  | Solution (x)      | #Assets | Objective (original) | Feasible (K=2?) |
| ----------------------- | ----------------- | ------: | -------------------: | --------------- |
| Classical (Brute Force) | `[1, 0, 0, 1, 0]` |       2 |               2.9000 | ✔               |
| QAOA                    | `[1, 0, 0, 1, 0]` |       2 |               2.9000 | ✔               |

Notes:
- The “Objective (original)” is the composite objective implemented in `utils/objective.py`.
- QAOA internally minimizes the QUBO energy; for comparison we evaluate the same original objective for both solutions.

### 2) Solution Quality

**Observation**
- Brute force returns the global optimum by exhaustive enumeration.
- In this instance, QAOA converged to the same optimal portfolio.

**Interpretation**
- For small $N$, brute force is exact and provides a ground-truth benchmark.
- QAOA is approximate in general, but can match the optimum on small instances (especially when the QUBO encoding and penalty scaling are consistent).

**Report-ready text**
> The classical brute-force method provides an exact global optimum by enumerating all configurations. QAOA, implemented as a hybrid quantum-classical loop, produced a solution that matched the classical optimum for this small-scale instance, demonstrating that the QUBO encoding is compatible with quantum optimization.

### 3) Constraint Satisfaction (Cardinality)

Constraint:
$$\sum_i x_i = K = 2$$

**Observation**
- Classical optimum satisfies the constraint.
- QAOA also returns a feasible solution in this run.

**Interpretation**
- In QAOA/QUBO pipelines, constraints are typically enforced via penalty terms. Feasibility therefore depends on penalty scaling and a correct QUBO mapping convention.

**Report-ready text**
> Constraint satisfaction in QAOA depends on penalty-based encoding. With appropriate penalty scaling and consistent QUBO construction, the quantum solver can recover feasible portfolios; however, feasibility is not guaranteed a priori.

### 4) Convergence Behavior

- Brute force has no convergence issue (finite exhaustive search).
- QAOA relies on a hybrid loop (quantum circuit sampling + classical parameter optimization) and may converge to local minima depending on circuit depth (`reps`), optimizer choice, and initialization.

**Report-ready text**
> QAOA relies on iterative hybrid optimization and may converge to local minima depending on circuit depth and optimizer settings, whereas brute force deterministically identifies the best solution for small $N$.

### 5) Computational Complexity & Scalability

- Brute force scales as $O(2^N)$ and becomes intractable as $N$ grows.
- QAOA circuit resources and optimizer iterations grow with $N$; it is a candidate approach for larger combinatorial instances, subject to current hardware and noise limitations.

**Report-ready text**
> While brute-force enumeration becomes intractable as the number of assets increases, quantum approaches like QAOA offer a potential pathway to mitigate combinatorial explosion, subject to circuit depth and hardware limitations.

### 6) Practical Limitations

- Small problem size ($N=5$) favors classical methods.
- QAOA quality depends on penalty tuning and parameter optimization.
- Shallow circuits (`reps=2`) limit expressivity; deeper circuits increase runtime/noise sensitivity.

### 7) Key Insights

- Modeling and encoding matter as much as the solver choice.
- Constraint encoding via penalties is sensitive to scaling.
- QAOA can match the classical optimum on small instances, but quantum advantage is not guaranteed at small scale.

### 8) Mini-Conclusion

> The hybrid quantum-classical approach demonstrates feasibility in encoding and solving a multi-objective portfolio optimization problem in QUBO form. For the small-scale instance studied, QAOA matched the classical global optimum. The experiment highlights the importance of correct QUBO mapping and penalty scaling, and underscores both the potential and current limitations of quantum optimization for financial applications.
