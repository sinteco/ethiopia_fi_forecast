import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Logistic Impact Function from Task 3
def scure_impact(t, L=1.0, k=0.5, x0=12):
    return L / (1 + np.exp(-k * (t - x0)))

class EthiopiaFiForecaster:
    def __init__(self, data_path, impact_matrix_path):
        self.df = pd.read_csv(data_path)
        self.matrix = pd.read_csv(impact_matrix_path, index_col=0)
        self.results = {}

    def get_baseline_model(self, indicator_code):
        obs = self.df[(self.df['indicator_code'] == indicator_code) & 
                      (self.df['record_type'] == 'observation') & 
                      (self.df['gender'] == 'all')].copy()
        obs['date'] = pd.to_datetime(obs['observation_date'])
        obs = obs.sort_values('date')
        
        # If Usage is too sparse, add a dummy 2011 point (0% inclusion) for baseline trend
        if len(obs) < 3:
            dummy = pd.DataFrame({
                'date': [pd.to_datetime('2011-12-31')],
                'value_numeric': [0.0] if indicator_code == 'USG_DIGITAL_PAY' else [14.0]
            })
            obs = pd.concat([dummy, obs[['date', 'value_numeric']]], ignore_index=True).sort_values('date')

        X = np.array(obs['date'].map(datetime.toordinal)).reshape(-1, 1)
        y = obs['value_numeric'].values
        model = LinearRegression().fit(X, y)
        return model, obs

    def run_forecast(self, indicator_code, scenario='base'):
        model, obs = self.get_baseline_model(indicator_code)
        
        # Calibration factors
        access_discount = 0.6 if scenario == 'base' else (0.8 if scenario == 'optimistic' else 0.4)
        impact_mult = 1.0 if scenario == 'base' else (1.3 if scenario == 'optimistic' else 0.7)
        
        forecast_years = [2025, 2026, 2027]
        forecast_dates = [pd.to_datetime(f'{y}-12-31') for y in forecast_years]
        X_pred = np.array([d.toordinal() for d in forecast_dates]).reshape(-1, 1)
        
        y_base = model.predict(X_pred)
        
        # Add Event Impacts (Aggregated)
        # We'll calculate total active impact relative to the 2021/2024 baselines
        # This is a simplified integration: total_delta = sum(impacts_since_last_findex)
        
        total_impact = np.zeros(len(forecast_years))
        
        # Events and their months since launch relative to forecast years
        events = {
            'Telebirr Launch': ('2021-05-17', 'high'),
            'M-Pesa Ethiopia Launch': ('2023-08-01', 'medium'),
            'Fayda Digital ID Program Rollout': ('2024-01-01', 'high')
        }
        
        for event_name, (launch_date, mag) in events.items():
            if indicator_code in self.matrix.columns:
                L = self.matrix.loc[event_name, indicator_code] * impact_mult
                if indicator_code == 'ACC_OWNERSHIP': L *= access_discount
                
                launch_dt = pd.to_datetime(launch_date)
                for i, fd in enumerate(forecast_dates):
                    months_since = (fd.year - launch_dt.year) * 12 + (fd.month - launch_dt.month)
                    total_impact[i] += scure_impact(months_since, L=L, k=0.15, x0=18)

        # Final y = last_observed + trend_growth + net_impact
        last_val = obs['value_numeric'].iloc[-1]
        last_date = obs['date'].iloc[-1]
        
        # Calculate trend growth relative to last observation
        trend_last = model.predict(np.array([[last_date.toordinal()]]))[0]
        y_final = last_val + (y_base - trend_last) + total_impact
        
        # Clipping
        y_final = np.clip(y_final, 0, 100)
        
        return pd.DataFrame({
            'year': forecast_years,
            'forecast': y_final,
            'scenario': scenario,
            'indicator': indicator_code
        })

# Execute
forecaster = EthiopiaFiForecaster('data/processed/ethiopia_fi_unified_data_enriched.csv', 
                                  'data/processed/impact_association_matrix.csv')

all_results = []
for ind in ['ACC_OWNERSHIP', 'USG_DIGITAL_PAY']:
    for scen in ['pessimistic', 'base', 'optimistic']:
        all_results.append(forecaster.run_forecast(ind, scen))

forecast_df = pd.concat(all_results)
forecast_df.to_csv('data/processed/forecasts_2025_2027.csv', index=False)

# Visualization
plt.figure(figsize=(12, 6))
for ind in ['ACC_OWNERSHIP', 'USG_DIGITAL_PAY']:
    sub = forecast_df[forecast_df['indicator'] == ind]
    for scen in ['base']:
        plt.plot(sub[sub['scenario']==scen]['year'], sub[sub['scenario']==scen]['forecast'], label=f'{ind} ({scen})', marker='o')
    plt.fill_between(sub[sub['scenario']=='base']['year'], 
                     sub[sub['scenario']=='pessimistic']['forecast'], 
                     sub[sub['scenario']=='optimistic']['forecast'], alpha=0.2)

plt.title("Financial Inclusion Forecasts 2025-2027 (Scenarios)")
plt.ylabel("Percentage (%)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('reports/figures/forecast_scenarios.png')

print("Forecasts generated and saved to data/processed/forecasts_2025_2027.csv")
print(forecast_df[forecast_df['scenario'] == 'base'])
