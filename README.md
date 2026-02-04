# Ethiopia Financial Inclusion Forecasting System

This project provides a forecasting system to predict Ethiopia's progress on financial inclusion (Access and Usage) for 2025-2027.

## Project Structure
- `data/`: Raw and processed datasets.
- `src/`: Core logic (preprocessing and modeling).
- `dashboard/`: Streamlit dashboard for visualization.
- `tests/`: Unit tests.
- `.github/workflows/`: CI/CD configuration.

## Tasks Implementation

### Task 1: Data Exploration and Enrichment
In this task, we explored the `ethiopia_fi_unified_data.csv` dataset and enriched it with additional observations, events, and impact links to improve the forecasting model.

**Key Activities:**
- **Schema Analysis**: Verified the unified schema and confirmed the presence of `observation`, `event`, and `target` record types.
- **Data Exploration**: Identified temporal range (2014-2025) and coverage for key indicators like `ACC_OWNERSHIP` and `USG_P2P_COUNT`.
- **Enrichment**:
  - Added **3 new observations**: Digital Payment Adoption (2024), Bank Branch Density (IMF), and Smartphone Penetration (GSMA).
  - Added **1 new event**: NBE Mobile Money Service Provider Directive (2025).
  - Added **4 new impact links**: Modeled the relationships between launches (Telebirr, M-Pesa) and financial inclusion outcomes.
- **Documentation**: Detailed all changes in [data_enrichment_log.md](data/processed/data_enrichment_log.md).

### Task 2: Exploratory Data Analysis
Completed a comprehensive analysis of the enriched dataset to understand the drivers of financial inclusion in Ethiopia.

**Key Deliverables:**
- **EDA Notebooks/Scripts**: Modular scripts for [Overview](notebooks/eda_overview.py), [Access/Usage](notebooks/eda_access_usage.py), [Timeline/Infra](notebooks/eda_timeline_infra.py), and [Correlation](notebooks/eda_correlation.py).
- **Visualizations**: Generated 6+ charts in [reports/figures/](reports/figures/) covering temporal coverage, trajectory, gender gap, and event timelines.
- **Insights Report**: Consolidated 5+ key insights in [eda_insights.md](reports/eda_insights.md), highlighting the 2021-2024 slowdown paradox and the P2P crossover milestone.

### Task 3: Event Impact Modeling
Developed a quantitative framework to simulate how major events shift financial inclusion trajectories.

**Key Deliverables:**
- **Modeling Notebook**: [task3_impact_modeling.py](notebooks/task3_impact_modeling.py) containing the logistic build-up logic and historical validation.
- **Association Matrix**: [impact_association_matrix.csv](data/processed/impact_association_matrix.csv) mapping event magnitudes to indicators.
- **Methodology Report**: [impact_methodology.md](reports/impact_methodology.md) explaining the S-curve approach and the 0.6 discount factor for Access indicators.

### Task 4: Forecasting Access and Usage
Generated data-driven projections for Ethiopia's financial inclusion metrics through 2027.

**Key Deliverables:**
- **Forecasting Notebook**: [task4_forecasting.py](notebooks/task4_forecasting.py) for scenario-based projections.
- **Forecast Data**: [forecasts_2025_2027.csv](data/processed/forecasts_2025_2027.csv) containing baseline, optimistic, and pessimistic values.
- **Scenario Visualization**: [forecast_scenarios.png](reports/figures/forecast_scenarios.png) showing the fan chart of projections.
- **Result Interpretation**: [forecasting_results.md](reports/forecasting_results.md) analyzing the likelihood of meeting national targets.

### Task 5: Dashboard Development
Created an interactive Streamlit-based forecasting system for stakeholders.

**Key Features:**
- **Overview**: High-level metrics (Access, Usage, P2P/ATM Ratio).
- **Trends**: Interactive time-series comparison with indicator selection.
- **Forecasts**: Scenario-based projections (Base/Optimistic/Pessimistic) with NFIS-II target overlays.
- **Insights**: Consolidated answers to the consortium's core strategic questions.

## Setup & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard
```bash
streamlit run dashboard/app.py
```

### 3. Run Pipeline Scripts (Optional)
To regenerate data or models:
- **Enrich Data**: `python3 scripts/enrich_data.py`
- **Impact Modeling**: `python3 notebooks/task3_impact_modeling.py`
- **Generate Forecasts**: `python3 notebooks/task4_forecasting.py`

### 4. Run Tests
```bash
pytest tests/test_pipeline.py
```
