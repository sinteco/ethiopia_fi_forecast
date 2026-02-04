import pytest
import pandas as pd
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from preprocessor import preprocess_data
from model import ImpactAdjustedModel

def test_preprocessing():
    raw_path = 'data/raw/ethiopia_fi_unified_data.csv'
    processed_path = 'data/processed/processed_data.csv'
    data_dict = preprocess_data(raw_path, processed_path)
    
    assert 'access' in data_dict
    assert 'usage' in data_dict
    assert not data_dict['access'].empty
    assert os.path.exists(processed_path)

def test_forecasting():
    raw_path = 'data/raw/ethiopia_fi_unified_data.csv'
    processed_path = 'data/processed/processed_data.csv'
    data_dict = preprocess_data(raw_path, processed_path)
    
    model = ImpactAdjustedModel(data_dict)
    access_fc = model.forecast_with_impacts('access', years=[2025, 2026, 2027])
    
    assert len(access_fc) == 3
    assert all(access_fc['value'] > 0)
    assert all(access_fc['value'] <= 100)
