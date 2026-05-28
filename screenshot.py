import os
from datetime import datetime
from zoneinfo import ZoneInfo
from playwright.sync_api import sync_playwright
from config import SCREENSHOT_DIR, URL


def take_screenshot():
    # absolutna ścieżka (ważne w GitHub Actions)
    base_dir = os.path.abspath(SCREENSHOT_DIR)
    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"pbl_screenshot_{timestamp}.png"
    path = os.path.join(base_dir, filename)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto(URL, timeout=20000)

            # zamiast fixed sleep → stabilniejsze
            page.wait_for_load_state("networkidle", timeout=15000)

            page.screenshot(path=path, full_page=True)

        finally:
            context.close()
            browser.close()

    return path