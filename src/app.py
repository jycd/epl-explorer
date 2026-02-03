import os
import sys

# Add the project root to the python path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, send_from_directory
from src.routes import api_bp

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(api_bp)

# Serve logos folder
@app.route('/logos/<path:filename>')
def serve_logo(filename):
    return send_from_directory(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logos2'), filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/team-history')
def team_history():
    return render_template('team_history.html')

@app.route('/team-detail')
def team_detail():
    return render_template('team_detail.html')

@app.route('/match-details')
def match_details():
    return render_template('match_details.html')

@app.route('/average-stats')
def average_stats():
    return render_template('average_stats.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
