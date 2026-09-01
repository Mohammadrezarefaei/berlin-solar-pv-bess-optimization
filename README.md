# Berlin Solar PV & BESS Optimization Pipeline

End-to-end data science and mathematical optimization platform featuring machine learning-based solar photovoltaic power generation forecasting for Berlin grids, combined with an optimal Battery Energy Storage System (BESS) market arbitrage dispatch model.

## Project Architecture
- **Solar PV Forecasting**: XGBoost regressor trained on meteorological features (solar zenith angle, wind speed, temperature) with chronological data splitting.
- **BESS Optimization**: Linear programming solver via **PuLP** utilizing real-world Day-Ahead electricity prices from the **ENTSO-E Transparency Platform**.
- **Interactive Dashboard**: Built with **Streamlit** featuring real-time data integration, mock fallbacks, and animated visualization analytics.

## Tech Stack
- **Language**: Python
- **ML / Optimization**: Scikit-Learn, XGBoost, PuLP
- **Data / APIs**: Pandas, NumPy, ENTSO-E API (`entsoe-py`)
- **Visualization**: Matplotlib (Dark Theme), Streamlit
- **CI/CD & Testing**: GitHub Actions, Pytest
