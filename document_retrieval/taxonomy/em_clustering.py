"""Expectation-maximisation clustering of observations with a Gaussian mixture."""

from __future__ import annotations

import copy
import math
import random
import sys
from typing import Any

import numpy as np


def expectation_maximization(
    observations: np.ndarray,
    nbclusters: int = 2,
    nbiter: int = 3,
    normalize: bool = False,
    epsilon: float = 0.001,
    monotony: bool = False,
    datasetinit: bool = True,
) -> dict[str, Any]:
    """Cluster ``observations`` (rows) with EM over a Gaussian mixture.

    ``nbclusters`` is the number of mixture components, ``nbiter`` the number
    of random restarts, and ``epsilon`` the convergence bound on the change of
    the log-likelihood.  The best of the ``nbiter`` runs (by ``quality``) is
    returned as ``{"quality", "params", "clusters"}``.

    Overview of one run:

    * Draw ``nbclusters`` sets of ``(mu, sigma, P_cluster)`` at random.
    * [E] Compute ``P(Cluster|obs)`` for every observation.
    * [M] Recompute the mixture parameters from those estimates.
    * Repeat until ``|E_t - E_{t-1}| < epsilon`` where
      ``E_t = sum_obs log P(obs)``.
    """
    min_float = sys.float_info.min

    def pnorm(x: np.ndarray, mean: np.ndarray, sigma: np.matrix) -> float:
        """Multivariate normal density of ``x``."""
        centered_t = np.matrix(x - mean).transpose()
        for i in range(len(sigma)):
            if sigma[i, i] <= min_float:
                sigma[i, i] = min_float
        sigma_inverse = np.linalg.inv(sigma)
        centered = np.matrix(x - mean)
        return (
            (2.0 * math.pi) ** (-len(x) / 2.0)
            * (1.0 / math.sqrt(np.linalg.det(sigma)))
            * math.exp(-0.5 * (centered * sigma_inverse * centered_t).item())
        )

    def draw_params() -> dict[str, Any]:
        if datasetinit:
            mean = np.array([1.0 * observations[random.randrange(nbobs), :]], np.float64)
        else:
            mean = np.array(
                [random.uniform(*min_max[f]) for f in range(nbfeatures)], np.float64
            )
        return {
            "mu": mean,
            "sigma": np.matrix(
                np.diag(
                    [(min_max[f][1] - min_max[f][0]) / 2.0 for f in range(nbfeatures)]
                )
            ),
            "proba": 1.0 / nbclusters,
        }

    def feature_ranges() -> list[tuple[float, float]]:
        return [
            (observations[:, f].min(), observations[:, f].max())
            for f in range(nbfeatures)
        ]

    nbobs = observations.shape[0]
    nbfeatures = observations.shape[1]
    min_max = feature_ranges()

    if normalize:
        for f in range(nbfeatures):
            observations[:, f] -= min_max[f][0]
            observations[:, f] /= min_max[f][1] - min_max[f][0]
    min_max = feature_ranges()

    result: dict[str, Any] = {}
    random.seed()
    cluster_given_obs = np.ndarray([nbobs, nbclusters], np.float64)  # P(clust|obs)
    obs_given_cluster = np.ndarray([nbobs, nbclusters], np.float64)  # P(obs|clust)

    for _ in range(nbiter):
        params = [draw_params() for _ in range(nbclusters)]
        old_log_estimate: float = sys.maxsize  # init, not true/real
        log_estimate: float = sys.maxsize // 2 + epsilon  # init, not true/real
        while abs(log_estimate - old_log_estimate) > epsilon and (
            not monotony or log_estimate < old_log_estimate
        ):
            restart = False
            old_log_estimate = log_estimate

            # E step: P(cluster|obs) for every observation.
            for o in range(nbobs):
                for c in range(nbclusters):
                    obs_given_cluster[o, c] = pnorm(
                        observations[o, :], params[c]["mu"], params[c]["sigma"]
                    )
            for o in range(nbobs):
                for c in range(nbclusters):
                    cluster_given_obs[o, c] = (
                        obs_given_cluster[o, c] * params[c]["proba"]
                    )
            for o in range(nbobs):
                total = 0.0
                for c in range(nbclusters):
                    total += params[c]["proba"] * obs_given_cluster[o, c]
                cluster_given_obs[o, :] /= total

            # M step: update {mu, sigma, proba}.
            for c in range(nbclusters):
                weight_sum = math.fsum(cluster_given_obs[:, c])
                params[c]["proba"] = weight_sum / nbobs
                if params[c]["proba"] <= 1.0 / nbobs:
                    # All observations converged to one cluster: restart.
                    restart = True
                    break
                mean = np.zeros(nbfeatures, np.float64)
                for o in range(nbobs):
                    mean += observations[o, :] * cluster_given_obs[o, c]
                params[c]["mu"] = mean / weight_sum
                sigma = np.matrix(np.diag(np.zeros(nbfeatures, np.float64)))
                for o in range(nbobs):
                    deviation = observations[o, :] - params[c]["mu"]
                    sigma += cluster_given_obs[o, c] * (
                        np.matrix(deviation).transpose() * np.matrix(deviation)
                    )
                params[c]["sigma"] = sigma / weight_sum

            if not restart:
                restart = True
                for c in range(1, nbclusters):
                    if not np.allclose(
                        params[c]["mu"], params[c - 1]["mu"]
                    ) or not np.allclose(params[c]["sigma"], params[c - 1]["sigma"]):
                        restart = False
                        break
            if restart:
                old_log_estimate = sys.maxsize
                log_estimate = sys.maxsize // 2 + epsilon
                params = [draw_params() for _ in range(nbclusters)]
                continue

            # Log estimate of the data likelihood.
            log_estimate = math.fsum(
                math.log(
                    math.fsum(
                        obs_given_cluster[o, c] * params[c]["proba"]
                        for c in range(nbclusters)
                    )
                )
                for o in range(nbobs)
            )

        # Keep the best clustering over all restarts.
        quality = -log_estimate
        if "quality" not in result or quality > result["quality"]:
            result["quality"] = quality
            result["params"] = copy.deepcopy(params)
            result["clusters"] = [
                [
                    o
                    for o in range(nbobs)
                    if obs_given_cluster[o, c] == max(obs_given_cluster[o, :])
                ]
                for c in range(nbclusters)
            ]
    return result
