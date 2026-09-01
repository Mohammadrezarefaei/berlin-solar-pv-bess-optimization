import pandas as pd
from src.bess_optimizer import optimize_bess_dispatch

def test_bess_optimization_output():
    hours = pd.date_range(start="2026-09-01 00:00", periods=24, freq="h")
    sample_prices = pd.Series([50] * 24, index=hours)
    
    schedule_df, revenue = optimize_bess_dispatch(sample_prices, max_capacity=100.0, max_power=50.0)
    
    # Assertions to verify correct schema and bounds
    assert not schedule_df.empty
    assert len(schedule_df) == 24
    assert "Charge (MW)" in schedule_df.columns
    assert "Discharge (MW)" in schedule_df.columns
    assert "SoC (MWh)" in schedule_df.columns
    assert schedule_df["SoC (MWh)"].max() <= 100.0
    assert schedule_df["SoC (MWh)"].min() >= 0.0
