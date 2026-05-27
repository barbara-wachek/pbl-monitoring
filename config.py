import os
import json
from dotenv import load_dotenv

load_dotenv()

# ======================
# TEST / DEBUG
# ======================
TEST_QUERY = "Tokarczuk"

# ======================
# PATHS
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# ======================
# GOOGLE SHEETS
# ======================
GOOGLE_SHEET_ID = "1-lqkngW5dvekVcddgo9ocZp8OGMDufNVPF7vDL19sW8"

GOOGLE_CREDENTIALS = json.loads(
    os.environ["GOOGLE_CREDENTIALS"].replace("\\n", "\n")
)

# ======================
# EMAIL / SMTP
# ======================
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_TO = os.environ["EMAIL_TO"]

SMTP_SERVER = os.environ["SMTP_SERVER"]
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

# ======================
# URL MONITOROWANY
# ======================
URL = os.environ.get("URL", "https://pbl.ibl.waw.pl/")