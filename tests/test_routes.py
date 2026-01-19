import pytest
from unittest.mock import patch
from src.app import app

@pytest.fixture
def client(mock_data_dir):
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    
    # Patch DATA_DIR in services to use our fixture
    with patch("src.services.DATA_DIR", mock_data_dir):
        with app.test_client() as client:
            yield client

def test_get_season_stats_route(client):
    response = client.get('/api/stats/2324')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]['team'] is not None

def test_get_season_stats_route_invalid(client):
    response = client.get('/api/stats/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_get_season_standings_route(client):
    response = client.get('/api/standings/2324')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'position' in data[0]

def test_get_head_to_head_route(client):
    response = client.get('/api/head-to-head/2324')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'Burnley' in data

def test_get_seasons_route(client):
    response = client.get('/api/seasons')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert "2324" in data

def test_get_team_history_route(client):
    response = client.get('/api/team-history/Arsenal')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_team_win_rate_by_month_route(client):
    response = client.get('/api/team-win-rate-by-month/Arsenal')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    
    # Test with season filter
    response_filtered = client.get('/api/team-win-rate-by-month/Arsenal?season=2324')
    assert response_filtered.status_code == 200
    data_filtered = response_filtered.get_json()
    assert isinstance(data_filtered, list)

def test_get_all_teams_route(client):
    response = client.get('/api/teams')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert "Arsenal" in data

def test_get_match_details_route(client):
    response = client.get('/api/match-details/Burnley/Man City')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['home_team'] == "Burnley"
