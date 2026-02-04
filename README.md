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

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```
3. Run tests:
   ```bash
   pytest tests/test_pipeline.py
   ```
