import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page Config
st.set_page_config(page_title="Ethiopia FI Forecast Dashboard", layout="wide", page_icon="🇪🇹")

# CSS for styling
st.markdown("""
<style>
    .main { backgroundColor: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #1e3a8a; }
</style>
""", unsafe_allow_html=True)

# Data Loading
@st.cache_data
def load_data():
    data_path = 'data/processed/ethiopia_fi_unified_data_enriched.csv'
    forecast_path = 'data/processed/forecasts_2025_2027.csv'
    
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['observation_date'])
    
    f_df = pd.read_csv(forecast_path)
    return df, f_df

df, f_df = load_data()

# Header
st.title("🇪🇹 Ethiopia Digital Financial Transformation Forecasting")
st.markdown("---")

# Tabs for Navigation
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "🔮 Forecasts", "💡 Insights"])

# --- Tab 1: Overview ---
with tab1:
    st.header("Key Performance Metrics")
    
    # Metrics Cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Latest Account Ownership
    latest_acc = df[(df['indicator_code'] == 'ACC_OWNERSHIP') & (df['gender'] == 'all')].iloc[-1]
    col1.metric("Account Ownership (2024)", f"{latest_acc['value_numeric']}%", "+3pp vs 2021")
    
    # Latest Digital Payments
    latest_usage = df[df['indicator_code'] == 'USG_DIGITAL_PAY'].iloc[-1]
    col2.metric("Digital Payment Adoption", f"{latest_usage['value_numeric']}%", "New Baseline")
    
    # Telebirr Users
    telebirr_users = df[df['indicator_code'] == 'USG_TELEBIRR_USERS'].iloc[-1]
    col3.metric("Telebirr Users", f"{telebirr_users['value_numeric']/1e6:.1f}M", "Active")
    
    # P2P/ATM Crossover
    crossover = df[df['indicator_code'] == 'USG_CROSSOVER'].iloc[-1]
    col4.metric("P2P/ATM Ratio", f"{crossover['value_numeric']}", "P2P > ATM")

    st.markdown("---")
    
    # P2P vs ATM Visualization
    st.subheader("The Digital Shift: P2P Transfers vs. ATM Withdrawals")
    crossover_data = df[df['indicator_code'].isin(['USG_P2P_COUNT', 'USG_ATM_COUNT'])]
    fig_cross = px.line(crossover_data, x='date', y='value_numeric', color='indicator', 
                        markers=True, title="P2P vs ATM Transaction Counts (FY2023-2025)",
                        labels={'value_numeric': 'Transaction Count', 'indicator': 'Channel'})
    st.plotly_chart(fig_cross, use_container_width=True)

# --- Tab 2: Trends ---
with tab2:
    st.header("Interactive Trend Analysis")
    
    # Selector
    all_indicators = df[df['record_type'] == 'observation']['indicator'].unique()
    selected_ind = st.multiselect("Select Indicators to Compare", all_indicators, default=["Account Ownership Rate", "Mobile Money Account Rate"])
    
    if selected_ind:
        trend_data = df[df['indicator'].isin(selected_ind)].sort_values('date')
        fig_trend = px.line(trend_data, x='date', y='value_numeric', color='indicator', markers=True, 
                            title="Historical Trends", labels={'value_numeric': 'Value'})
        st.plotly_chart(fig_trend, use_container_width=True)
    
    st.subheader("Gender Gap Analysis")
    gender_data = df[(df['indicator_code'] == 'ACC_OWNERSHIP') & (df['gender'].isin(['male', 'female']))]
    fig_gender = px.bar(gender_data, x='date', y='value_numeric', color='gender', barmode='group',
                         title="Account Ownership by Gender (2021-2024)")
    st.plotly_chart(fig_gender, use_container_width=True)

