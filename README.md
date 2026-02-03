# EPL Explorer

Quickstart
---------

1. Create a virtual environment (recommended) and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Download season CSVs (optional — the repo includes example CSVs in `data/`):

```bash
bash scripts/download_data.sh
```

3. Run the development server:

```bash
python3 src/app.py
```

The Flask app listens on port `5001` by default. The single-page UI routes are served by `src/app.py` and the JSON API is exposed under the `/api` blueprint registered in `src/routes.py`.

Important files
---------------

- `src/app.py` — Flask app + template routes (index, team history, details).
- `src/routes.py` — API blueprint; all JSON endpoints live here (e.g. `/api/stats/<season>`).
- `src/services.py` — business logic: reads CSVs from `data/`, computes stats, standings, histories.
- `src/utils.py` — `load_data(season, data_dir)` and `calculate_team_stats(df)`. Note `load_data` is cached with `@lru_cache`.
- `scripts/download_data.sh` — downloader that saves files as `{season}_E0.csv` into `data/`.

Data expectations
-----------------

- CSVs must be named `{season}_E0.csv` (examples: `2526_E0.csv`, `2425_E0.csv`) and placed in `data/`.
- Expected CSV columns: `HomeTeam`, `AwayTeam`, `FTR`, `FTHG`, `FTAG`, `Date`.
- Many services operate over the most recent 10 season files (sorted reverse) — see `DATA_DIR = "data"` in `src/services.py`.

Club Logos
----------

The application displays club logos next to team names in the standings table:

- **Source**: Logos are sourced from https://football-logos.cc/england/
- **Storage**: Local files stored in `logos2/` directory
- **Coverage**: 40+ English football teams with multiple name variations
- **Display**: 24x24px with proper aspect ratios and responsive design
- **Fallback**: UI avatars for teams without local logos
- **Serving**: Flask route `/logos/<filename>` serves logo files

Team name variations are supported (e.g., "Manchester United", "Man United", "Man Utd") to ensure logos display correctly regardless of data format.

API examples
------------

- List seasons: `GET /api/seasons`
- Season stats: `GET /api/stats/2526`
- Team history: `GET /api/team-history/Arsenal`

Notes for contributors
----------------------

- If you change `load_data`, remember `@lru_cache` may cause stale reads during development — restart the server or clear the cache.
- Standings and sorting use points (3/win, 1/draw), then goal difference, then goals for. Keep these rules consistent when editing `get_standings_service` or `calculate_team_stats`.
- Dates are parsed with `pd.to_datetime(..., dayfirst=True)` in several services; be conservative when changing date handling.

Running locally
---------------

After installing dependencies and ensuring `data/` contains CSVs, run:

```bash
python3 src/app.py
```

Then open `http://localhost:5001` in your browser.

Need help?
----------
If anything in this README is unclear or you want runnable tests/CI examples added, open an issue or ask to expand the developer instructions in `.github/copilot-instructions.md`.

Container / Docker
------------------

Build and run the dev container (binds the Flask dev server to 0.0.0.0):

```bash
docker build -t epl-explorer:dev .
docker run --rm -p 5001:5001 -v "$(pwd)/data":/app/data:ro epl-explorer:dev
```

Or use Compose:

```bash
docker compose up --build
```

Notes:
- The container expects `data/` mounted at `/app/data`; use the `-v` flag or the Compose volume.
- `src/app.py` is configured to bind `0.0.0.0` so the dev server is reachable from the host.
- For production, prefer running `gunicorn` (the project has `gunicorn` in `requirements.txt`) and adjust the `Dockerfile` accordingly.

Production image
----------------

This repository includes `Dockerfile.prod` which runs the app with `gunicorn`.

Build and run the production image (mount `data/` at runtime):

```bash
docker build -f Dockerfile.prod -t epl-explorer:prod .
docker run --rm -p 5001:5001 -v "$(pwd)/data":/app/data:ro epl-explorer:prod
```

The `Dockerfile.prod` creates a non-root user and launches `gunicorn` bound to `0.0.0.0:5001`.
