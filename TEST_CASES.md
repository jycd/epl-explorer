# EPL Application Test Cases

This document outlines the test cases for the English Premier League (EPL) data analysis application. The application is built using Flask and Pandas.

## Table of Contents
1. [Unit Tests - Utils](#unit-tests---utils)
2. [Integration Tests - Services](#integration-tests---services)
3. [Functional Tests - API Routes](#functional-tests---api-routes)
4. [UI Test Cases](#ui-test-cases)

---

## Unit Tests - Utils

### `src/utils.py`

#### `load_data(season, data_dir)`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| UT-UTILS-001 | Load valid season data | `season="2324"`, valid `data_dir` | Returns a non-empty Pandas DataFrame with expected columns (HomeTeam, AwayTeam, FTR, etc.). |
| UT-UTILS-002 | Load non-existent season | `season="9999"`, valid `data_dir` | Returns `None`. |
| UT-UTILS-003 | Load data with encoding issues | Season file with Latin1 characters | Returns DataFrame with correctly decoded characters. |
| UT-UTILS-004 | Data cleaning - Empty rows | CSV with empty rows | Returns DataFrame with empty rows removed (subset HomeTeam, AwayTeam, FTR). |
| UT-UTILS-005 | Data cleaning - Whitespace | CSV with whitespace in team names | Returns DataFrame with whitespace stripped from 'HomeTeam' and 'AwayTeam'. |

#### `calculate_team_stats(df)`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| UT-UTILS-006 | Calculate stats for standard match results | DataFrame with known match results (e.g., Team A wins home, Team B wins away) | Returns list of dictionaries with correct wins, losses, draws, goals, and points for each team. |
| UT-UTILS-007 | Calculate stats with no matches | Empty DataFrame | Returns empty list. |
| UT-UTILS-008 | Verify points calculation | DataFrame where Team A has 1 Win, 1 Draw, 1 Loss | Team A points = 4 (3+1+0). |
| UT-UTILS-009 | Verify goal difference | DataFrame where Team A scored 5, conceded 3 | Goal difference = +2. |
| UT-UTILS-010 | Verify sorting | DataFrame with multiple teams | Result list is sorted by overall win rate descending. |

---

## Integration Tests - Services

### `src/services.py`

#### `get_season_stats_service(season)`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| IT-SERV-001 | Get stats for valid season | `season="2324"` | Returns list of team stats objects. |
| IT-SERV-002 | Get stats for invalid season | `season="invalid"` | Returns `None`. |

#### `get_standings_service(season)`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| IT-SERV-003 | Get standings for valid season | `season="2324"` | Returns list of team objects sorted by Points > Goal Diff > Goals For. |
| IT-SERV-004 | Verify position assignment | `season="2324"` | Each object has a correct sequential `position` field (1, 2, 3...). |

#### `get_head_to_head_service(season)`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| IT-SERV-005 | Get H2H stats | `season="2324"` | Returns nested dictionary `stats[team_a][team_b]` with match counts and win rates. |
| IT-SERV-006 | Verify self-match exclusion | `season="2324"` | `stats[team_a]` does not contain `team_a`. |

#### `get_available_seasons_service()`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| IT-SERV-007 | List available seasons | None | Returns list of season strings (e.g., ["2425", "2324", ...]) sorted descending. |

#### `get_team_history_service(team_name)`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| IT-SERV-008 | Get history for existing team | `team_name="Arsenal"` | Returns list of stats per season where the team played. |
| IT-SERV-009 | Get history for non-existent team | `team_name="FakeTeam"` | Returns empty list. |

#### `get_team_win_rate_by_month_service(team_name, season)`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| IT-SERV-010 | Win rate by month (all time) | `team_name="Liverpool"`, `season=None` | Returns list of monthly stats aggregated across all available recent seasons. |
| IT-SERV-011 | Win rate by month (specific season) | `team_name="Liverpool"`, `season="2324"` | Returns list of monthly stats for that specific season only. |

#### `get_match_details_service(team_name, opponent_name)`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| IT-SERV-012 | Get match details | `team_name="Chelsea"`, `opponent_name="Man United"` | Returns list of matches between the two teams, sorted by date descending. |

---

## Functional Tests - API Routes

### `src/routes.py`

#### `GET /api/stats/<season>`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| FT-API-001 | Get stats for valid season | `GET /api/stats/2324` | HTTP 200, JSON body with list of team stats. |
| FT-API-002 | Get stats for invalid season | `GET /api/stats/9999` | HTTP 404, JSON body `{"error": "Season not found"}`. |

#### `GET /api/standings/<season>`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| FT-API-003 | Get standings | `GET /api/standings/2324` | HTTP 200, JSON body with standings list. |

#### `GET /api/seasons`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| FT-API-004 | Get all seasons | `GET /api/seasons` | HTTP 200, JSON list of season strings. |

#### `GET /api/team-history/<team_name>`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| FT-API-005 | Get team history | `GET /api/team-history/Man City` | HTTP 200, JSON list of historical stats. |

#### `GET /api/team-win-rate-by-month/<team_name>`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| FT-API-006 | Get monthly win rate | `GET /api/team-win-rate-by-month/Liverpool` | HTTP 200, JSON list of monthly win rates. |
| FT-API-007 | Get monthly win rate with season filter | `GET /api/team-win-rate-by-month/Liverpool?season=2324` | HTTP 200, JSON list filtered by season. |

#### `GET /api/match-details/<team_name>/<opponent_name>`
| Test Case ID | Description | Input | Expected Output |
|--------------|-------------|-------|-----------------|
| FT-API-008 | Get match details | `GET /api/match-details/Arsenal/Tottenham` | HTTP 200, JSON list of match details. |

---

## UI Test Cases

### Standings Page (`/`)

| Test Case ID | Description | Pre-conditions | Steps | Expected Result |
|--------------|-------------|----------------|-------|-----------------|
| UI-STD-001 | Load Standings Page | Application running | 1. Navigate to `/` | Page loads with title "EPL Season Standings". Season dropdown is populated. Default season standings are displayed. |
| UI-STD-002 | Change Season | Page loaded | 1. Select a different season from dropdown<br>2. Click "Get Standings" | Table updates to show standings for the selected season. |
| UI-STD-003 | Sort Table | Standings displayed | 1. Click on "Points" header | Table sorts by Points (descending/ascending toggle). Sort icon updates. |
| UI-STD-004 | Navigate to Team Detail | Standings displayed | 1. Click on a team name (e.g., "Arsenal") | Redirects to `/team-detail?team=Arsenal`. |
| UI-STD-005 | Verify Row Colors | Standings displayed | 1. Observe top 4 rows<br>2. Observe 5th row<br>3. Observe bottom 3 rows | Top 4 are green (UCL). 5th is yellow (UEL). Bottom 3 are red (Relegation). |

### Team History Page (`/team-history`)

| Test Case ID | Description | Pre-conditions | Steps | Expected Result |
|--------------|-------------|----------------|-------|-----------------|
| UI-HIST-001 | Load History Page | Application running | 1. Navigate to `/team-history` | Page loads with title "Team History". Team dropdown is populated. |
| UI-HIST-002 | View Team Charts | Page loaded | 1. Select "Liverpool" from dropdown<br>2. Click "Show Chart" | Three charts appear: League Standing, Win/Draw/Loss Rate, and Goal Difference. |
| UI-HIST-003 | Chart Interaction | Charts displayed | 1. Hover over a data point on the Win Rate chart | Tooltip displays detailed stats (e.g., "Wins: 20"). |
| UI-HIST-004 | No Data Handling | Page loaded | 1. Select a team with no history (if any)<br>2. Click "Show Chart" | Error message "No data found for this team" is displayed. |

### Team Detail Page (`/team-detail`)

| Test Case ID | Description | Pre-conditions | Steps | Expected Result |
|--------------|-------------|----------------|-------|-----------------|
| UI-DET-001 | Load Detail Page | Application running | 1. Navigate to `/team-detail?team=Chelsea` | Page loads with title "Chelsea - Team Details". Opponent Win Rate chart and Monthly Win Rate chart are displayed. |
| UI-DET-002 | Filter Monthly Stats | Page loaded | 1. Select a specific season from dropdown | Monthly Win Rate chart updates to show data only for that season. |
| UI-DET-003 | Navigate to Match Details | Opponent chart displayed | 1. Click on a bar in the Opponent Win Rate chart (e.g., "Man United") | Redirects to `/match-details?team=Chelsea&opponent=Man United`. |
| UI-DET-004 | Missing Team Parameter | Application running | 1. Navigate to `/team-detail` (no param) | Error message "No team specified" is displayed. |

### Match Details Page (`/match-details`)

| Test Case ID | Description | Pre-conditions | Steps | Expected Result |
|--------------|-------------|----------------|-------|-----------------|
| UI-MATCH-001 | Load Match Details | Application running | 1. Navigate to `/match-details?team=Arsenal&opponent=Tottenham` | Page loads with title "Matches: Arsenal vs Tottenham". Table lists all matches with Date, Score, and Result. |
| UI-MATCH-002 | Verify Result Coloring | Matches displayed | 1. Observe "Result" column | Wins are green, Draws are orange, Losses are red. |
| UI-MATCH-003 | Back Navigation | Page loaded | 1. Click "Back to Team Detail" | Redirects back to `/team-detail?team=Arsenal`. |

