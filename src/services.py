import glob
import os
import pandas as pd
from src.utils import load_data, calculate_team_stats

DATA_DIR = "data"

def get_season_stats_service(season):
    df = load_data(season, DATA_DIR)
    if df is None:
        return None
    return calculate_team_stats(df)

def get_standings_service(season):
    df = load_data(season, DATA_DIR)
    if df is None:
        return None
    
    stats = calculate_team_stats(df)
    # Sort by points (descending), then goal difference (descending), then goals for (descending)
    stats.sort(key=lambda x: (x['overall']['points'], x['overall']['goal_difference'], x['overall']['goals_for']), reverse=True)
    
    standings = []
    for i, team_stat in enumerate(stats, 1):
        standings.append({
            "position": i,
            "team": team_stat['team'],
            "played": team_stat['overall']['matches'],
            "won": team_stat['overall']['wins'],
            "drawn": team_stat['overall']['draws'],
            "lost": team_stat['overall']['losses'],
            "goals_for": team_stat['overall']['goals_for'],
            "goals_against": team_stat['overall']['goals_against'],
            "goal_difference": team_stat['overall']['goal_difference'],
            "points": team_stat['overall']['points']
        })
    return standings

def get_head_to_head_service(season):
    df = load_data(season, DATA_DIR)
    if df is None:
        return None

    teams = sorted(list(set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique())))
    stats = {}

    for team_a in teams:
        stats[team_a] = {}
        for team_b in teams:
            if team_a == team_b:
                continue
            
            # Matches where Team A is Home and Team B is Away
            home_matches = df[(df['HomeTeam'] == team_a) & (df['AwayTeam'] == team_b)]
            # Matches where Team A is Away and Team B is Home
            away_matches = df[(df['HomeTeam'] == team_b) & (df['AwayTeam'] == team_a)]
            
            wins = 0
            draws = 0
            losses = 0
            
            # Check home matches for Team A
            wins += len(home_matches[home_matches['FTR'] == 'H'])
            draws += len(home_matches[home_matches['FTR'] == 'D'])
            losses += len(home_matches[home_matches['FTR'] == 'A'])
            
            # Check away matches for Team A
            wins += len(away_matches[away_matches['FTR'] == 'A'])
            draws += len(away_matches[away_matches['FTR'] == 'D'])
            losses += len(away_matches[away_matches['FTR'] == 'H'])
            
            total = wins + draws + losses
            win_rate = round((wins / total) * 100, 2) if total > 0 else 0.0
            
            stats[team_a][team_b] = {
                "matches": total,
                "wins": wins,
                "draws": draws,
                "losses": losses,
                "win_rate": win_rate
            }
    return stats

def get_available_seasons_service():
    files = glob.glob(os.path.join(DATA_DIR, "*_E0.csv"))
    seasons = [os.path.basename(f).split('_')[0] for f in files]
    return sorted(seasons, reverse=True)

def get_team_history_service(team_name):
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*_E0.csv")), reverse=True)
    recent_files = files[:10]
    
    history = []
    
    for f in recent_files:
        season = os.path.basename(f).split('_')[0]
        df = load_data(season, DATA_DIR)
        
        if df is None:
            continue
            
        if team_name not in df['HomeTeam'].values and team_name not in df['AwayTeam'].values:
            continue
            
        all_stats = calculate_team_stats(df)
        team_stats = next((s for s in all_stats if s['team'] == team_name), None)
        
        if team_stats:
            history.append({
                "season": season,
                "matches": team_stats['overall']['matches'],
                "wins": team_stats['overall']['wins'],
                "draws": team_stats['overall']['draws'],
                "losses": team_stats['overall']['losses'],
                "win_rate": team_stats['overall']['win_rate'],
                "draw_rate": team_stats['overall']['draw_rate'],
                "loss_rate": team_stats['overall']['loss_rate'],
                "goals_for": team_stats['overall']['goals_for'],
                "goals_against": team_stats['overall']['goals_against'],
                "goal_difference": team_stats['overall']['goal_difference']
            })
    return history

