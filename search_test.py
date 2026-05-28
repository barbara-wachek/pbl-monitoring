from playwright.sync_api import sync_playwright
import os
from datetime import datetime

from config import SCREENSHOT_DIR


# ======================
# ANTI-POPUP HANDLER
# ======================
def close_popups(page):

    try:
        cookie_btn = page.locator(".cookie-bar__button")
        if cookie_btn.count() > 0 and cookie_btn.first.is_visible():
            cookie_btn.first.click(timeout=2000)
            page.wait_for_timeout(800)
    except Exception:
        pass

    try:
        welcome_btn = page.locator(".welcome-bar__button")
        if welcome_btn.count() > 0 and welcome_btn.first.is_visible():
            welcome_btn.first.click(timeout=2000)
            page.wait_for_timeout(800)
    except Exception:
        pass

    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


# ======================
# MAIN TEST (URL-BASED SEARCH)
# ======================
def test_search_tokarczuk():

    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    screenshot_path = os.path.join(
        SCREENSHOT_DIR,
        f"search_tokarczuk_{timestamp}.png"
    )

    url = "https://pbl.ibl.waw.pl/results?q=Tokarczuk&area=all"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # wejście bezpośrednio w wyniki
            page.goto(url, timeout=30000, wait_until="domcontentloaded")

            # stabilizacja JS
            page.wait_for_timeout(3000)

            # pop-upy (nadal mogą się pojawić na results page)
            close_popups(page)

            # dodatkowe krótkie dociążenie DOM
            page.wait_for_timeout(1500)

            # pobranie treści strony
            body_text = page.locator("body").inner_text().lower()

            # prosty, stabilny warunek
            results_exist = "tokarczuk" in body_text

            # screenshot (debug / email)
            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            return results_exist, screenshot_path

        finally:
            browser.close()