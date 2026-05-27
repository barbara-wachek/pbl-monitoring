import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from config import SCREENSHOT_DIR, URL


def take_screenshot():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"pbl_screenshot_{timestamp}.png"
    path = os.path.join(SCREENSHOT_DIR, filename)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(URL, timeout=20000)
            page.wait_for_timeout(5000)
            page.screenshot(path=path, full_page=True)
        finally:
            browser.close()

    return path