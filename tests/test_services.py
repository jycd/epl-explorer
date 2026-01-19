import pytest
from unittest.mock import patch
from src.services import (
    get_season_stats_service,
    get_standings_service,
    get_head_to_head_service,
    get_available_seasons_service,
    get_team_history_service,
    get_team_win_rate_by_month_service,
    get_match_details_service
)

# Mock DATA_DIR in services to use our fixture
@pytest.fixture(autouse=True)
def mock_data_dir_path(mock_data_dir):
    with patch("src.services.DATA_DIR", mock_data_dir):
        yield

def test_get_season_stats_service_valid():
    stats = get_season_stats_service("2324")
    assert stats is not None
    assert len(stats) > 0
    
    # Check Man City stats (from fixture: 1 match, 1 win)
    mancity = next((s for s in stats if s['team'] == "Man City"), None)
    assert mancity is not None
    assert mancity['overall']['matches'] == 1
    assert mancity['overall']['wins'] == 1
    assert mancity['overall']['points'] == 3

def test_get_season_stats_service_invalid():
    stats = get_season_stats_service("9999")
    assert stats is None

def test_get_standings_service():
    standings = get_standings_service("2324")
    assert standings is not None
    assert len(standings) > 0
    
    # Check sorting (Man City should be high up with 3 points and +3 GD)
    # Newcastle also has 3 points and +4 GD, so Newcastle should be 1st, Man City 2nd (or close)
    first_place = standings[0]
    assert first_place['team'] == "Newcastle"
    assert first_place['points'] == 3
    assert first_place['goal_difference'] == 4

def test_get_head_to_head_service():
    h2h = get_head_to_head_service("2324")
    assert h2h is not None
    
    # Check Burnley vs Man City
    burnley_vs_city = h2h['Burnley']['Man City']
    assert burnley_vs_city['matches'] == 1
    assert burnley_vs_city['wins'] == 0
    assert burnley_vs_city['losses'] == 1

def test_get_available_seasons_service():
    seasons = get_available_seasons_service()
    assert "2324" in seasons
    assert "2223" in seasons
    assert len(seasons) == 2

def test_get_team_history_service():
    history = get_team_history_service("Arsenal")
    assert len(history) == 2 # Played in both 2324 and 2223 in fixture
    
    # Check 2324 season
    season_2324 = next((h for h in history if h['season'] == "2324"), None)
    assert season_2324 is not None
    assert season_2324['matches'] == 1
    assert season_2324['wins'] == 1

def test_get_team_win_rate_by_month_service():
    # Arsenal played in August in both seasons in fixture
    monthly_stats = get_team_win_rate_by_month_service("Arsenal")
    august_stats = next((m for m in monthly_stats if m['month'] == "August"), None)
    
    assert august_stats is not None
    assert august_stats['matches'] == 2 # One in 2324, one in 2223
    assert august_stats['wins'] == 2 # Won both

def test_get_match_details_service():
    matches = get_match_details_service("Burnley", "Man City")
    assert len(matches) == 1
    
    match = matches[0]
    assert match['home_team'] == "Burnley"
    assert match['away_team'] == "Man City"
    assert match['fthg'] == 0
    assert match['ftag'] == 3
