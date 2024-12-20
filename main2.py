import pandas as pd

def clean_size_column(value):
    if isinstance(value, str) and '-' in value:
        return value.split('-')[0].strip()
    return value

# Read and validate CSV
try:
    df = pd.read_csv('sizing2025.csv')
    if df.empty:
        raise ValueError("Input file is empty.")
except FileNotFoundError:
    raise FileNotFoundError("The file 'sizing2025.csv' was not found.")

# Print initial data info
print("Columns in the CSV file:", df.columns)
print("First few rows of the file:")
print(df.head())

# Standardize column names
df.columns = df.columns.str.strip().str.lower()

# Validate required columns
required_columns = ['team', 'jersey', 'shorts']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise KeyError(f"Missing required columns: {', '.join(missing_columns)}")

# Team mapping dictionary
team_mapping = {
    'Dolphins': 'Miami Dolphins',
    'Chiefs': 'Kansas City Chiefs',
    'Bengals': 'Cincinnati Bengals',
    'Buccaneers': 'Tampa Bay Buccaneers',
    'Bills': 'Buffalo Bills',
    'Cardinals': 'Arizona Cardinals',
    'Falcons': 'Atlanta Falcons',
    'Ravens': 'Baltimore Ravens',
    'Panthers': 'Carolina Panthers',
    'Bears': 'Chicago Bears',
    'Browns': 'Cleveland Browns',
    'Cowboys': 'Dallas Cowboys',
    'Broncos': 'Denver Broncos',
    'Lions': 'Detroit Lions',
    'Packers': 'Green Bay Packers',
    'Texans': 'Houston Texans',
    'Colts': 'Indianapolis Colts',
    'Jaguars': 'Jacksonville Jaguars',
    'Chargers': 'Los Angeles Chargers',
    'Rams': 'Los Angeles Rams',
    'Vikings': 'Minnesota Vikings',
    'Giants': 'N.Y. Giants',
    'Jets': 'N.Y. Jets',
    'Patriots': 'New England Patriots',
    'Saints': 'New Orleans Saints',
    'Eagles': 'Philadelphia Eagles',
    'Steelers': 'Pittsburgh Steelers',
    '49ers': 'San Francisco 49ers',
    'Seahawks': 'Seattle Seahawks',
    'Titans': 'Tennessee Titans',
    'Commanders': 'Washington Commanders'
}
# Define team information as list of tuples
team_order = [
    ('Arizona Cardinals', 'Cardinals'),
    ('Atlanta Falcons', 'Falcons'),
    ('Baltimore Ravens', 'Ravens'),
    ('Buffalo Bills', 'Bills'),
    ('Carolina Panthers', 'Panthers'),
    ('Chicago Bears', 'Bears'),
    ('Cincinnati Bengals', 'Bengals'),
    ('Cleveland Browns', 'Browns'),
    ('Dallas Cowboys', 'Cowboys'),
    ('Denver Broncos', 'Broncos'),
    ('Detroit Lions', 'Lions'),
    ('Green Bay Packers', 'Packers'),
    ('Houston Texans', 'Texans'),
    ('Indianapolis Colts', 'Colts'),
    ('Jacksonville Jaguars', 'Jaguars'),
    ('Kansas City Chiefs', 'Chiefs'),
    ('Los Angeles Chargers', 'Chargers'),
    ('Los Angeles Rams', 'Rams'),
    ('Miami Dolphins', 'Dolphins'),
    ('Minnesota Vikings', 'Vikings'),
    ('N.Y. Giants', 'Giants'),
    ('N.Y. Jets', 'Jets'),
    ('New England Patriots', 'Patriots'),
    ('New Orleans Saints', 'Saints'),
    ('Philadelphia Eagles', 'Eagles'),
    ('Pittsburgh Steelers', 'Steelers'),
    ('San Francisco 49ers', '49ers'),
    ('Seattle Seahawks', 'Seahawks'),
    ('Tampa Bay Buccaneers', 'Buccaneers'),
    ('Tennessee Titans', 'Titans'),
    ('Washington Commanders', 'Commanders')
]

# Apply team mapping
df['team'] = df['team'].map(lambda x: team_mapping.get(x, x))

# Clean size columns
df['jersey'] = df['jersey'].apply(clean_size_column)
df['shorts'] = df['shorts'].apply(clean_size_column)

# Define size order
size_order = ['YXS', 'YS', 'YM', 'YL', 'YXL', 'ASM', 'AM', 'AL', 'AXL', 'AXXL']

# Create summaries (single operation)
jersey_summary = df.groupby(['team', 'jersey']).size().unstack(fill_value=0).astype(int)
shorts_summary = df.groupby(['team', 'shorts']).size().unstack(fill_value=0).astype(int)

# Get available size columns
jersey_cols = [col for col in size_order if col in jersey_summary.columns]
shorts_cols = [col for col in size_order if col in shorts_summary.columns]

# Order columns (no intermediate filling)
jersey_summary = jersey_summary[jersey_cols].fillna(0).astype(int)
shorts_summary = shorts_summary[shorts_cols].fillna(0).astype(int)

# Create and apply team aliases with NaN handling
team_aliases = {team[0]: team[1] for team in team_order}
jersey_summary = jersey_summary.reindex([t[0] for t in team_order], fill_value=0)
shorts_summary = shorts_summary.reindex([t[0] for t in team_order], fill_value=0)

# Add totals (single operation)
jersey_summary['Total'] = jersey_summary.sum(axis=1)
shorts_summary['Total'] = shorts_summary.sum(axis=1)

# Format display options
pd.set_option('display.float_format', lambda x: '{:,.0f}'.format(x))
  # '%.0f' % x)

# Create and apply team aliases
team_aliases = {team[0]: team[1] for team in team_order}
jersey_summary = jersey_summary.reindex([t[0] for t in team_order])
shorts_summary = shorts_summary.reindex([t[0] for t in team_order])

# Save results
jersey_summary.to_csv('jersey_summary_sorted_teams.csv')
shorts_summary.to_csv('shorts_summary_sorted_teams.csv')
df.to_csv('sizing2025.csv', index=False)

# Print results
print("\nSize summaries created successfully!")
print("\nJersey sizes by team:")
print(jersey_summary)
print("\nShorts sizes by team:")
print(shorts_summary)