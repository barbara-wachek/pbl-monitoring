import os

URL = "https://pbl.ibl.waw.pl"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# EMAIL
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_FROM = "barbara.wachek@ibl.waw.pl"
EMAIL_PASSWORD = "uqsu jbcy luqh vpdn"
EMAIL_TO = "barbara.wachek@ibl.waw.pl"

# TEST SEARCH
TEST_QUERY = "Tokarczuk"

# PATHS
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
LOG_DIR = os.path.join(BASE_DIR, "logs")


CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")


GOOGLE_SHEET_NAME = "PBL monitoring logs"