import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

from config import CREDENTIALS_FILE

SHEET_ID = "1-lqkngW5dvekVcddgo9ocZp8OGMDufNVPF7vDL19sW8"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]


def get_sheet():
    creds = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=SCOPES
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1

    return sheet


def ensure_headers(sheet):
    if not sheet.row_values(1):
        sheet.append_row([
            "timestamp",
            "site_ok",
            "search_ok",
            "info"
        ])


def append_log(site_ok, search_ok, info):
    # 👉 timestamp generowany tutaj, zawsze aktualny
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet = get_sheet()
    ensure_headers(sheet)

    sheet.append_row([
        timestamp,
        str(site_ok),
        str(search_ok),
        str(info)
    ])