# Copilot / AI agent instructions for the EPL explorer

Purpose: help AI coding assistants be immediately productive in this repository.

- **Run app (dev):** The app is a small Flask server. Run with:

  ```bash
  python3 src/app.py
  ```
  It listens on port `5001` and registers the API blueprint in `src/routes.py`.

- **Primary architecture:**
  - `src/app.py` wires Flask and templates. See [src/app.py](src/app.py#L1-L40).
  - `src/routes.py` exposes a single blueprint at `/api`—all JSON endpoints live here. See [src/routes.py](src/routes.py#L1-L200).
  - `src/services.py` contains the business logic that reads CSV season files from `data/` and returns JSON-ready dicts.
  - `src/utils.py` contains data loading (`load_data`) and core calculations (`calculate_team_stats`). Note `load_data` is cached with `lru_cache`.

- **Data model & conventions:**
  - Raw CSV files are expected in `data/` named `{season}_E0.csv` (e.g. `2526_E0.csv`). The downloader is `scripts/download_data.sh`.
  - `load_data(season, data_dir)` returns a pandas DataFrame and strips team name whitespace; services assume columns like `HomeTeam`, `AwayTeam`, `FTR`, `FTHG`, `FTAG`, `Date`.
  - Many service functions operate over the last 10 season files (sorted reverse). See `DATA_DIR = "data"` and file globbing in [src/services.py](src/services.py#L1-L60).

- **Editing guidance / common pitfalls:**
  - When changing data-loading behavior, update `src/utils.py::load_data` and be mindful of `@lru_cache` (clear or adjust cache during dev/tests).
  - Sorting/standings logic lives in `get_standings_service` and depends on `calculate_team_stats`. Keep point calculation consistent (3 points/win, 1/draw).
  - Dates are parsed with `pd.to_datetime(..., dayfirst=True)` in services; be cautious when changing date formats.

- **API examples:**
  - List seasons: `GET /api/seasons` → `curl http://localhost:5001/api/seasons`
  - Season stats: `GET /api/stats/2526` → `curl http://localhost:5001/api/stats/2526`
  - Team history: `GET /api/team-history/Arsenal` → `curl "http://localhost:5001/api/team-history/Arsenal"`

- **Files to inspect when debugging:**
  - `src/services.py` — business rules and file selection
  - `src/utils.py` — CSV parsing, cleaning, and core stats
  - `templates/` — front-end templates used by `src/app.py`
  - `scripts/download_data.sh` — how CSVs are fetched and named

- **Dependencies & env:**
  - The project expects `pandas` and `flask`. If a `requirements.txt` is added, use it; otherwise run `pip install pandas flask`.

If anything above is unclear or you want additional examples (tests, CI, or editing a specific service), tell me which area to expand.  