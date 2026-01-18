import os
import pandas as pd
from functools import lru_cache

@lru_cache(maxsize=32)
def load_data(season, data_dir="data"):
    """Load data for a specific season."""
    # Season format expected: "2526", "2425", etc.
    file_path = os.path.join(data_dir, f"{season}_E0.csv")
    if not os.path.exists(file_path):
        return None
    
    try:
        df = pd.read_csv(file_path)
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')
        
    # Filter out empty rows
    df = df.dropna(subset=['HomeTeam', 'AwayTeam', 'FTR'])
    
    # Strip whitespace from team names
    df['HomeTeam'] = df['HomeTeam'].str.strip()
    df['AwayTeam'] = df['AwayTeam'].str.strip()
    
    return df

def calculate_team_stats(df):
    """Calculate stats for all teams in the dataframe."""
    # Create a list to store team stats
    stats = []
    
    # Get all unique teams
    teams = set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique())
    
    # Pre-calculate home and away aggregations
    home_stats = df.groupby('HomeTeam').agg(
        matches=('FTR', 'count'),
        wins=('FTR', lambda x: (x == 'H').sum()),
        draws=('FTR', lambda x: (x == 'D').sum()),
        losses=('FTR', lambda x: (x == 'A').sum()),
        goals_for=('FTHG', 'sum'),
        goals_against=('FTAG', 'sum')
    )
    
    away_stats = df.groupby('AwayTeam').agg(
        matches=('FTR', 'count'),
        wins=('FTR', lambda x: (x == 'A').sum()),
        draws=('FTR', lambda x: (x == 'D').sum()),
        losses=('FTR', lambda x: (x == 'H').sum()),
        goals_for=('FTAG', 'sum'),
        goals_against=('FTHG', 'sum')
    )
    
    for team in teams:
        # Get home stats (handle missing if team played no home games)
        h = home_stats.loc[team] if team in home_stats.index else pd.Series(0, index=home_stats.columns)
        # Get away stats (handle missing if team played no away games)
        a = away_stats.loc[team] if team in away_stats.index else pd.Series(0, index=away_stats.columns)
        
        # Helper for rate calculation
        def calc_rate(count, total):
            return round((count / total) * 100, 2) if total > 0 else 0
            
        # Calculate totals
        total_matches = h['matches'] + a['matches']
        total_wins = h['wins'] + a['wins']
        total_draws = h['draws'] + a['draws']
        total_losses = h['losses'] + a['losses']
        total_goals_for = h['goals_for'] + a['goals_for']
        total_goals_against = h['goals_against'] + a['goals_against']
        goal_difference = total_goals_for - total_goals_against
        points = (total_wins * 3) + (total_draws * 1)
        
        stats.append({
            "team": team,
            "home": {
                "matches": int(h['matches']),
                "wins": int(h['wins']),
                "draws": int(h['draws']),
                "losses": int(h['losses']),
                "win_rate": calc_rate(h['wins'], h['matches']),
                "draw_rate": calc_rate(h['draws'], h['matches']),
                "loss_rate": calc_rate(h['losses'], h['matches']),
                "goals_for": int(h['goals_for']),
                "goals_against": int(h['goals_against'])
            },
            "away": {
                "matches": int(a['matches']),
                "wins": int(a['wins']),
                "draws": int(a['draws']),
                "losses": int(a['losses']),
                "win_rate": calc_rate(a['wins'], a['matches']),
                "draw_rate": calc_rate(a['draws'], a['matches']),
                "loss_rate": calc_rate(a['losses'], a['matches']),
                "goals_for": int(a['goals_for']),
                "goals_against": int(a['goals_against'])
            },
            "overall": {
                "matches": int(total_matches),
                "wins": int(total_wins),
                "draws": int(total_draws),
                "losses": int(total_losses),
                "win_rate": calc_rate(total_wins, total_matches),
                "draw_rate": calc_rate(total_draws, total_matches),
                "loss_rate": calc_rate(total_losses, total_matches),
                "goals_for": int(total_goals_for),
                "goals_against": int(total_goals_against),
                "goal_difference": int(goal_difference),
                "points": int(points)
            }
        })
    
    # Sort by overall win rate descending
    stats.sort(key=lambda x: x['overall']['win_rate'], reverse=True)
    return stats
