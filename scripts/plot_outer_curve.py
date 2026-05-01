#!/usr/bin/env python3
"""Approximate and plot the outer wave curve from the reference screenshot."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
IMAGE_PATH = ROOT / "ChatGPT Image May 1, 2026, 12_40_28 PM.png"
OUTPUT_PATH = ROOT / "outer_curve_fit.png"

# Hand-picked points on the visible outer ridge in image pixel coordinates.
# x increases left-to-right; y increases downward, matching image coordinates.
OUTER_CURVE_POINTS = np.array(
    [
        (516, 677),
        (548, 621),
        (586, 554),
        (670, 528),
        (720, 513),
        (760, 474),
        (800, 402),
        (850, 280),
        (928, 190),
        (1018, 207),
        (1096, 258),
    ],
    dtype=float,
)


def _hermite_slopes(points: np.ndarray) -> np.ndarray:
    """Return finite-difference slopes dy/dx for cubic Hermite interpolation."""
    x = points[:, 0]
    y = points[:, 1]
    slopes = np.empty_like(x)
    slopes[0] = (y[1] - y[0]) / (x[1] - x[0])
    slopes[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])
    slopes[1:-1] = (y[2:] - y[:-2]) / (x[2:] - x[:-2])
    return slopes


SLOPES = _hermite_slopes(OUTER_CURVE_POINTS)


def outer_curve_y(x_values: float | np.ndarray) -> float | np.ndarray:
    """Return y pixel coordinate on the outer curve for x pixel coordinate(s).

    The function is defined only over the wave interval
    [516, 1096]. Values outside that interval return NaN.
    """
    scalar = np.isscalar(x_values)
    xq = np.asarray(x_values, dtype=float)
    yq = np.full_like(xq, np.nan, dtype=float)

    x = OUTER_CURVE_POINTS[:, 0]
    y = OUTER_CURVE_POINTS[:, 1]

    inside = (xq >= x[0]) & (xq <= x[-1])
    bins = np.searchsorted(x, xq[inside], side="right") - 1
    bins = np.clip(bins, 0, len(x) - 2)

    x0 = x[bins]
    x1 = x[bins + 1]
    y0 = y[bins]
    y1 = y[bins + 1]
    m0 = SLOPES[bins]
    m1 = SLOPES[bins + 1]

    h = x1 - x0
    t = (xq[inside] - x0) / h
    h00 = 2 * t**3 - 3 * t**2 + 1
    h10 = t**3 - 2 * t**2 + t
    h01 = -2 * t**3 + 3 * t**2
    h11 = t**3 - t**2
    yq[inside] = h00 * y0 + h10 * h * m0 + h01 * y1 + h11 * h * m1

    if scalar:
        return float(yq)
    return yq


def plot_curve() -> None:
    image = Image.open(IMAGE_PATH)
    width, height = image.size

    xs = np.linspace(OUTER_CURVE_POINTS[0, 0], OUTER_CURVE_POINTS[-1, 0], 800)
    ys = outer_curve_y(xs)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

    axes[0].imshow(image)
    axes[0].plot(xs, ys, color="#d62728", linewidth=3, label="outer_curve_y(x)")
    axes[0].scatter(
        OUTER_CURVE_POINTS[:, 0],
        OUTER_CURVE_POINTS[:, 1],
        color="#1f77b4",
        s=24,
        label="control points",
    )
    axes[0].set_xlim(450, width)
    axes[0].set_ylim(730, 150)
    axes[0].set_title("Overlay on reference image")
    axes[0].legend(loc="lower right")

    axes[1].plot(xs, height - ys, color="#11735f", linewidth=3)
    axes[1].scatter(
        OUTER_CURVE_POINTS[:, 0],
        height - OUTER_CURVE_POINTS[:, 1],
        color="#1f77b4",
        s=24,
    )
    axes[1].set_title("Mathematical view: height - outer_curve_y(x)")
    axes[1].set_xlabel("x pixels")
    axes[1].set_ylabel("y pixels from bottom")
    axes[1].grid(True, alpha=0.25)

    fig.savefig(OUTPUT_PATH, dpi=180)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    plot_curve()
