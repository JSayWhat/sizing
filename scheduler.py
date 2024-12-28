import pandas as pd
import os


# Read and validate CSV
try:
    df = pd.read_csv('schedule.csv')
    if df.empty:
        raise ValueError("Input file is empty.")
except FileNotFoundError:
    raise FileNotFoundError("The file 'schedule.csv' was not found.")

# Print initial data info
print("Columns in the CSV file:", df.columns)
print("First few rows of the file:")
print(df.head())

# Standardize column names
df.columns = df.columns.str.strip().str.lower()

# Validate required columns
required_columns = ['week', 'home team', 'home division', 'away team', 'away division']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise KeyError(f"Missing required columns: {', '.join(missing_columns)}")

# Create a dictionary to store each team's schedule
team_schedules = {}
division_schedules = {}

# Iterate over each row to build the schedules
for _, row in df.iterrows():
    home_team = row['home team']
    away_team = row['away team']
    week = row['week']
    home_division = row['home division']
    away_division = row['away division']

    # Add home team schedule
    if home_team not in team_schedules:
        team_schedules[home_team] = []
    team_schedules[home_team].append({
        'week': week,
        'opponent': away_team,
        'location': 'Home',
        'division': away_division
    })

    # Add away team schedule
    if away_team not in team_schedules:
        team_schedules[away_team] = []
    team_schedules[away_team].append({
        'week': week,
        'opponent': home_team,
        'location': 'Away',
        'division': home_division
    })
    
     # Add schedules to divisions
    division_schedules.setdefault(home_division, []).append({
        'week': week,
        'team': home_team,
        'opponent': away_team,
        'location': 'Home',
        'opponent_division': away_division
    })
    division_schedules.setdefault(away_division, []).append({
        'week': week,
        'team': away_team,
        'opponent': home_team,
        'location': 'Away',
        'opponent_division': home_division
    })

# Format display options
pd.set_option('display.float_format', lambda x: '{:,.0f}'.format(x))

# Create output folders
team_output_folder = "organized_schedules/teams"
division_output_folder = "organized_schedules/divisions"
os.makedirs(team_output_folder, exist_ok=True)
os.makedirs(division_output_folder, exist_ok=True)

# Save team schedules as CSV files
for team, schedule in team_schedules.items():
    schedule_df = pd.DataFrame(schedule)
    schedule_df.insert(1, 'Empty_Column', '', allow_duplicates=False)  # Insert empty column
    filename = f"{team.replace(' ', '_').lower()}_schedule.csv"
    output_file_path = os.path.join(team_output_folder, filename)
    schedule_df.to_csv(output_file_path, index=False)
    print(f"Saved schedule for {team} to {filename}")

# Save division schedules as CSV files
for division, schedule in division_schedules.items():
    schedule_df = pd.DataFrame(schedule)
    filename = f"{division.replace(' ', '_').lower()}_schedule.csv"
    output_file_path = os.path.join(division_output_folder, filename)
    schedule_df.to_csv(output_file_path, index=False)
    print(f"Saved schedule for division {division} to {filename}")

