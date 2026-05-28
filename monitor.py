import requests
import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from config import URL, LOG_DIR
from screenshot import take_screenshot
from mailer import send_email
from search_test import test_search_tokarczuk
from google_sheets import append_log






print("MONITOR STARTED")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "monitor.log")),
        logging.StreamHandler()
    ]
)


def check_site():
    try:
        r = requests.get(URL, timeout=10)
        return r.status_code == 200, r.elapsed.total_seconds()
    except Exception as e:
        return False, str(e)


# ======================
# MAIN RUN (CRASH SAFE)
# ======================
def run():

    try:
        print("RUN START")

        timestamp = datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d %H:%M:%S")

        # ======================
        # SITE CHECK
        # ======================
        ok, info = check_site()

        # ======================
        # SEARCH TEST
        # ======================
        search_ok = False

        try:
            search_ok, _ = test_search_tokarczuk()
        except Exception as e:
            logging.error(f"Search test failed: {e}")
            search_ok = False

        overall_ok = ok and search_ok

        screenshot_path = None

        # ======================
        # SCREENSHOT (ONLY ON ERROR)
        # ======================
        if not overall_ok:
            try:
                screenshot_path = take_screenshot()
                logging.info(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                logging.error(f"Screenshot failed: {e}")
                screenshot_path = None

        # ======================
        # GOOGLE SHEETS (ALWAYS TRY)
        # ======================
        try:
            append_log(
                overall_ok,
                search_ok,
                str(info)
            )
            logging.info("Sheets log written successfully")

        except Exception as e:
            logging.error(f"Sheets logging failed: {e}")

        # ======================
        # EMAIL REPORT
        # ======================
        try:
            if overall_ok:
                subject = "PBL OK"
                body = (
                    f"[{timestamp}]\n"
                    f"System OK\n"
                    f"Site OK\n"
                    f"Search OK (Tokarczuk)\n"
                    f"Info: {info}"
                )

                logging.info("System healthy")
                send_email(subject, body)

            else:
                subject = "PBL ERROR"
                body = (
                    f"[{timestamp}]\n"
                    f"Problem detected\n"
                    f"Site OK: {ok}\n"
                    f"Search OK: {search_ok}\n"
                    f"Info: {info}"
                )

                logging.error("System failure")

                send_email(
                    subject,
                    body,
                    attachment_path=screenshot_path
                )

        except Exception as e:
            logging.critical(f"Email sending failed: {e}")

        print("SITE CHECK DONE")

    # ======================
    # GLOBAL CRASH HANDLER
    # ======================
    except Exception as e:

        logging.critical(f"CRITICAL CRASH: {e}")

        try:
            append_log(False, False, f"CRASH: {e}")
        except Exception:
            pass

        try:
            send_email(
                "PBL CRITICAL ERROR",
                f"Monitor crashed:\n\n{e}"
            )
        except Exception:
            pass

        raise


if __name__ == "__main__":
    run()