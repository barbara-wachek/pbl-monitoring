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


def build_result(site_ok, search_ok, info, screenshot_path):
    return {
        "timestamp": datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d %H:%M:%S"),
        "site_ok": site_ok,
        "search_ok": search_ok,
        "overall_ok": site_ok and search_ok,
        "info": info,
        "screenshot": screenshot_path
    }


def run():
    try:
        print("RUN START")

        # ======================
        # SITE CHECK
        # ======================
        site_ok, info = check_site()

        # ======================
        # SEARCH TEST
        # ======================
        search_ok = False
        try:
            search_ok, _ = test_search_tokarczuk()
        except Exception as e:
            logging.error(f"Search test failed: {e}")
            search_ok = False

        # ======================
        # SCREENSHOT ONLY ON ERROR
        # ======================
        screenshot_path = None
        if not (site_ok and search_ok):
            try:
                screenshot_path = take_screenshot()
                logging.info(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                logging.error(f"Screenshot failed: {e}")

        # ======================
        # UNIFIED RESULT
        # ======================
        result = build_result(site_ok, search_ok, info, screenshot_path)

        # ======================
        # GOOGLE SHEETS
        # ======================
        try:
            append_log(result)
            logging.info("Sheets log written successfully")
        except Exception as e:
            logging.error(f"Sheets logging failed: {e}")

        # ======================
        # EMAIL
        # ======================
        try:
            if result["overall_ok"]:
                subject = "PBL OK"
                body = (
                    f"[{result['timestamp']}]\n"
                    f"System OK\n"
                    f"Site OK\n"
                    f"Search OK (Tokarczuk)\n"
                    f"Info: {result['info']}"
                )
            else:
                subject = "PBL ERROR"
                body = (
                    f"[{result['timestamp']}]\n"
                    f"Problem detected\n"
                    f"Site OK: {result['site_ok']}\n"
                    f"Search OK: {result['search_ok']}\n"
                    f"Info: {result['info']}"
                )

            send_email(
                subject,
                body,
                attachment_path=result["screenshot"]
            )

            logging.info("Email sent")

        except Exception as e:
            logging.critical(f"Email sending failed: {e}")

        print("SITE CHECK DONE")

    except Exception as e:
        logging.critical(f"CRITICAL CRASH: {e}")

        try:
            append_log({
                "timestamp": datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d %H:%M:%S"),
                "site_ok": False,
                "search_ok": False,
                "overall_ok": False,
                "info": f"CRASH: {e}",
                "screenshot": None
            })
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