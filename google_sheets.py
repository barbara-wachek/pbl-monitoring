import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo

from config import (
    GOOGLE_CREDENTIALS,
    GOOGLE_SHEET_ID
)

# ======================
# GOOGLE SCOPES
# ======================
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

EXPECTED_HEADERS = ["timestamp", "site_ok", "search_ok", "info"]


def get_sheet():

    creds = Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=SCOPES
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

    return sheet


def ensure_headers(sheet):

    first_row = sheet.row_values(1)

    if first_row != EXPECTED_HEADERS:
        sheet.clear()
        sheet.append_row(EXPECTED_HEADERS)


def append_log(site_ok, search_ok, info):

    try:
        timestamp = datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d_%H-%M-%S")

        sheet = get_sheet()
        ensure_headers(sheet)

        sheet.append_row([
            timestamp,
            str(site_ok),
            str(search_ok),
            str(info)
        ])

        print("SHEETS WRITE OK")

    except Exception as e:
        print("SHEETS ERROR:", e)
        raise