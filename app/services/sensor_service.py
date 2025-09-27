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

def calculate_ccme_wqi(df: pd.DataFrame, guidelines: Dict[str, float]) -> Dict[str, Any]:
    """
    Calculates CCME WQI for factory data safely.
    
    Parameters:
        df : DataFrame with columns ['monitorDate', 'ph', 'cod', 'ss', ...]
        guidelines : dict with regulatory limits, e.g.
                     {"ph_min": 6.5, "ph_max": 8.5, "cod": 100, "ss": 50}
    
    Returns:
        Dictionary with average parameters and CCME WQI (clamped 0-100)
    """
    parameters = ['ph', 'cod', 'ss']
    
    if df.empty:
        return {param: None for param in parameters} | {"WQI_CCME": None}

    # Ensure datetime
    df['monitorDate'] = pd.to_datetime(df['monitorDate'], errors='coerce')
    
    # Drop rows with missing numeric data
    df = df.dropna(subset=parameters)
    if df.empty:
        return {param: None for param in parameters} | {"WQI_CCME": None}
    
    # Step 1: Failures
    fail_matrix = pd.DataFrame(index=df.index)
    fail_matrix['ph'] = (df['ph'] < guidelines['ph_min']) | (df['ph'] > guidelines['ph_max'])
    fail_matrix['cod'] = df['cod'] > guidelines['cod']
    fail_matrix['ss'] = df['ss'] > guidelines['ss']
    
    # Step 2: F1 - Scope (% of parameters that failed at least once)
    failed_params = fail_matrix.any()
    F1 = failed_params.sum() / len(parameters) * 100
    
    # Step 3: F2 - Frequency (% of measurements failing)
    F2 = fail_matrix.sum().sum() / fail_matrix.size * 100
    
    # Step 4: F3 - Amplitude
    excursion_list = []
    for param in parameters:
        if param == 'ph':
            excursion = np.where(
                df['ph'] < guidelines['ph_min'],
                guidelines['ph_min']/df['ph'] - 1,
                np.where(df['ph'] > guidelines['ph_max'],
                         df['ph']/guidelines['ph_max'] - 1, 0)
            )
        else:
            excursion = np.where(df[param] > guidelines[param],
                                 df[param]/guidelines[param] - 1, 0)
        excursion_list.append(excursion)
    
    excursion_matrix = np.column_stack(excursion_list)
    nse = excursion_matrix.sum() / excursion_matrix.size if excursion_matrix.size > 0 else 0
    F3 = nse / (0.01 * nse + 0.01) if np.isfinite(nse) else 0
    
    # Step 5: CCME WQI
    WQI_CCME = 100 - (np.sqrt(F1**2 + F2**2 + F3**2) / 1.732)
    WQI_CCME = np.clip(WQI_CCME, 0, 100)  # safe for JSON
    
    # Step 6: Average metrics
    avg_metrics = df[parameters].mean().to_dict()
    avg_metrics['WQI_CCME'] = WQI_CCME
    
    return avg_metrics