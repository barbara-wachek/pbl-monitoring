import requests
import logging
import os
from datetime import datetime

from config import URL, LOG_DIR
from screenshot import take_screenshot
from mailer import send_email
from search_test import test_search_tokarczuk
from google_sheets import append_log


print("MONITOR STARTED")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "monitor.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def check_site():
    try:
        r = requests.get(URL, timeout=10)
        return r.status_code == 200, r.elapsed.total_seconds()
    except Exception as e:
        return False, str(e)


def run():
    print("RUN START")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ok, info = check_site()

    search_ok = True
    screenshot_path = None

    # SEARCH TEST
    try:
        search_ok, _ = test_search_tokarczuk()
    except Exception as e:
        search_ok = False
        logging.error(f"Search test failed: {e}")

    overall_ok = ok and search_ok

    # SCREENSHOT tylko przy błędzie
    if not overall_ok:
        try:
            screenshot_path = take_screenshot()
        except Exception as e:
            logging.error(f"Screenshot failed: {e}")

    # ======================
    # GOOGLE SHEETS LOG
    # ======================
    append_log(
        overall_ok,
        search_ok,
        str(info)
    )

    # ======================
    # EMAIL
    # ======================
    if overall_ok:
        subject = "PBL OK"
        body = (
            f"[{timestamp}]\n"
            f"System OK\n"
            f"Site OK\n"
            f"Search OK (Tokarczuk)\n"
            f"Info: {info}"
        )

        logging.info("OK - full system healthy")
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

        logging.error("ERROR - system failure")
        send_email(subject, body, attachment_path=screenshot_path)

    print("SITE CHECK DONE")
    
    
    
if __name__ == "__main__":
    run()
    
    
    
    
    
    
    
    