import sys
import os
import pandas as pd

model_logs = []

def save_model_metrics(model_name, duration, energy):
    model_logs.append({
        "Model": model_name,
        "Execution Time (s)": round(duration, 2),
        "Energy (kJ)": round(energy, 2)
    })

def get_app_path():
    """Get the directory where the .exe or .py is located"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def export_metrics_to_excel():
    if model_logs:
        output_path = os.path.join(get_app_path(), "metrics.xlsx")
        df = pd.DataFrame(model_logs)
        df.to_excel(output_path, index=False)
