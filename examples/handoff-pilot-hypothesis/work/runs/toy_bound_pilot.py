#!/usr/bin/env python3
"""RUN-001 toy: δ-matrix bound pilot for HYP-001.

Architecture A (toy):
  x ~ N(0, epsilon^2 I / n)
  P: precondition (scales toward unit ball) -> kappa = ||P(x) - x||
  f: (I + delta * M) @ P(x)
  y: (I + delta_true * M_true) @ x  (ground truth on raw input)

Bound Y(epsilon, n, kappa) = C_delta * epsilon * sqrt(n) + C_kappa * kappa
  C_delta = ||delta_true M_true - delta M||_op
  C_kappa = ||I + delta M||_op
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass

import numpy as np


@dataclass
class RunConfig:
    n: int = 8
    epsilon: float = 1.0
    delta: float = 0.05
    delta_true: float = 0.08
    alpha_p: float = 0.15
    num_seeds: int = 12


@dataclass
class SeedResult:
    seed: int
    max_error: float
    y_bound: float
    kappa: float
    pass_fail: str


def precondition(x: np.ndarray, alpha: float) -> np.ndarray:
    norm = np.linalg.norm(x)
    if norm < 1e-12:
        return x.copy()
    return x / (1.0 + alpha * norm)


def kappa(x: np.ndarray, x_p: np.ndarray) -> float:
    return float(np.linalg.norm(x_p - x))


def f_transform(x: np.ndarray, delta: float, m: np.ndarray) -> np.ndarray:
    n = x.shape[0]
    return (np.eye(n) + delta * m) @ x


def y_bound(
    epsilon: float,
    n: int,
    kappa_val: float,
    c_delta: float,
    c_kappa: float,
) -> float:
    return c_delta * epsilon * np.sqrt(n) + c_kappa * kappa_val


def run_pilot(cfg: RunConfig) -> dict:
    rng = np.random.default_rng(42)
    m = rng.standard_normal((cfg.n, cfg.n))
    m = (m + m.T) / 2
    m_true = rng.standard_normal((cfg.n, cfg.n))
    m_true = (m_true + m_true.T) / 2

    eye = np.eye(cfg.n)
    c_delta = float(
        np.linalg.norm(cfg.delta_true * m_true - cfg.delta * m, ord=2)
    )
    c_kappa = float(np.linalg.norm(eye + cfg.delta * m, ord=2))

    results: list[SeedResult] = []
    for seed in range(cfg.num_seeds):
        local_rng = np.random.default_rng(seed)
        x = local_rng.standard_normal(cfg.n) * (cfg.epsilon / np.sqrt(cfg.n))
        x_p = precondition(x, cfg.alpha_p)
        k = kappa(x, x_p)
        y = f_transform(x, cfg.delta_true, m_true)
        y_hat = f_transform(x_p, cfg.delta, m)
        err = float(np.linalg.norm(y - y_hat))
        bound = y_bound(cfg.epsilon, cfg.n, k, c_delta, c_kappa)
        results.append(
            SeedResult(
                seed=seed,
                max_error=err,
                y_bound=bound,
                kappa=k,
                pass_fail="PASS" if err <= bound else "FAIL",
            )
        )

    failures = [r for r in results if r.pass_fail == "FAIL"]
    verdict = "accepted" if not failures else "rejected"

    return {
        "config": asdict(cfg),
        "pins": {
            "x": "R^n synthetic, N(0, epsilon^2 I / n)",
            "y": "(I + delta_true M_true) x",
            "f": "(I + delta M) P(x)",
            "kappa": "||P(x) - x||, P scales by 1/(1+alpha||x||)",
            "Y": "C_delta * epsilon * sqrt(n) + C_kappa * kappa",
        },
        "coefficients": {"C_delta": c_delta, "C_kappa": c_kappa},
        "results": [asdict(r) for r in results],
        "summary": {
            "max_observed_error": max(r.max_error for r in results),
            "max_bound": max(r.y_bound for r in results),
            "fail_count": len(failures),
            "verdict": verdict,
        },
    }


def main() -> int:
    out = run_pilot(RunConfig())
    print(json.dumps(out, indent=2))
    return 0 if out["summary"]["verdict"] == "accepted" else 1


if __name__ == "__main__":
    sys.exit(main())