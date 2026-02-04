import pandas as pd

# Load the data
file_path = 'data/raw/ethiopia_fi_unified_data.csv'
df = pd.read_csv(file_path)

print("--- Record Counts by record_type ---")
print(df['record_type'].value_counts())

print("\n--- Record Counts by pillar ---")
print(df['pillar'].value_counts(dropna=False))

print("\n--- Record Counts by source_type ---")
print(df['source_type'].value_counts())

print("\n--- Record Counts by confidence ---")
print(df['confidence'].value_counts())

print("\n--- Temporal Range of Observations ---")
obs_df = df[df['record_type'] == 'observation'].copy()
obs_df['observation_date'] = pd.to_datetime(obs_df['observation_date'])
print(f"Start Date: {obs_df['observation_date'].min()}")
print(f"End Date: {obs_df['observation_date'].max()}")

print("\n--- Unique Indicators and Coverage ---")
indicators = obs_df.groupby('indicator_code').agg(
    count=('record_id', 'count'),
    min_date=('observation_date', 'min'),
    max_date=('observation_date', 'max')
)
print(indicators)

print("\n--- Cataloged Events ---")
events = df[df['record_type'] == 'event'].sort_values('observation_date')
print(events[['observation_date', 'indicator', 'value_text']])
