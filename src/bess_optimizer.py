import pandas as pd
import pulp

def optimize_bess_dispatch(prices: pd.Series, max_capacity=100.0, max_power=50.0, efficiency=0.90, initial_soc=50.0):
    """
    Optimizes BESS charge/discharge schedule using PuLP linear programming 
    to maximize revenue from market price arbitrage.
    """
    eta = efficiency ** 0.5
    price_list = prices.values[:len(prices)]
    time_periods = range(len(price_list))
    
    prob = pulp.LpProblem("BESS_Arbitrage_Optimization", pulp.LpMaximize)
    
    charge = {t: pulp.LpVariable(f"charge_{t}", lowBound=0, upBound=max_power) for t in time_periods}
    discharge = {t: pulp.LpVariable(f"discharge_{t}", lowBound=0, upBound=max_power) for t in time_periods}
    soc = {t: pulp.LpVariable(f"soc_{t}", lowBound=0, upBound=max_capacity) for t in time_periods}
    
    prob += pulp.lpSum((discharge[t] - charge[t]) * price_list[t] for t in time_periods), "Total_Arbitrage_Profit"
    
    for t in time_periods:
        if t == 0:
            prob += soc[t] == initial_soc + (charge[t] * eta) - (discharge[t] / eta), f"SoC_Balance_{t}"
        else:
            prob += soc[t] == soc[t-1] + (charge[t] * eta) - (discharge[t] / eta), f"SoC_Balance_{t}"
            
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    schedule_data = []
    for t in time_periods:
        schedule_data.append({
            "Hour": t,
            "Price (EUR/MWh)": round(price_list[t], 2),
            "Charge (MW)": round(charge[t].varValue, 2),
            "Discharge (MW)": round(discharge[t].varValue, 2),
            "SoC (MWh)": round(soc[t].varValue, 2)
        })
        
    return pd.DataFrame(schedule_data), pulp.value(prob.objective)