def get_team_goal_diff_service(team_name):
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*_E0.csv")), reverse=True)
    recent_files = files[:10]
    
    history = []
    
    for f in recent_files:
        season = os.path.basename(f).split('_')[0]
        df = load_data(season, DATA_DIR)
        
        if df is None:
            continue
            
        if team_name not in df['HomeTeam'].values and team_name not in df['AwayTeam'].values:
            # If the team didn't play this season, we can either skip or add a 0 entry.
            # For now, let's skip to maintain the "history" aspect, but the user might expect 0.
            # However, the issue reported is "no data", which implies the team WAS there but not found.
            # Let's check if the team name matches exactly.
            continue
            
        all_stats = calculate_team_stats(df)
        team_stats = next((s for s in all_stats if s['team'] == team_name), None)
        
        if team_stats:
            history.append({
                "season": season,
                "goal_difference": team_stats['overall']['goal_difference'],
                "goals_for": team_stats['overall']['goals_for'],
                "goals_against": team_stats['overall']['goals_against']
            })
    return history

def get_team_win_rate_by_month_service(team_name, season=None):
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*_E0.csv")), reverse=True)
    recent_files = files[:10]
    
    monthly_stats = {}
    
    for f in recent_files:
        file_season = os.path.basename(f).split('_')[0]
        
        # If a specific season is requested, skip others
        if season and file_season != season:
            continue
            
        df = load_data(file_season, DATA_DIR)
        
        if df is None:
            continue
            
        team_matches = df[(df['HomeTeam'] == team_name) | (df['AwayTeam'] == team_name)].copy()
        
        if team_matches.empty:
            continue
            
        try:
            team_matches['Date'] = pd.to_datetime(team_matches['Date'], dayfirst=True)
        except Exception:
            continue
            
        for _, match in team_matches.iterrows():
            month_name = match['Date'].strftime('%B')
            
            if month_name not in monthly_stats:
                monthly_stats[month_name] = {"wins": 0, "total": 0}
                
            monthly_stats[month_name]["total"] += 1
            
            if match['HomeTeam'] == team_name:
                if match['FTR'] == 'H':
                    monthly_stats[month_name]["wins"] += 1
            else:
                if match['FTR'] == 'A':
                    monthly_stats[month_name]["wins"] += 1
                    
    results = []
    months_order = ['August', 'September', 'October', 'November', 'December', 'January', 'February', 'March', 'April', 'May', 'June', 'July']
    
    for month in months_order:
        if month in monthly_stats:
            stats = monthly_stats[month]
            win_rate = round((stats["wins"] / stats["total"]) * 100, 2) if stats["total"] > 0 else 0.0
            results.append({
                "month": month,
                "win_rate": win_rate,
                "matches": stats["total"],
                "wins": stats["wins"]
            })
    return results

def get_all_teams_service():
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*_E0.csv")), reverse=True)
    recent_files = files[:10]
    
    team_seasons = {}
    
    for f in recent_files:
        season = os.path.basename(f).split('_')[0]
        df = load_data(season, DATA_DIR)
        
        if df is None:
            continue
            
        teams = set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique())
        
        for team in teams:
            if team not in team_seasons:
                team_seasons[team] = 0
            team_seasons[team] += 1
            
    # Filter teams that have played in all 10 seasons (or however many files we found)
    # If we have fewer than 10 files, we just check if they played in all available files
    num_seasons = len(recent_files)
    consistent_teams = [team for team, count in team_seasons.items() if count == num_seasons]
    
    return sorted(consistent_teams)

