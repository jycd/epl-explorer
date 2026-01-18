import glob
import os
import sys

# Add the project root to the python path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_data, calculate_team_stats

def calculate_season_stats(data_dir):
    files = sorted(glob.glob(os.path.join(data_dir, "*_E0.csv")))
    
    if not files:
        print("No data files found.")
        return

    print(f"{'Season':<10} | {'Team':<25} | {'Matches':<7} | {'Win %':<7} | {'Draw %':<7} | {'Loss %':<7}")
    print("-" * 80)

    for f in files:
        filename = os.path.basename(f)
        season = filename.split('_')[0]
        
        try:
            df = load_data(season, data_dir)
            
            if df is None:
                print(f"Skipping {filename}: Could not load data.")
                continue

            stats = calculate_team_stats(df)
            
            # Sort by Win Rate descending (already sorted in calculate_team_stats but by overall win rate)
            # The structure returned by calculate_team_stats is a list of dicts with 'overall' key
            # We need to adapt it to print format
            
            for stat in stats:
                team_name = stat['team']
                matches = stat['overall']['matches']
                win_rate = stat['overall']['win_rate']
                draw_rate = stat['overall']['draw_rate']
                loss_rate = stat['overall']['loss_rate']
                
                print(f"{season:<10} | {team_name:<25} | {matches:<7} | {win_rate:<7.2f} | {draw_rate:<7.2f} | {loss_rate:<7.2f}")
            
            print("-" * 80)

        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Assuming script is run from project root or scripts dir, but data is in project root/data
    # If run from scripts/, data is ../data
    # If run from root, data is data/
    
    # Let's make it robust by finding the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(project_root, "data")
    
    calculate_season_stats(data_dir)
