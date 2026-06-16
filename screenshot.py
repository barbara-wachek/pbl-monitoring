import os
from datetime import datetime
from zoneinfo import ZoneInfo
from playwright.sync_api import sync_playwright

from config import SCREENSHOT_DIR, URL


def take_screenshot():
    base_dir = os.path.abspath(SCREENSHOT_DIR)
    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(base_dir, f"pbl_{timestamp}.png")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        try:
            page.goto(URL, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle", timeout=20000)
            page.wait_for_timeout(2000)  # stabilizacja JS
            page.screenshot(path=path, full_page=True)

        finally:
            context.close()
            browser.close()

    return path