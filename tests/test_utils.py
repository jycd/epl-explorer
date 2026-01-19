import pytest
import pandas as pd
from src.utils import load_data, calculate_team_stats

def test_load_data_valid(mock_data_dir):
    """Test loading data for a valid season."""
    df = load_data("2324", data_dir=mock_data_dir)
    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "HomeTeam" in df.columns
    assert "AwayTeam" in df.columns

def test_load_data_invalid(mock_data_dir):
    """Test loading data for an invalid season."""
    df = load_data("9999", data_dir=mock_data_dir)
    assert df is None

def test_calculate_team_stats_basic():
    """Test calculating stats for a simple dataframe."""
    data = {
        'HomeTeam': ['TeamA', 'TeamB'],
        'AwayTeam': ['TeamB', 'TeamA'],
        'FTHG': [2, 1],
        'FTAG': [1, 1],
        'FTR': ['H', 'D']
    }
    df = pd.DataFrame(data)
    
    stats = calculate_team_stats(df)
    assert len(stats) == 2
    
    # Team A: 1 Home Win (2-1), 1 Away Draw (1-1) -> 4 points
    team_a = next(s for s in stats if s['team'] == 'TeamA')
    assert team_a['overall']['matches'] == 2
    assert team_a['overall']['wins'] == 1
    assert team_a['overall']['draws'] == 1
    assert team_a['overall']['losses'] == 0
    assert team_a['overall']['points'] == 4
    assert team_a['overall']['goals_for'] == 3 # 2 home + 1 away
    assert team_a['overall']['goals_against'] == 2 # 1 home + 1 away
    
    # Team B: 1 Away Loss (1-2), 1 Home Draw (1-1) -> 1 point
    team_b = next(s for s in stats if s['team'] == 'TeamB')
    assert team_b['overall']['matches'] == 2
    assert team_b['overall']['wins'] == 0
    assert team_b['overall']['draws'] == 1
    assert team_b['overall']['losses'] == 1
    assert team_b['overall']['points'] == 1

def test_calculate_team_stats_empty():
    """Test calculating stats for an empty dataframe."""
    df = pd.DataFrame(columns=['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR'])
    stats = calculate_team_stats(df)
    assert stats == []

def test_calculate_team_stats_sorting():
    """Test that stats are sorted by win rate."""
    data = {
        'HomeTeam': ['TeamA', 'TeamB'],
        'AwayTeam': ['TeamC', 'TeamC'],
        'FTHG': [1, 1],
        'FTAG': [0, 0],
        'FTR': ['H', 'H']
    }
    # Team A: 1 win / 1 match = 100%
    # Team B: 1 win / 1 match = 100%
    # Team C: 0 wins / 2 matches = 0%
    df = pd.DataFrame(data)
    
    stats = calculate_team_stats(df)
    assert len(stats) == 3
    assert stats[0]['overall']['win_rate'] >= stats[1]['overall']['win_rate']
    assert stats[-1]['team'] == 'TeamC'
