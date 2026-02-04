import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('data/processed/ethiopia_fi_unified_data_enriched.csv')

# 1. Timeline Visualization
events = df[df['record_type'] == 'event'].copy()
events['date'] = pd.to_datetime(events['observation_date'])
events = events.sort_values('date')

# 2. Overlay Events on Access Trend
access_df = df[(df['indicator_code'] == 'ACC_OWNERSHIP') & (df['record_type'] == 'observation') & (df['gender'] == 'all')]
access_df['date'] = pd.to_datetime(access_df['observation_date'])
access_df = access_df.sort_values('date')

plt.figure(figsize=(12, 7))
plt.plot(access_df['date'], access_df['value_numeric'], marker='o', label='Account Ownership (%)', linewidth=2)

# Add event markers
for idx, row in events.iterrows():
    plt.axvline(x=row['date'], color='red', linestyle='--', alpha=0.3)
    plt.text(row['date'], plt.ylim()[0], row['indicator'], rotation=90, verticalalignment='bottom', fontsize=8, color='red')

plt.title("Account Ownership Trend with Key Events")
plt.xlabel("Year")
plt.ylabel("Percentage (%)")
plt.legend()
plt.tight_layout()
plt.savefig('reports/figures/event_timeline_access.png')

# 3. Infrastructure Analysis (4G vs Access)
infra_codes = ['ACC_4G_COV', 'ACC_MOBILE_PEN']
infra_df = df[df['indicator_code'].isin(infra_codes) & (df['record_type'] == 'observation')].copy()
infra_df['date'] = pd.to_datetime(infra_df['observation_date'])

plt.figure(figsize=(10, 6))
for code in infra_codes:
    data = infra_df[infra_df['indicator_code'] == code]
    plt.plot(data['date'], data['value_numeric'], marker='x', label=code)

plt.title("Infrastructure Enablers Trajectory")
plt.ylabel("Percentage (%)")
plt.legend()
plt.savefig('reports/figures/infrastructure_trends.png')

print("Timeline and Infrastructure analysis complete.")
