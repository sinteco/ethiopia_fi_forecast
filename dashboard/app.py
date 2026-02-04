import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from preprocessor import preprocess_data
from model import ImpactAdjustedModel

st.set_page_config(page_title="Ethiopia Financial Inclusion Forecast", layout="wide")

st.title("🇪🇹 Ethiopia Digital Financial Transformation Forecasting")
st.markdown("""
This dashboard tracks and predicts Ethiopia's progress on two core dimensions of financial inclusion: 
**Access** (Account Ownership) and **Usage** (Digital Payment Adoption).
""")

# Load Data
@st.cache_data
def get_data():
    raw_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'ethiopia_fi_unified_data.csv')
    processed_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'processed_data.csv')
    return preprocess_data(raw_path, processed_path)

data_dict = get_data()

# Sidebar - Settings
st.sidebar.header("Forecast Settings")
years_to_forecast = st.sidebar.multiselect("Forecast Years", [2025, 2026, 2027], default=[2025, 2026, 2027])

# Run Models
model = ImpactAdjustedModel(data_dict)
access_fc = model.forecast_with_impacts('access', years=years_to_forecast)
usage_fc = model.forecast_with_impacts('usage', years=years_to_forecast)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Access: Account Ownership Rate")
    fig_access = go.Figure()
    # Historical
    fig_access.add_trace(go.Scatter(x=data_dict['access']['date'], y=data_dict['access']['value'], name="Historical", mode='lines+markers'))
    # Forecast
    fig_access.add_trace(go.Scatter(x=access_fc['date'], y=access_fc['value'], name="Forecast", mode='lines+markers', line=dict(dash='dash')))
    # Target
    fig_access.add_hline(y=70, line_dash="dot", annotation_text="NFIS-II Target (70%)", line_color="green")
    
    fig_access.update_layout(yaxis_title="Percentage (%)", xaxis_title="Year")
    st.plotly_chart(fig_access, use_container_width=True)

with col2:
    st.subheader("Usage: Digital Payment Adoption")
    fig_usage = go.Figure()
    # Historical (including enriched point)
    fig_usage.add_trace(go.Scatter(x=data_dict['usage']['date'], y=data_dict['usage']['value'], name="Historical/Current", mode='markers+lines'))
    # Forecast
    fig_usage.add_trace(go.Scatter(x=usage_fc['date'], y=usage_fc['value'], name="Forecast", mode='lines+markers', line=dict(dash='dash')))
    
    fig_usage.update_layout(yaxis_title="Percentage (%)", xaxis_title="Year")
    st.plotly_chart(fig_usage, use_container_width=True)

# Events Timeline
st.subheader("Key Transformation Events")
events = data_dict['events']
st.dataframe(events[['observation_date', 'indicator', 'value_text', 'notes']].rename(columns={'observation_date': 'Date', 'indicator': 'Event', 'value_text': 'Status'}))

# Impact Analysis
st.subheader("Impact Analysis")
st.markdown("""
The forecasts incorporate weighted impacts from major events:
- **High Impact**: Telebirr Launch, Fayda Digital ID Program
- **Medium Impact**: M-Pesa Ethiopia Launch
- **Low Impact**: Foreign Exchange Liberalization
""")
