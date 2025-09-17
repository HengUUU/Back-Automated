from typing import Dict, Any
import pandas as pd


def calculate_average_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculates the average of COD, pH, TSS, waterFlow, and temperature.
    If any value in the relevant columns is null, returns all metrics as None.
    
    Returns:
        A dictionary with the average value for each parameter, or None if any value is missing.
    """
    if df.empty:
        return {
            "ph": None,
            "cod": None,
            "ss": None,
            "waterFlow": None,
            "temperature": None
        }
    
    # Check if any value in the selected columns is NaN
    if df[['ph', 'ss', 'cod', 'waterFlow', 'temperature']].isnull().any().any():
        return {
            "ph": None,
            "cod": None,
            "ss": None,
            "waterFlow": None,
            "temperature": None
        }
    
    # Compute mean
    avg_metrics = df[['ph', 'ss', 'cod', 'waterFlow', 'temperature']].mean()
    return avg_metrics.to_dict()