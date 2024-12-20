import pandas as pd

df = pd.read_csv('sizing2025.csv')
print("Columns in the CSV file:", df.columns)
print("First few rows of the file:")
print(df.head())

def clean_size_column(value):
    # Check if there's a dash and return everything before it
    if isinstance(value, str) and '-' in value:
        return value.split('-')[0].strip()
    return value

# Read the CSV file
try:
    df = pd.read_csv('sizing2025.csv')
    if df.empty:
        raise ValueError("Input file is empty.")
except FileNotFoundError:
    raise FileNotFoundError("The file 'sizing2025.csv' was not found.")

# Standardize column names
df.columns = df.columns.str.strip().str.lower()

# Ensure required columns exist
required_columns = ['team', 'jersey', 'shorts']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise KeyError(f"Missing required columns: {', '.join(missing_columns)}")


# Clean jersey and shorts columns
df['jersey'] = df['jersey'].apply(clean_size_column)
df['shorts'] = df['shorts'].apply(clean_size_column)

# Group by team and count sizes
jersey_summary = df.groupby(['team', 'jersey']).size().unstack(fill_value=0)
shorts_summary = df.groupby(['team', 'shorts']).size().unstack(fill_value=0)

size_order = ['YXS', 'YS', 'YM', 'YL', 'YXL', 'ASM', 'AM', 'AL', 'AXL', 'AXXL']

# Reorder columns according to standard sizes
jersey_cols = [col for col in size_order if col in jersey_summary.columns]
shorts_cols = [col for col in size_order if col in shorts_summary.columns]

# Reindex and add totals
jersey_summary = jersey_summary[jersey_cols]
shorts_summary = shorts_summary[shorts_cols]

# Add totals
jersey_summary['Total'] = jersey_summary.sum(axis=1)
shorts_summary['Total'] = shorts_summary.sum(axis=1)

# Save summaries to separate CSV files
jersey_summary.to_csv('jersey_summary_sorted_teams.csv')
shorts_summary.to_csv('shorts_summary_sorted_teams.csv')

# Save the cleaned original data
df.to_csv('sizing2025.csv', index=False)

print("Size summaries created successfully!")
print("\nJersey sizes by team:")
print(jersey_summary)
print("\nShorts sizes by team:")
print(shorts_summary)