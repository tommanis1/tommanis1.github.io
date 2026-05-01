#!/usr/bin/env python3
"""Capture the local site and overlay its red wave on the reference image."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "ChatGPT Image May 1, 2026, 12_40_28 PM.png"
SITE_INDEX = ROOT / "_site" / "index.html"
CAPTURE_INDEX = ROOT / "_site" / "screenshot-index.html"
SITE_SCREENSHOT = ROOT / "site_screenshot.png"
BLEND_OUTPUT = ROOT / "site_reference_blend.png"
WAVE_OVERLAY_OUTPUT = ROOT / "wave_overlay_compare.png"
WAVE_MASK_OUTPUT = ROOT / "site_wave_red_mask.png"


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def build_site(skip_build: bool) -> None:
    if not skip_build:
        run(["make", "build"])


def write_capture_html() -> None:
    html = SITE_INDEX.read_text()
    html = html.replace('href="/', 'href="').replace('src="/', 'src="')
    html = html.replace(
        "<head>",
        '<head><script>localStorage.setItem("theme","light");'
        'document.documentElement.dataset.theme="light";</script>',
        1,
    )
    CAPTURE_INDEX.write_text(html)


def capture_site(chrome: str, width: int, height: int) -> None:
    command = [
        chrome,
        "--headless=new",
        "--no-sandbox",
        "--allow-file-access-from-files",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-breakpad",
        "--disable-crashpad",
        "--disable-crash-reporter",
        "--disable-features=Crashpad",
        "--no-zygote",
        "--single-process",
        "--user-data-dir=/tmp/chrome-wave-compare",
        f"--window-size={width},{height}",
        f"--screenshot={SITE_SCREENSHOT}",
        CAPTURE_INDEX.resolve().as_uri(),
    ]
    run(command)


def create_overlays() -> None:
    reference = Image.open(REFERENCE).convert("RGBA")
    site = Image.open(SITE_SCREENSHOT).convert("RGBA")

    if site.size != reference.size:
        site = site.resize(reference.size, Image.Resampling.LANCZOS)

    Image.blend(reference, site, 0.5).save(BLEND_OUTPUT)

    site_rgb = np.array(site.convert("RGB"))
    red = site_rgb[:, :, 0].astype(int)
    green = site_rgb[:, :, 1].astype(int)
    blue = site_rgb[:, :, 2].astype(int)
    rows, cols = red.shape
    yy, xx = np.mgrid[:rows, :cols]
    hero_wave_region = (xx > 430) & (yy > 90) & (yy < 700)
    red_wave = (red > 150) & (red - green > 45) & (red - blue > 45) & hero_wave_region

    mask = np.zeros((*red_wave.shape, 4), dtype=np.uint8)
    mask[red_wave] = [255, 0, 0, 210]
    Image.fromarray(mask, "RGBA").save(WAVE_MASK_OUTPUT)

    overlay = Image.alpha_composite(reference, Image.fromarray(mask, "RGBA"))
    overlay.save(WAVE_OVERLAY_OUTPUT)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument("--chrome", default=shutil.which("google-chrome") or "/usr/bin/google-chrome")
    args = parser.parse_args()

    width, height = Image.open(REFERENCE).size
    build_site(args.skip_build)
    write_capture_html()
    capture_site(args.chrome, width, height)
    create_overlays()

    print(f"Wrote {SITE_SCREENSHOT}")
    print(f"Wrote {BLEND_OUTPUT}")
    print(f"Wrote {WAVE_MASK_OUTPUT}")
    print(f"Wrote {WAVE_OVERLAY_OUTPUT}")


if __name__ == "__main__":
    main()
