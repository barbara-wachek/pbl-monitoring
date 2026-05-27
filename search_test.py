from playwright.sync_api import sync_playwright, TimeoutError
import os
from datetime import datetime

from config import URL, SCREENSHOT_DIR


# ======================
# ANTI-POPUP HANDLER
# ======================
def close_popups(page):
    try:
        cookie_btn = page.locator(".cookie-bar__button")
        if cookie_btn.count() > 0 and cookie_btn.first.is_visible():
            cookie_btn.first.click(timeout=3000)
    except Exception:
        pass

    try:
        welcome_btn = page.locator(".welcome-bar__button")
        if welcome_btn.count() > 0 and welcome_btn.first.is_visible():
            welcome_btn.first.click(timeout=3000)
    except Exception:
        pass

    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


# ======================
# SINGLE SEARCH ATTEMPT
# ======================
def _run_search(page, screenshot_path):

    page.goto(URL, timeout=30000, wait_until="domcontentloaded")

    # popupy
    close_popups(page)

    # input (stabilny selector)
    search_input = page.locator("input[name='key']").first
    search_input.wait_for(timeout=10000)
    search_input.click()
    search_input.fill("Tokarczuk")

    # submit (fallback click + Enter)
    try:
        page.locator("button[type='submit']").first.click(timeout=3000)
    except Exception:
        page.keyboard.press("Enter")

    # czekamy na realny efekt (DOM zamiast sleep)
    try:
        page.wait_for_function(
            "document.body.innerText.toLowerCase().includes('tokarczuk')",
            timeout=15000
        )
    except TimeoutError:
        pass

    body_text = page.locator("body").inner_text().lower()
    current_url = page.url.lower()

    results_exist = (
        "tokarczuk" in body_text
    )

    page.screenshot(path=screenshot_path, full_page=True)

    return results_exist, screenshot_path


# ======================
# MAIN TEST (WITH RETRY)
# ======================
def test_search_tokarczuk():

    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    screenshot_path = os.path.join(
        SCREENSHOT_DIR,
        f"search_tokarczuk_{timestamp}.png"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # 1st attempt
            try:
                return _run_search(page, screenshot_path)
            except Exception:
                # retry once (fresh page)
                page.close()
                page = browser.new_page()
                return _run_search(page, screenshot_path)

        finally:
            browser.close()