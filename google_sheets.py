import gspread
from google.oauth2.service_account import Credentials

from config import GOOGLE_CREDENTIALS, GOOGLE_SHEET_ID

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

EXPECTED_HEADERS = [
    "timestamp",
    "site_ok",
    "search_ok",
    "overall_ok",
    "info",
    "screenshot"
]


def get_sheet():
    creds = Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=SCOPES
    )

    client = gspread.authorize(creds)
    return client.open_by_key(GOOGLE_SHEET_ID).sheet1


def ensure_headers(sheet):
    first_row = sheet.row_values(1)

    if first_row != EXPECTED_HEADERS:
        sheet.clear()
        sheet.append_row(EXPECTED_HEADERS)


def append_log(result: dict):
    try:
        sheet = get_sheet()
        ensure_headers(sheet)

        sheet.append_row([
            result["timestamp"],
            str(result["site_ok"]),
            str(result["search_ok"]),
            str(result["overall_ok"]),
            str(result["info"]),
            str(result["screenshot"])
        ])

        print("SHEETS WRITE OK")

    except Exception as e:
        print("SHEETS ERROR:", e)
        raise