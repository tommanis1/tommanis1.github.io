#!/usr/bin/env python3
"""Render built pages in forced dark mode and screenshot them with headless Chrome.

For each (page, viewport) it writes a temporary capture HTML next to _site with
`data-theme="dark"` hardcoded on <html> and absolute file:// asset URLs, then uses
google-chrome --headless to capture a PNG.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
OUT = ROOT / "dark_audit"

# (source built html, output name)
PAGES = [
    (SITE / "index.html", "home"),
    (SITE / "contact" / "index.html", "contact"),
]

# (label, width, height)
VIEWPORTS = [
    ("desktop", 1440, 1900),
    ("mobile", 414, 1700),
]


def make_capture_html(src: Path) -> Path:
    html = src.read_text()
    # Absolute file:// URLs so assets resolve regardless of capture-file location.
    site_uri = SITE.resolve().as_uri()  # file:///.../_site
    html = html.replace('href="/', f'href="{site_uri}/')
    html = html.replace('src="/', f'src="{site_uri}/')
    # Force the site's own dark theme at parse time.
    html = html.replace('<html lang="en">', '<html lang="en" data-theme="dark">', 1)
    html = html.replace(
        "<head>",
        '<head><script>localStorage.setItem("theme","dark");'
        'document.documentElement.dataset.theme="dark";</script>',
        1,
    )
    capture = src.parent / f"__dark_capture_{src.stem}.html"
    capture.write_text(html)
    return capture


def capture(chrome: str, capture_html: Path, out_png: Path, width: int, height: int) -> None:
    command = [
        chrome,
        "--headless=new",
        "--no-sandbox",
        "--hide-scrollbars",
        "--allow-file-access-from-files",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-breakpad",
        "--disable-crashpad",
        "--disable-crash-reporter",
        "--disable-features=Crashpad",
        "--force-color-profile=srgb",
        "--user-data-dir=/tmp/chrome-dark-audit",
        f"--window-size={width},{height}",
        f"--screenshot={out_png}",
        capture_html.resolve().as_uri(),
    ]
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    chrome = shutil.which("google-chrome") or "/usr/bin/google-chrome"
    OUT.mkdir(exist_ok=True)
    written = []
    for src, name in PAGES:
        if not src.exists():
            print(f"skip missing {src}")
            continue
        cap = make_capture_html(src)
        try:
            for label, w, h in VIEWPORTS:
                out_png = OUT / f"{name}_{label}_dark.png"
                capture(chrome, cap, out_png, w, h)
                print(f"wrote {out_png}")
                written.append(out_png)
        finally:
            cap.unlink(missing_ok=True)
    print("\n".join(str(p) for p in written))


if __name__ == "__main__":
    main()
