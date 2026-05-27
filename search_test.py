from playwright.sync_api import sync_playwright
import os
from datetime import datetime

from config import URL, SCREENSHOT_DIR


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

            page.goto(URL, timeout=30000)

            page.wait_for_timeout(5000)

            # ======================
            # COOKIES
            # ======================

            try:
                cookies_btn = page.locator(
                    ".cookie-bar__button"
                )

                if cookies_btn.is_visible():
                    cookies_btn.click()

                    page.wait_for_timeout(1500)

            except Exception as e:
                print("Cookies error:", e)

            # ======================
            # WELCOME BAR
            # ======================

            try:
                welcome_btn = page.locator(
                    ".welcome-bar__button"
                )

                if welcome_btn.is_visible():
                    welcome_btn.click()

                    page.wait_for_timeout(2000)

            except Exception as e:
                print("Welcome error:", e)

            # ======================
            # MAIN SEARCH
            # ======================

            # bierzemy DRUGI input
            # pierwszy jest mobile hidden

            search_input = page.locator(
                "input[name='key']"
            ).nth(1)

            search_input.wait_for(timeout=10000)

            search_input.fill("Tokarczuk")

            page.wait_for_timeout(1000)

            # ======================
            # SUBMIT BUTTON
            # ======================

            submit_button = page.locator(
                "button[type='submit']"
            ).nth(1)

            submit_button.click()

            # ======================
            # WAIT
            # ======================

            page.wait_for_timeout(6000)

            current_url = page.url.lower()

            body_text = page.locator("body").inner_text().lower()

            # ======================
            # VALIDATION
            # ======================

            results_exist = (
                "tokarczuk" in body_text
                and "/results" in current_url
            )

            # ======================
            # SCREENSHOT
            # ======================

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            return results_exist, screenshot_path

        finally:
            browser.close()