def get_team_win_rate_against_others_service(team_name):
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*_E0.csv")), reverse=True)
    recent_files = files[:10]
    
    opponent_stats = {}
    
    for f in recent_files:
        season = os.path.basename(f).split('_')[0]
        df = load_data(season, DATA_DIR)
        
        if df is None:
            continue
            
        # Filter matches involving the team
        team_matches = df[(df['HomeTeam'] == team_name) | (df['AwayTeam'] == team_name)].copy()
        
        if team_matches.empty:
            continue
            
        for _, match in team_matches.iterrows():
            if match['HomeTeam'] == team_name:
                opponent = match['AwayTeam']
                is_win = match['FTR'] == 'H'
            else:
                opponent = match['HomeTeam']
                is_win = match['FTR'] == 'A'
                
            if opponent not in opponent_stats:
                opponent_stats[opponent] = {"wins": 0, "total": 0}
                
            opponent_stats[opponent]["total"] += 1
            if is_win:
                opponent_stats[opponent]["wins"] += 1
                
    results = []
    
    # First try with threshold of 10 matches
    threshold = 10
    qualified_opponents = [opp for opp, s in opponent_stats.items() if s["total"] >= threshold]
    
    # If fewer than 10 opponents meet the condition, lower threshold to 5
    if len(qualified_opponents) < 10:
        threshold = 5
        
    for opponent, stats in opponent_stats.items():
        if stats["total"] < threshold:
            continue
            
        win_rate = round((stats["wins"] / stats["total"]) * 100, 2) if stats["total"] > 0 else 0.0
        results.append({
            "opponent": opponent,
            "win_rate": win_rate,
            "matches": stats["total"],
            "wins": stats["wins"]
        })
        
    # Sort by win rate descending, then by total matches descending
    results.sort(key=lambda x: (x['win_rate'], x['matches']), reverse=True)
    return results

def get_match_details_service(team_name, opponent_name):
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*_E0.csv")), reverse=True)
    recent_files = files[:10]
    
    matches = []
    
    for f in recent_files:
        season = os.path.basename(f).split('_')[0]
        df = load_data(season, DATA_DIR)
        
        if df is None:
            continue
            
        # Filter matches between team and opponent
        relevant_matches = df[
            ((df['HomeTeam'] == team_name) & (df['AwayTeam'] == opponent_name)) |
            ((df['HomeTeam'] == opponent_name) & (df['AwayTeam'] == team_name))
        ].copy()
        
        if relevant_matches.empty:
            continue
            
        try:
            relevant_matches['Date'] = pd.to_datetime(relevant_matches['Date'], dayfirst=True)
        except Exception:
            pass
            
        for _, match in relevant_matches.iterrows():
            matches.append({
                "season": season,
                "date": match['Date'].strftime('%Y-%m-%d') if isinstance(match['Date'], pd.Timestamp) else match['Date'],
                "home_team": match['HomeTeam'],
                "away_team": match['AwayTeam'],
                "fthg": int(match['FTHG']),
                "ftag": int(match['FTAG']),
                "ftr": match['FTR']
            })
            
    # Sort by date descending
    matches.sort(key=lambda x: x['date'], reverse=True)
    return matches

def get_team_standing_history_service(team_name):
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*_E0.csv")), reverse=True)
    recent_files = files[:10]
    
    history = []
    
    for f in recent_files:
        season = os.path.basename(f).split('_')[0]
        df = load_data(season, DATA_DIR)
        
        if df is None:
            continue
            
        if team_name not in df['HomeTeam'].values and team_name not in df['AwayTeam'].values:
            continue
            
        stats = calculate_team_stats(df)
        # Sort by points (descending), then goal difference (descending), then goals for (descending)
        stats.sort(key=lambda x: (x['overall']['points'], x['overall']['goal_difference'], x['overall']['goals_for']), reverse=True)
        
        position = next((i for i, s in enumerate(stats, 1) if s['team'] == team_name), None)
        
        if position:
            # Get full standings for tooltip
            full_standings = []
            for i, s in enumerate(stats, 1):
                full_standings.append(f"{i}. {s['team']}")
            
            history.append({
                "season": season,
                "position": position,
                "full_standings": full_standings
            })
            
    return history
