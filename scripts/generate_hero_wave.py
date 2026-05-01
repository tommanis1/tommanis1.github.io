#!/usr/bin/env python3
"""Generate the hero wave SVG from a fitted contour curve."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "images" / "hero-wave.svg"

WIDTH = 1096
HEIGHT = 595
RIGHT_PIN_X = 1400.0
LEFT_ANCHOR_X = 516.0
TAPER_POWER = 1.25
LINE_COUNT = 23
DX_STEP = -1.8
DY_STEP = 23.0

BASE_PATH = [
    ("M", (516.0, 595.0)),
    ("C", (526.7, 576.3), (537.3, 557.7), (548.0, 539.0)),
    ("C", (560.7, 516.7), (573.3, 481.7), (586.0, 472.0)),
    ("C", (614.0, 450.7), (642.0, 454.6), (670.0, 446.0)),
    ("C", (686.7, 440.9), (703.3, 441.0), (720.0, 431.0)),
    ("C", (733.3, 423.0), (746.7, 410.5), (760.0, 392.0)),
    ("C", (773.3, 373.5), (786.7, 348.7), (800.0, 320.0)),
    ("C", (816.7, 284.1), (833.3, 225.6), (850.0, 198.0)),
    ("C", (876.0, 154.9), (902.0, 119.3), (928.0, 108.0)),
    ("C", (958.0, 95.0), (988.0, 112.9), (1018.0, 125.0)),
    ("C", (1044.0, 135.5), (1070.0, 159.0), (1096.0, 176.0)),
]


def tapered_offset(point: tuple[float, float], dx: float, dy: float) -> tuple[float, float]:
    x, y = point
    progress = (RIGHT_PIN_X - x) / (RIGHT_PIN_X - LEFT_ANCHOR_X)
    progress = max(0.0, min(1.0, progress))
    scale = progress**TAPER_POWER
    return x + dx * scale, y + dy * scale


def fmt_point(point: tuple[float, float]) -> str:
    return f"{point[0]:.1f} {point[1]:.1f}"


def path_for_line(index: int) -> str:
    dx = DX_STEP * index
    dy = DY_STEP * index
    parts: list[str] = []

    for command in BASE_PATH:
        if command[0] == "M":
            parts.append(f"M{fmt_point(tapered_offset(command[1], dx, dy))}")
        else:
            p1 = tapered_offset(command[1], dx, dy)
            p2 = tapered_offset(command[2], dx, dy)
            p3 = tapered_offset(command[3], dx, dy)
            parts.append(f"C{fmt_point(p1)} {fmt_point(p2)} {fmt_point(p3)}")

    return " ".join(parts)


def main() -> None:
    paths = "\n".join(
        f'    <path d="{path_for_line(i)}"/>' for i in range(LINE_COUNT)
    )
    svg = f"""<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <g stroke="#fff" stroke-width="1.32" stroke-linecap="round" stroke-linejoin="round">
{paths}
  </g>
</svg>
"""
    OUTPUT.write_text(svg)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
