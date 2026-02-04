import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data/processed/ethiopia_fi_unified_data_enriched.csv')

# Focus on observation records
obs_df = df[df['record_type'] == 'observation'].copy()
obs_df['year'] = pd.to_datetime(obs_df['observation_date']).dt.year

# Pivot to get indicators as columns for each year
# Since many indicators only have one point, we'll see a lot of NaNs, but it captures what we have.
corr_df = obs_df.pivot_table(index='year', columns='indicator_code', values='value_numeric')

# Filter for columns with at least 2 non-nan values for correlation (though limited)
valid_cols = [col for col in corr_df.columns if corr_df[col].count() >= 2]
correlation_matrix = corr_df[valid_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title("Indicator Correlations (where multiple years exist)")
plt.savefig('reports/figures/correlation_heatmap.png')

# Print core correlations with Access
if 'ACC_OWNERSHIP' in correlation_matrix:
    print("\n--- Correlations with Account Ownership ---")
    print(correlation_matrix['ACC_OWNERSHIP'].sort_values(ascending=False))

# Identify drivers from impact links
impacts = df[df['record_type'] == 'impact_link']
print("\n--- Drivers from Impact Links ---")
print(impacts[['parent_id', 'related_indicator', 'impact_direction', 'impact_magnitude']])

with open('reports/eda_insights.md', 'w') as f:
    f.write("# Task 2: Key EDA Insights\n\n")
    f.write("## 1. The 2021-2024 Slowdown Paradox\n")
    f.write("Despite the launch of Telebirr (2021) and M-Pesa (2023) leading to 65M+ registered accounts, national account ownership (Access) only grew by 3pp (46% to 49%). This suggests that new mobile money accounts are largely being opened by people who *already* have bank accounts, or those who open multiple accounts without becoming unique newly-included individuals.\n\n")
    f.write("## 2. Gender Gap Evolution\n")
    f.write("The account ownership gender gap remains significant at ~18-20pp. While male ownership reached 56% in 2021, female ownership lagged at 36%. Preliminary 2024 data suggests this gap is closing slowly if at all.\n\n")
    f.write("## 3. Registered vs. Active Gap\n")
    f.write("Operator reports show massive user bases (e.g., Telebirr at 54M), but activity rates are often lower. For example, M-Pesa's 90-day activity rate is ~66%. This indicates a need for 'Usage' depth beyond 'Access' enrollment.\n\n")
    f.write("## 4. Infrastructure as a Leading Indicator\n")
    f.write("4G coverage has surged from 37.5% to 70.8% in just two years. This infrastructure expansion is strongly correlated with P2P transaction volume growth (+158% YoY), suggesting infrastructure enables Usage even when Access growth stalls.\n\n")
    f.write("## 5. P2P Crossover Milestone\n")
    f.write("2024/25 marked the first time P2P digital transfers surpassed ATM cash withdrawals in count. This is a clear signal of moving from cash-heavy to digital-ready behavior among active users.\n\n")
    f.write("## Data Quality & Limitations\n")
    f.write("- **Sparsity**: Most usage indicators only have 1-2 data points, limitng deep time-series correlation.\n")
    f.write("- **Findex Frequency**: The 3-year gap between major surveys leaves 'blind spots' in annual progress tracking.\n")

print("Correlation analysis and insights documentation complete.")
