import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create reports directory if not exists
os.makedirs('reports/figures', exist_ok=True)

# Load data (using enriched data from Task 1)
df = pd.read_csv('data/processed/ethiopia_fi_unified_data_enriched.csv')

# 1. Dataset Overview
print("--- Dataset Overview ---")
print(df.groupby('record_type').size())
summary = df.groupby(['record_type', 'pillar']).size().unstack(fill_value=0)
print("\n--- Pillar Distribution ---")
print(summary)

# 2. Temporal Coverage
obs_df = df[df['record_type'] == 'observation'].copy()
obs_df['year'] = pd.to_datetime(obs_df['observation_date']).dt.year

coverage = obs_df.pivot_table(index='indicator_code', columns='year', values='value_numeric', aggfunc='count')
plt.figure(figsize=(12, 8))
sns.heatmap(coverage, annot=True, cmap='YlGnBu', cbar=False)
plt.title('Temporal Coverage of Financial Inclusion Indicators')
plt.tight_layout()
plt.savefig('reports/figures/temporal_coverage.png')

# 3. Data Quality (Confidence Distribution)
conf_dist = df['confidence'].value_counts()
plt.figure(figsize=(8, 6))
conf_dist.plot(kind='pie', autopct='%1.1f%%', colors=['#4CAF50', '#FFC107', '#F44336', '#2196F3'])
plt.title('Distribution of Data Confidence Levels')
plt.ylabel('')
plt.savefig('reports/figures/confidence_distribution.png')

# 4. Indicators Gaps
indicators_counts = obs_df['indicator_code'].value_counts()
print("\n--- Sparse Indicators ---")
print(indicators_counts[indicators_counts < 2])

print("Visualizations saved to reports/figures/")
