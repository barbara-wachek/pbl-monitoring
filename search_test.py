from playwright.sync_api import sync_playwright
import os
from config import SCREENSHOT_DIR


# ======================
# POPUP HANDLER (SAFE)
# ======================
def close_popups(page):
    selectors = [
        ".cookie-bar__button",
        ".welcome-bar__button"
    ]

    for sel in selectors:
        try:
            loc = page.locator(sel)

            if loc.count() > 0:
                btn = loc.first

                if btn.is_visible():
                    btn.click(timeout=2000)

        except Exception:
            # ignorujemy, bo popupy są niestabilne z definicji
            pass

    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


# ======================
# MAIN TEST
# ======================
def test_search_tokarczuk():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    url = "https://pbl.ibl.waw.pl/results?q=Tokarczuk&area=all"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            response = page.goto(url, timeout=30000, wait_until="domcontentloaded")

            if not response or response.status >= 400:
                raise Exception(f"HTTP ERROR: {response.status if response else 'no response'}")

            # stabilizacja DOM
            page.wait_for_selector("ul.results__list", timeout=15000)

            # popupy po załadowaniu DOM
            close_popups(page)

            # teraz dopiero sprawdzamy wyniki
            items = page.locator("ul.results__list li")

            if items.count() == 0:
                raise Exception("No results found")

            return True, items.count()

        finally:
            browser.close()