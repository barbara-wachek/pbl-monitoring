# PBL-monitoring

Automatyczny monitoring serwisu https://pbl.ibl.waw.pl/.

Repozytorium służy do codziennego sprawdzania dostępności strony internetowej Polskiej Bibliografii Literackiej oraz poprawności działania wyszukiwarki serwisu. System wykonuje testy automatyczne, zapisuje logi, tworzy screenshoty w przypadku błędów i wysyła raporty mailowe na wskazany adres.

## Technologie i biblioteki

Projekt został przygotowany w Pythonie z wykorzystaniem:

* `requests` — sprawdzanie dostępności strony i czasu odpowiedzi,
* `Playwright` — automatyzacja przeglądarki i testowanie wyszukiwarki,
* `gspread` + Google Sheets API — zapisywanie logów do arkusza Google,
* `smtplib` — wysyłka raportów mailowych,
* `python-dotenv` — obsługa zmiennych środowiskowych,
* `GitHub Actions` — codzienny scheduler uruchamiający monitoring automatycznie.

## Jak działa monitoring

Workflow uruchamia się automatycznie codziennie o godzinie 07:00 (GitHub Actions scheduler).

Monitoring wykonuje:

1. sprawdzenie dostępności strony,
2. test wyszukiwarki (fraza: „Tokarczuk”),
3. zapis logów,
4. wykonanie screenshotu przy błędzie,
5. wysyłkę raportu mailowego,
6. zapis statusu do Google Sheets: https://docs.google.com/spreadsheets/d/1-lqkngW5dvekVcddgo9ocZp8OGMDufNVPF7vDL19sW8/edit?gid=0#gid=0 

## Struktura repozytorium

### Foldery

* `.github` — konfiguracja GitHub Actions,


### Pliki

* `.env` — lokalne zmienne środowiskowe (niecommitowane),
* `.gitignore` — lista ignorowanych plików,
* `config.py` — konfiguracja aplikacji,
* `google_sheets.py` — zapis logów do Google Sheets,
* `mailer.py` — wysyłka raportów mailowych,
* `monitor.py` — główny skrypt monitorujący,
* `requirements.txt` — lista zależności,
* `screenshot.py` — wykonywanie screenshotów,
* `search_test.py` — test wyszukiwarki,
* `test_sheets.py` — test połączenia z Google Sheets.

## Raportowanie

Raporty są:

* wysyłane mailowo,
* zapisywane w Google Sheets,

W przypadku błędów system automatycznie tworzy screenshot strony i dołącza go do wiadomości e-mail.
