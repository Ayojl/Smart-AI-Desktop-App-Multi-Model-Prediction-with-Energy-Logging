import sys
import os
import pandas as pd
from datetime import datetime

# Dictionary to store metrics for each model
model_metrics = {}

def save_model_metrics(model_name, duration, energy):
    """Save metrics for a model"""
    if model_name not in model_metrics:
        model_metrics[model_name] = []
    
    model_metrics[model_name].append({
        'timestamp': datetime.now(),
        'duration': duration,
        'energy': energy
    })

def get_app_path():
    """Get the directory where the .exe or .py is located"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def generate_excel_report():
    """Generate Excel report with all model metrics"""
    try:
        # Create DataFrame from metrics
        data = []
        for model_name, metrics in model_metrics.items():
            for metric in metrics:
                data.append({
                    'Modèle': model_name,
                    'Date/Heure': metric['timestamp'],
                    'Durée (s)': metric['duration'],
                    'Énergie (kJ)': metric['energy']
                })
        
        if not data:
            print("Aucune métrique à exporter")
            return
        
        df = pd.DataFrame(data)
        
        # Create Excel writer
        filename = 'metrics.xlsx'
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Write main metrics
            df.to_excel(writer, sheet_name='Métriques', index=False)
            
            # Calculate and write summary statistics
            summary = df.groupby('Modèle').agg({
                'Durée (s)': ['mean', 'min', 'max'],
                'Énergie (kJ)': ['mean', 'min', 'max']
            }).round(2)
            
            summary.to_excel(writer, sheet_name='Résumé')
        
        print(f"Rapport généré avec succès: {filename}")
        return True
    except Exception as e:
        print(f"Erreur lors de la génération du rapport: {e}")
        return False
