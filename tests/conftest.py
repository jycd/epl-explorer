import pytest
import os
import sys

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_data_dir(tmp_path):
    """Create a temporary data directory with sample CSV files."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Create a sample CSV file for season 2324
    csv_content = """Div,Date,Time,HomeTeam,AwayTeam,FTHG,FTAG,FTR,HTHG,HTAG,HTR,Referee,HS,AS,HST,AST,HF,AF,HC,AC,HY,AY,HR,AR
E0,11/08/2023,20:00,Burnley,Man City,0,3,A,0,2,A,C Pawson,6,17,1,8,11,8,6,5,0,0,1,0
E0,12/08/2023,12:30,Arsenal,Nott'm Forest,2,1,H,2,0,H,M Oliver,15,6,7,2,12,12,8,3,2,2,0,0
E0,12/08/2023,15:00,Bournemouth,West Ham,1,1,D,0,0,D,P Bankes,14,16,5,3,9,14,5,4,1,4,0,0
E0,12/08/2023,15:00,Brighton,Luton,4,1,H,1,0,H,D Coote,27,9,12,3,11,12,6,7,2,2,0,0
E0,12/08/2023,15:00,Everton,Fulham,0,1,A,0,0,D,S Attwell,19,9,9,2,12,6,10,4,0,2,0,0
E0,12/08/2023,15:00,Sheffield United,Crystal Palace,0,1,A,0,0,D,J Brooks,8,24,1,5,13,10,5,5,3,0,0,0
E0,12/08/2023,17:30,Newcastle,Aston Villa,5,1,H,2,1,H,A Madley,17,16,13,6,12,14,6,4,4,4,0,0
E0,13/08/2023,14:00,Brentford,Tottenham,2,2,D,2,2,D,R Jones,11,18,6,6,9,10,3,5,2,4,0,0
E0,13/08/2023,16:30,Chelsea,Liverpool,1,1,D,1,1,D,A Taylor,10,13,4,1,5,10,4,4,3,3,0,0
E0,14/08/2023,20:00,Man United,Wolves,1,0,H,0,0,D,S Hooper,15,23,3,6,13,12,8,7,2,2,0,0
"""
    (data_dir / "2324_E0.csv").write_text(csv_content)
    
    # Create another season 2223
    csv_content_2223 = """Div,Date,Time,HomeTeam,AwayTeam,FTHG,FTAG,FTR,HTHG,HTAG,HTR,Referee,HS,AS,HST,AST,HF,AF,HC,AC,HY,AY,HR,AR
E0,05/08/2022,20:00,Crystal Palace,Arsenal,0,2,A,0,1,A,A Taylor,10,10,2,2,16,11,3,5,1,2,0,0
E0,06/08/2022,12:30,Fulham,Liverpool,2,2,D,1,0,H,A Madley,9,11,3,4,7,9,4,4,2,0,0,0
"""
    (data_dir / "2223_E0.csv").write_text(csv_content_2223)

    return str(data_dir)
