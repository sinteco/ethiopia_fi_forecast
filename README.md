# Ethiopia Financial Inclusion Forecasting System

This project provides a forecasting system to predict Ethiopia's progress on financial inclusion (Access and Usage) for 2025-2027.

## Project Structure
- `data/`: Raw and processed datasets.
- `src/`: Core logic (preprocessing and modeling).
- `dashboard/`: Streamlit dashboard for visualization.
- `tests/`: Unit tests.
- `.github/workflows/`: CI/CD configuration.

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
