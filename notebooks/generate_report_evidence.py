import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load enriched data
df = pd.read_csv('data/processed/ethiopia_fi_unified_data_enriched.csv')
df['date'] = pd.to_datetime(df['observation_date'])

# 1. THE SLOWDOWN PARADOX VISUALIZATION
# Comparing Mobile Money Accounts (Access) vs. Total Inclusion (Access)
access_codes = ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT']
slowdown_df = df[df['indicator_code'].isin(access_codes) & (df['gender'] == 'all')].sort_values('date')

plt.figure(figsize=(12, 7))
sns.lineplot(data=slowdown_df, x='date', y='value_numeric', hue='indicator', marker='o', linewidth=3)
# Highlight the gap
plt.fill_between(slowdown_df[slowdown_df['date'] >= '2021-01-01']['date'].unique(), 46, 55, alpha=0.1, color='red', label='Enrollment vs Inclusion Gap')
plt.title("The Slowdown Paradox: Enrollment Surge vs. Unique Inclusion Stagnation", fontsize=14, fontweight='bold')
plt.ylabel("Population Percentage (%)")
plt.annotate("Telebirr Launch", xy=(pd.to_datetime('2021-05-11'), 46), xytext=(pd.to_datetime('2019-01-01'), 35),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.grid(True, alpha=0.3)
plt.savefig('reports/figures/slowdown_paradox_evidence.png')

# 2. P2P CROSSOVER EVIDENCE
crossover_codes = ['USG_P2P_COUNT', 'USG_ATM_COUNT']
cross_df = df[df['indicator_code'].isin(crossover_codes)].sort_values('date')

plt.figure(figsize=(12, 7))
sns.barplot(data=cross_df, x='observation_date', y='value_numeric', hue='indicator')
plt.title("Evidence of Digital Maturity: P2P vs ATM Transaction Volume", fontsize=14, fontweight='bold')
plt.ylabel("Annual Transaction Count")
plt.xlabel("Fiscal Year")
plt.savefig('reports/figures/p2p_crossover_evidence.png')

# 3. IMPACT MODEL VALIDATION: TELEBIRR PREDICTED VS OBSERVED
# We previously calculated ~5.0pp gross, 3.0pp net.
# Let's visualize the build-up curve vs the 2024 observation point.
def scure_impact(t, L=1.0, k=0.5, x0=12):
    return L / (1 + np.exp(-k * (t - x0)))

t = np.linspace(0, 48, 100) # 4 years
y_pred = scure_impact(t, L=5.0, k=0.15, x0=18)
y_pred_calibrated = y_pred * 0.6 # The 0.6 overlap factor

plt.figure(figsize=(12, 7))
plt.plot(t, y_pred, 'k--', alpha=0.3, label='Gross Theoretical Impact')
plt.plot(t, y_pred_calibrated, 'b-', linewidth=3, label='Calibrated Net Impact (Overlap Adjusted)')
plt.scatter([42], [3.0], color='red', s=150, zorder=5, label='Actual 2021-2024 Growth (+3pp)')
plt.title("Impact Model Validation: Telebirr Theoretical vs. Observed (ACC_OWNERSHIP)", fontsize=14, fontweight='bold')
plt.xlabel("Months Post-Launch (May 2021)")
plt.ylabel("Incremental Percentage Points (pp)")
plt.legend()
plt.grid(True, alpha=0.2)
plt.savefig('reports/figures/impact_validation_evidence.png')

print("Enhanced evidence visualizations saved to reports/figures/")
