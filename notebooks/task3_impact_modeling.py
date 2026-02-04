import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load enriched data
df = pd.read_csv('data/processed/ethiopia_fi_unified_data_enriched.csv')

# 1. Build Association Matrix
impacts = df[df['record_type'] == 'impact_link'].copy()
events = df[df['record_type'] == 'event'][['record_id', 'indicator', 'observation_date']].rename(columns={'record_id': 'parent_id', 'indicator': 'event_name'})

# Join
matrix_data = pd.merge(impacts, events, on='parent_id', how='left')

# Map magnitudes to numeric weights
# High = 5pp, Medium = 2pp, Low = 1pp (Assumed initial weights based on Findex shifts)
mag_map = {'high': 5.0, 'medium': 2.0, 'low': 1.0}
matrix_data['impact_weight'] = matrix_data['impact_magnitude'].map(mag_map)
matrix_data.loc[matrix_data['impact_direction'] == 'decrease', 'impact_weight'] *= -1

# Pivot to Matrix
association_matrix = matrix_data.pivot_table(
    index='event_name', 
    columns='related_indicator', 
    values='impact_weight', 
    aggfunc='sum'
).fillna(0)

# Visualization
plt.figure(figsize=(10, 6))
sns.heatmap(association_matrix, annot=True, cmap='RdYlGn', center=0)
plt.title("Event-Indicator Association Matrix (Weighted Impacts)")
plt.tight_layout()
plt.savefig('reports/figures/impact_association_matrix.png')

# 2. Impact Function (S-Curve for build-up)
def scure_impact(t, L=1.0, k=0.5, x0=12):
    """
    Simulates a gradual build-up of event impact.
    t: months since event
    L: max impact (magnitude)
    k: growth rate
    x0: midpoint (months)
    """
    return L / (1 + np.exp(-k * (t - x0)))

# 3. Test Model against Telebirr (EVT_0001)
# Telebirr launch: May 2021. Findex 2024: ~3.5 years later (42 months)
telebirr_impact_ownership = scure_impact(42, L=5.0, k=0.2, x0=12)
print(f"Predicted Telebirr Impact on Ownership after 42 months: {telebirr_impact_ownership:.2f} pp")

# Compare with observed: 35% (2017) -> 46% (2021) -> 49% (2024)
# Growth 2021-2024 was 3pp. 
# Prediction of 4.95pp is slightly higher than total growth, suggesting other counter-factors
# or that Telebirr's 'unique' inclusion was slower due to overlap.

# Save Matrix
association_matrix.to_csv('data/processed/impact_association_matrix.csv')
print("\n--- Event-Indicator Association Matrix ---")
print(association_matrix)

print("\nImpact modeling artifacts saved.")
