import time
import os
import sys

# Add the project root to the python path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.utils import load_data, calculate_team_stats
from src.services import get_team_history_service

# Mock data directory if needed, but we'll use the real one
DATA_DIR = "data"

def benchmark_load_and_calc():
    # Warm up cache
    print("Warming up cache...")
    load_data("2324", DATA_DIR)
    
    start_time = time.time()
    # Simulate a heavy request: getting team history which loads 10 files
    # We'll pick a team that likely exists, e.g., "Arsenal" or "Chelsea"
    # We need to know a valid team name.
    # Let's just load one season first to get a team name
    df = load_data("2324", DATA_DIR)
    if df is not None:
        team = df['HomeTeam'].iloc[0]
        print(f"Benchmarking history for team: {team}")
        
        # Run multiple times to see cache effect
        for _ in range(5):
            history = get_team_history_service(team)
        
        print(f"History length: {len(history)}")
    else:
        print("Could not load 2324 data for setup.")

    end_time = time.time()
    print(f"Total time (5 iterations): {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    benchmark_load_and_calc()
