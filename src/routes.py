from flask import Blueprint, jsonify
from src.services import (
    get_season_stats_service,
    get_standings_service,
    get_head_to_head_service,
    get_available_seasons_service,
    get_team_history_service,
    get_team_goal_diff_service,
    get_team_win_rate_by_month_service,
    get_all_teams_service,
    get_team_win_rate_against_others_service,
    get_team_standing_history_service
)

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/stats/<season>', methods=['GET'])
def get_season_stats(season):
    stats = get_season_stats_service(season)
    if stats is None:
        return jsonify({"error": "Season not found"}), 404
    return jsonify(stats)

@api_bp.route('/standings/<season>', methods=['GET'])
def get_season_standings(season):
    standings = get_standings_service(season)
    if standings is None:
        return jsonify({"error": "Season not found"}), 404
    return jsonify(standings)

@api_bp.route('/head-to-head/<season>', methods=['GET'])
def get_head_to_head_stats(season):
    stats = get_head_to_head_service(season)
    if stats is None:
        return jsonify({"error": "Season not found"}), 404
    return jsonify(stats)

@api_bp.route('/seasons', methods=['GET'])
def get_seasons():
    seasons = get_available_seasons_service()
    return jsonify(seasons)

@api_bp.route('/team-history/<team_name>', methods=['GET'])
def get_team_history(team_name):
    history = get_team_history_service(team_name)
    return jsonify(history)

@api_bp.route('/team-goal-diff/<team_name>', methods=['GET'])
def get_team_goal_diff(team_name):
    history = get_team_goal_diff_service(team_name)
    return jsonify(history)

@api_bp.route('/team-win-rate-by-month/<team_name>', methods=['GET'])
def get_team_win_rate_by_month(team_name):
    from flask import request
    season = request.args.get('season')
    results = get_team_win_rate_by_month_service(team_name, season)
    return jsonify(results)

@api_bp.route('/teams', methods=['GET'])
def get_all_teams():
    teams = get_all_teams_service()
    return jsonify(teams)

@api_bp.route('/team-win-rate-against-others/<team_name>', methods=['GET'])
def get_team_win_rate_against_others(team_name):
    results = get_team_win_rate_against_others_service(team_name)
    return jsonify(results)

@api_bp.route('/match-details/<team_name>/<opponent_name>', methods=['GET'])
def get_match_details(team_name, opponent_name):
    from src.services import get_match_details_service
    matches = get_match_details_service(team_name, opponent_name)
    return jsonify(matches)

@api_bp.route('/team-standing-history/<team_name>', methods=['GET'])
def get_team_standing_history(team_name):
    history = get_team_standing_history_service(team_name)
    return jsonify(history)
