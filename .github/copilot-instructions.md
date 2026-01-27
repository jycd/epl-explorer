# Copilot / AI agent instructions for the EPL explorer

Purpose: help AI coding assistants be immediately productive in this repository.

## Quick Start
- **Run app (dev):** The app is a Flask server with modern UI. Run with:
  ```bash
  python3 src/app.py
  ```
  It listens on port `5001` and registers the API blueprint in `src/routes.py`.

## Architecture Overview

### Backend (Flask)
- `src/app.py` - Flask app setup, template routes, and URL parameter handling
- `src/routes.py` - API blueprint at `/api` with all JSON endpoints
- `src/services.py` - Business logic, CSV processing, and data calculations
- `src/utils.py` - Data loading (`load_data`) and core calculations (`calculate_team_stats`) with `@lru_cache`

### Frontend (Modern UI)
- `src/static/css/` - CSS architecture with variables and modular stylesheets
  - `common.css` - Global styles, CSS variables, and common components
  - `home-page.css` - Standings page specific styles
  - `team-detail.css` - Team detail page styles
  - `match-details.css` - Match details page styles
  - `team-history.css` - Team history page styles
  - `average-stats.css` - Average stats page styles
- `src/static/js/` - JavaScript for interactive features
  - `team-history.js` - Team history chart interactions
  - `average-stats-page.js` - Average stats page functionality
- `src/templates/` - HTML templates with modern responsive design

## Key Features & Pages

### 1. Season Standings (`/`)
- Interactive standings table with sorting
- Form indicators (W/D/L) for recent matches
- Competition qualification colors (UCL, UEL, Relegation)
- Team search and filtering
- URL parameter persistence for selections

### 2. Team History (`/team-history`)
- Win/Draw/Loss rate history charts with improved colors
- Goal difference charts
- Interactive tooltips showing all three rates
- Season selection with URL persistence

### 3. Team Detail (`/team-detail`)
- Win rate against opponents (bar chart)
- Win rate by month (pie chart)
- Clickable opponent bars for match details
- Season filtering for monthly data

### 4. Match Details (`/match-details`)
- Head-to-head match history
- Team vs opponent analysis
- Responsive card-based layout

### 5. Average Stats (`/average-stats`)
- League-wide average statistics
- Persistent URL parameters
- Modern chart visualizations

## CSS Architecture & Variables

### Color System (defined in `common.css`)
```css
/* Match Result Colors */
--win-bg: #d1e7dd; --win-text: #0f5132;
--draw-bg: #64748b; --draw-text: #ffffff;
--loss-bg: #f8d7da; --loss-text: #721c24;

/* Chart Colors */
--chart-green: #22c55e; --chart-yellow: #fbbf24;
--chart-red: #f87171; --chart-purple: #667eea;

/* Competition Colors */
--ucl-bg: rgba(16, 185, 129, 0.1);
--uel-bg: rgba(59, 130, 246, 0.1);
--rel-bg: rgba(239, 68, 68, 0.1);
```

### Design Principles
- **Responsive Design**: Mobile-first approach with breakpoints
- **Modern UI**: Clean, card-based layouts with subtle shadows
- **Consistent Theming**: Centralized color variables
- **Accessibility**: Proper contrast ratios and semantic HTML

## Data Model & Conventions

### CSV Files
- Location: `data/` directory
- Naming: `{season}_E0.csv` (e.g., `2526_E0.csv`)
- Required columns: `HomeTeam`, `AwayTeam`, `FTR`, `FTHG`, `FTAG`, `Date`
- Downloader: `scripts/download_data.sh`

### Data Processing
- `load_data(season, data_dir)` returns pandas DataFrame with whitespace trimming
- Most services operate on last 10 season files (reverse sorted)
- `@lru_cache` used for performance - clear cache when modifying data loading

## API Endpoints

### Core Endpoints
- `GET /api/seasons` - List available seasons
- `GET /api/stats/<season>` - Season statistics
- `GET /api/standings/<season>` - League standings
- `GET /api/team-history/<team>` - Team historical data
- `GET /api/team-win-rate-against-others/<team>` - Opponent win rates
- `GET /api/team-win-rate-by-month/<team>` - Monthly win rates
- `GET /api/match-details/<team>/<opponent>` - Head-to-head matches
- `GET /api/average-stats/<season>` - League averages

### URL Parameter Persistence
All pages support URL parameters to maintain state:
- Season selection: `?season=2526`
- Team selection: `?team=Arsenal`
- Multiple parameters: `?season=2526&team=Arsenal&includeRecent=true`

## Development Guidelines

### When Adding New Features
1. **Backend**: Add route in `routes.py`, implement logic in `services.py`
2. **Frontend**: Create/update CSS in `src/static/css/`, add JS if needed
3. **Templates**: Update appropriate HTML template in `src/templates/`
4. **URL Persistence**: Add parameter handling in `app.py` template routes

### CSS Guidelines
- **Use CSS variables** from `common.css` for colors
- **Follow mobile-first responsive design**
- **Use semantic HTML5 elements**
- **Maintain consistent spacing and typography**

### Chart.js Integration
- **Colors**: Use direct color codes (not CSS variables) in Chart.js configs
- **Tooltips**: Configure for consistent styling across charts
- **Responsiveness**: Set `maintainAspectRatio: false` for proper container sizing

### Common Pitfalls to Avoid
- **Chart.js Colors**: CSS variables don't work in Chart.js - use direct hex codes
- **Cache Issues**: Clear `@lru_cache` when modifying data loading logic
- **Date Handling**: Use `pd.to_datetime(..., dayfirst=True)` consistently
- **URL Parameters**: Ensure proper encoding for team names with spaces

## Files to Inspect When Debugging

### Backend Issues
- `src/services.py` - Business logic and data processing
- `src/utils.py` - CSV parsing and core calculations
- `src/routes.py` - API endpoint definitions

### Frontend Issues
- `src/static/css/common.css` - Global styles and variables
- `src/templates/` - HTML templates and structure
- `src/static/js/` - Interactive JavaScript functionality

### Data Issues
- `data/` directory - CSV file format and naming
- `scripts/download_data.sh` - Data acquisition process

## Dependencies
- **Backend**: `flask`, `pandas`, `gunicorn` (production)
- **Frontend**: Chart.js (via CDN), modern CSS features
- **Development**: Python 3.8+, modern browser

## Production Deployment
- Use `Dockerfile.prod` for production builds
- Run with `gunicorn` instead of Flask dev server
- Mount `data/` directory at runtime
- Configure proper environment variables

If anything above is unclear or you want additional examples (tests, CI, or specific feature implementation), tell me which area to expand.