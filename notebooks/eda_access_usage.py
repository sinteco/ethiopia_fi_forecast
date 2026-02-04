import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('data/processed/ethiopia_fi_unified_data_enriched.csv')

# Filter for Account Ownership
access_df = df[(df['indicator_code'] == 'ACC_OWNERSHIP') & (df['record_type'] == 'observation')].copy()
access_df['date'] = pd.to_datetime(access_df['observation_date'])
access_df = access_df.sort_values('date')

# 1. Plot Trajectory (National)
national_access = access_df[access_df['gender'] == 'all']
plt.figure(figsize=(10, 6))
plt.plot(national_access['date'], national_access['value_numeric'], marker='o', label='Account Ownership (%)')
plt.title("Ethiopia's Account Ownership Trajectory (2014-2024)")
plt.xlabel("Year")
plt.ylabel("Percentage (%)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('reports/figures/access_trajectory.png')

# 2. Gender Gap Analysis
gender_df = access_df[access_df['gender'].isin(['male', 'female'])].pivot(index='date', columns='gender', values='value_numeric')
if not gender_df.empty:
    gender_df['gender_gap'] = gender_df['male'] - gender_df['female']
    plt.figure(figsize=(10, 6))
    gender_df[['male', 'female']].plot(kind='bar', ax=plt.gca())
    plt.title("Account Ownership by Gender")
    plt.ylabel("Percentage (%)")
    plt.savefig('reports/figures/gender_gap_access.png')
    print("\n--- Gender Gap History ---")
    print(gender_df)

# 3. Mobile Money Penetration
mm_df = df[(df['indicator_code'] == 'ACC_MM_ACCOUNT') & (df['record_type'] == 'observation')].copy()
mm_df['date'] = pd.to_datetime(mm_df['observation_date'])
mm_df = mm_df.sort_values('date')

plt.figure(figsize=(10, 6))
plt.plot(mm_df['date'], mm_df['value_numeric'], marker='s', color='orange', label='Mobile Money Accounts (%)')
plt.title("Mobile Money Account Penetration (2021-2024)")
plt.ylabel("Percentage (%)")
plt.savefig('reports/figures/mm_penetration.png')

# 4. Usage vs Registered Gap
# M-Pesa Reg vs Active (from data)
mpesa_reg = df[df['indicator_code'] == 'USG_MPESA_USERS']['value_numeric'].values
mpesa_active = df[df['indicator_code'] == 'USG_MPESA_ACTIVE']['value_numeric'].values
if len(mpesa_reg) > 0 and len(mpesa_active) > 0:
    print(f"\nM-Pesa (Dec 2024): {mpesa_reg[0]} registered vs {mpesa_active[0]} 90-day active.")
    print(f"Activity Rate: {mpesa_active[0]/mpesa_reg[0]:.1%}")

print("\nAnalysis complete. Figures saved.")
