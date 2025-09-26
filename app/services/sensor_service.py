from typing import Dict, Any
import pandas as pd
import numpy as np

def calculate_average_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculates the average of COD, pH, TSS, waterFlow, and temperature.
    Computes WQI using piecewise scoring for COD, TSS, and pH.
    Returns a dictionary with averages and WQI_avg_sample.
    """
    required_cols = ["ph", "ss", "cod", "waterFlow", "temperature"]
    
    if df.empty or df[required_cols].isnull().any().any():
        return {col: None for col in required_cols} | {"WQI_avg_sample": None}

    # Compute average values
    avg_metrics = df[required_cols].mean().to_dict()
    avg_ph = avg_metrics["ph"]
    avg_cod = avg_metrics["cod"]
    avg_ss = avg_metrics["ss"]

    # --- Piecewise scoring functions ---
    def cod_score(cod: float) -> float:
        if cod <= 50: return 1.0
        elif cod <= 120: return 0.7
        elif cod <= 200: return 0.3
        else: return 0.0

    def tss_score(ss: float) -> float:
        if ss <= 50: return 1.0
        elif ss <= 100: return 0.7
        elif ss <= 200: return 0.3
        else: return 0.0

    def ph_score(ph: float) -> float:
        if 6.5 <= ph <= 8.5: return 1.0
        elif 6.0 <= ph < 6.5 or 8.5 < ph <= 9.0: return 0.7
        elif 5.5 <= ph < 6.0 or 9.0 < ph <= 9.5: return 0.3
        else: return 0.0

    # Compute individual scores
    c_score = cod_score(avg_cod)
    s_score = tss_score(avg_ss)
    p_score = ph_score(avg_ph)

    # Weighted WQI (adjust weights if needed)
    WQI_avg_sample = np.mean([c_score, s_score, p_score])

    avg_metrics["WQI_avg_sample"] = WQI_avg_sample
    return avg_metrics
