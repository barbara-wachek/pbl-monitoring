import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

from config import (
    GOOGLE_CREDENTIALS,
    GOOGLE_SHEET_ID
)


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def get_sheet():

    creds = Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=SCOPES
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_key(
        GOOGLE_SHEET_ID
    ).sheet1

    return sheet



def ensure_headers(sheet):

    first_row = sheet.row_values(1)

    if not first_row:

        sheet.append_row([
            "timestamp",
            "site_ok",
            "search_ok",
            "info"
        ])

def append_log(site_ok, search_ok, info):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    sheet = get_sheet()

    ensure_headers(sheet)

    sheet.append_row([
        timestamp,
        str(site_ok),
        str(search_ok),
        str(info)
    ])