# --- Tab 3: Forecasts ---
with tab3:
    st.header("Financial Inclusion Projections (2025-2027)")
    
    # Scenario Selector
    scenario = st.selectbox("Select Scenario", ["base", "optimistic", "pessimistic"])
    
    col_f1, col_f2 = st.columns(2)
    
    # Access Forecast
    with col_f1:
        st.subheader("Account Ownership Forecast")
        raw_access = df[(df['indicator_code'] == 'ACC_OWNERSHIP') & (df['gender'] == 'all')]
        fc_access = f_df[(f_df['indicator'] == 'ACC_OWNERSHIP') & (f_df['scenario'] == scenario)]
        
        fig_f_acc = go.Figure()
        fig_f_acc.add_trace(go.Scatter(x=raw_access['date'], y=raw_access['value_numeric'], name="Historical", mode='lines+markers'))
        # Connect last historical to first forecast
        last_hist = raw_access.iloc[-1]
        fc_dates = [last_hist['date']] + [pd.to_datetime(f"{y}-12-31") for y in fc_access['year']]
        fc_vals = [last_hist['value_numeric']] + list(fc_access['forecast'])
        
        fig_f_acc.add_trace(go.Scatter(x=fc_dates, y=fc_vals, name="Forecast", mode='lines+markers', line=dict(dash='dash')))
        fig_f_acc.add_hline(y=70, line_dash="dot", annotation_text="NFIS-II Target (70%)", line_color="green")
        st.plotly_chart(fig_f_acc, use_container_width=True)
        
    # Usage Forecast
    with col_f2:
        st.subheader("Digital Payment Usage Forecast")
        raw_usage = df[df['indicator_code'] == 'USG_DIGITAL_PAY']
        fc_usage = f_df[(f_df['indicator'] == 'USG_DIGITAL_PAY') & (f_df['scenario'] == scenario)]
        
        fig_f_usg = go.Figure()
        fig_f_usg.add_trace(go.Scatter(x=raw_usage['date'], y=raw_usage['value_numeric'], name="Current", mode='lines+markers'))
        
        last_hist_u = raw_usage.iloc[-1]
        fc_dates_u = [last_hist_u['date']] + [pd.to_datetime(f"{y}-12-31") for y in fc_usage['year']]
        fc_vals_u = [last_hist_u['value_numeric']] + list(fc_usage['forecast'])
        
        fig_f_usg.add_trace(go.Scatter(x=fc_dates_u, y=fc_vals_u, name="Forecast", mode='lines+markers', line=dict(dash='dash')))
        st.plotly_chart(fig_f_usg, use_container_width=True)

    st.download_button("Download Forecast Data", f_df.to_csv(index=False), "forecasts_2025_2027.csv", "text/csv")

# --- Tab 4: Insights ---
with tab4:
    st.header("Consortium Key Questions")
    
    with st.expander("❓ What drives financial inclusion in Ethiopia?"):
        st.write("""
        - **Mobile Money (Telebirr/M-Pesa)**: The primary growth engine.
        - **Digital ID (Fayda)**: A secondary critical enabler for simplifying KYC.
        - **Infrastructure**: Surging 4G coverage (70.8%) enabling usage even where access lags.
        """)
        
    with st.expander("❓ Why did account ownership slow down (2021-2024)?"):
        st.write("""
        - **Account Duplication**: Many of the 65M+ mobile money accounts are held by users who already have bank accounts.
        - **KYC Barriers**: Difficulty in onboarding rural populations without digital identity cards.
        """)
        
    with st.expander("❓ Will Ethiopia meet its 70% inclusion target?"):
        st.write("""
        - **Base Projection**: Ethiopia is expected to reach ~64.6% by 2027.
        - **Target Gap**: The 70% target (NFIS-II) originally set for 2025 is likely to be delayed until 2028-2029.
        """)
    
    st.subheader("Transformation Timeline")
    events = df[df['record_type'] == 'event'].sort_values('date')
    st.dataframe(events[['observation_date', 'indicator', 'value_text', 'notes']].rename(columns={'indicator': 'Event'}))

# Footer
st.markdown("---")
st.caption("Developed by Selam Analytics for the National Bank of Ethiopia Consortium.")
