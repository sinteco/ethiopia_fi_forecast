import pandas as pd
import numpy as np

def load_data(filepath):
    """Loads the unified fi data CSV."""
    df = pd.read_csv(filepath)
    # Convert dates to datetime objects
    df['observation_date'] = pd.to_datetime(df['observation_date'])
    return df

def get_time_series(df, indicator_code, gender='all', location='national'):
    """Extracts a time series for a specific indicator."""
    mask = (
        (df['record_type'] == 'observation') & 
        (df['indicator_code'] == indicator_code) & 
        (df['gender'] == gender) & 
        (df['location'] == location)
    )
    ts_df = df[mask][['observation_date', 'value_numeric']].sort_values('observation_date')
    ts_df = ts_df.rename(columns={'observation_date': 'date', 'value_numeric': 'value'})
    return ts_df

def get_events(df):
    """Extracts event records."""
    return df[df['record_type'] == 'event'].sort_values('observation_date')

def preprocess_data(raw_filepath, output_filepath):
    """Main preprocessing function with enrichment."""
    df = load_data(raw_filepath)
    
    # 1. Add missing Digital Payment indicator for 2024 (from prompt)
    digital_payment_2024 = {
        'record_id': 'REC_ENR_0001',
        'record_type': 'observation',
        'pillar': 'USAGE',
        'indicator': 'Digital Payment Adoption Rate',
        'indicator_code': 'USG_DIGITAL_PAY',
        'indicator_direction': 'higher_better',
        'value_numeric': 35.0,
        'value_type': 'percentage',
        'unit': '%',
        'observation_date': pd.to_datetime('2024-11-29'),
        'source_name': 'Global Findex 2024 (Prompt)',
        'source_type': 'survey',
        'gender': 'all',
        'location': 'national'
    }
    df = pd.concat([df, pd.DataFrame([digital_payment_2024])], ignore_index=True)

    # 2. Add impact links (since they are missing from CSV but mentioned in task)
    # We'll map key events to indicators
    impact_links = [
        # Telebirr Launch -> Account Ownership & Digital Payments
        {'record_id': 'IMP_0001', 'record_type': 'impact_link', 'indicator_code': 'ACC_OWNERSHIP', 'related_indicator': 'EVT_TELEBIRR', 'impact_direction': 'increase', 'impact_magnitude': 'high'},
        {'record_id': 'IMP_0002', 'record_type': 'impact_link', 'indicator_code': 'USG_DIGITAL_PAY', 'related_indicator': 'EVT_TELEBIRR', 'impact_direction': 'increase', 'impact_magnitude': 'high'},
        # Safaricom/M-Pesa -> Account Ownership & Digital Payments
        {'record_id': 'IMP_0003', 'record_type': 'impact_link', 'indicator_code': 'ACC_OWNERSHIP', 'related_indicator': 'EVT_MPESA', 'impact_direction': 'increase', 'impact_magnitude': 'medium'},
        {'record_id': 'IMP_0004', 'record_type': 'impact_link', 'indicator_code': 'USG_DIGITAL_PAY', 'related_indicator': 'EVT_MPESA', 'impact_direction': 'increase', 'impact_magnitude': 'medium'},
        # Digital ID (Fayda) -> Account Ownership
        {'record_id': 'IMP_0005', 'record_type': 'impact_link', 'indicator_code': 'ACC_OWNERSHIP', 'related_indicator': 'EVT_FAYDA', 'impact_direction': 'increase', 'impact_magnitude': 'high'},
        # FX Reform -> Might have mixed impact but generally enabling
        {'record_id': 'IMP_0006', 'record_type': 'impact_link', 'indicator_code': 'USG_DIGITAL_PAY', 'related_indicator': 'EVT_FX_REFORM', 'impact_direction': 'increase', 'impact_magnitude': 'low'},
    ]
    df = pd.concat([df, pd.DataFrame(impact_links)], ignore_index=True)

    # Save processed data
    df.to_csv(output_filepath, index=False)
    
    # Extract key indicators for modeling
    access_ts = get_time_series(df, 'ACC_OWNERSHIP')
    usage_ts = get_time_series(df, 'USG_DIGITAL_PAY')
    events = get_events(df)
    
    return {
        'access': access_ts,
        'usage': usage_ts,
        'events': events,
        'full_df': df
    }

if __name__ == "__main__":
    # Test loading
    output_path = 'data/processed/processed_data.csv'
    data_dict = preprocess_data('data/raw/ethiopia_fi_unified_data.csv', output_path)
    print("Access TS:")
    print(data_dict['access'])
    print("\nUsage TS:")
    print(data_dict['usage'])
    print("\nEvents found:", len(data_dict['events']))
    print(f"Processed data saved to {output_path}")
