import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

class FinancialInclusionModel:
    def __init__(self, data_dict):
        self.data_dict = data_dict
        self.models = {}
        self.forecasts = {}

    def _prepare_ts(self, ts_df):
        if ts_df.empty:
            return None, None
        # Convert date to ordinal for regression
        X = np.array(ts_df['date'].map(datetime.toordinal)).reshape(-1, 1)
        y = ts_df['value'].values
        return X, y

    def train_baseline(self, indicator_code):
        """Trains a simple linear regression on available data."""
        ts_df = self.data_dict.get(indicator_code)
        if ts_df is None or len(ts_df) < 2:
            # If only one point (like Usage), we assume a default starting point or constant
            if indicator_code == 'usage' and not ts_df.empty:
                # Assume 0% in 2011 if missing
                ts_df = pd.concat([
                    pd.DataFrame({'date': [pd.to_datetime('2011-12-31')], 'value': [14.0] if indicator_code=='access' else [5.0]}),
                    ts_df
                ]).sort_values('date')
        
        X, y = self._prepare_ts(ts_df)
        model = LinearRegression()
        model.fit(X, y)
        self.models[indicator_code] = model
        return model

    def forecast(self, indicator_code, years=[2025, 2026, 2027], impact_multiplier=1.0):
        """Forecasts for given years, with an optional impact multiplier."""
        model = self.models.get(indicator_code)
        if not model:
            self.train_baseline(indicator_code)
            model = self.models.get(indicator_code)

        forecast_dates = [pd.to_datetime(f'{year}-12-31') for year in years]
        X_pred = np.array([d.toordinal() for d in forecast_dates]).reshape(-1, 1)
        
        # Baseline prediction
        y_pred = model.predict(X_pred)
        
        # Apply impact multiplier (e.g. accelerating growth due to new policies/products)
        # This is a simplification of the impact_link logic
        if impact_multiplier != 1.0:
            last_val = self.data_dict[indicator_code]['value'].iloc[-1]
            growth = y_pred - last_val
            y_pred = last_val + (growth * impact_multiplier)

        # Ensure values don't exceed 100 or drop below 0
        y_pred = np.clip(y_pred, 0, 100)
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'value': y_pred,
            'indicator_code': indicator_code,
            'type': 'forecast'
        })
        self.forecasts[indicator_code] = forecast_df
        return forecast_df

class ImpactAdjustedModel(FinancialInclusionModel):
    def forecast_with_impacts(self, indicator_code, years=[2025, 2026, 2027]):
        """Adjusts forecast based on specific event impact links."""
        # Get impact links for this indicator
        impacts = self.data_dict['full_df'][
            (self.data_dict['full_df']['record_type'] == 'impact_link') &
            (self.data_dict['full_df']['indicator_code'] == (
                'ACC_OWNERSHIP' if indicator_code == 'access' else 'USG_DIGITAL_PAY'
            ))
        ]
        
        # Calculate a cumulative impact score
        # High impact = 1.5x growth, Medium = 1.2x, Low = 1.1x
        multiplier = 1.0
        for _, row in impacts.iterrows():
            mag = row['impact_magnitude']
            if mag == 'high': multiplier += 0.2
            elif mag == 'medium': multiplier += 0.1
            elif mag == 'low': multiplier += 0.05
            
        return self.forecast(indicator_code, years, impact_multiplier=multiplier)

if __name__ == "__main__":
    from preprocessor import preprocess_data
    data_dict = preprocess_data('data/raw/ethiopia_fi_unified_data.csv', 'data/processed/processed_data.csv')
    
    model = ImpactAdjustedModel(data_dict)
    
    print("Forecasting Access...")
    access_fc = model.forecast_with_impacts('access')
    print(access_fc)
    
    print("\nForecasting Usage...")
    usage_fc = model.forecast_with_impacts('usage')
    print(usage_fc)
