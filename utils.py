import sys
import os
import pandas as pd
from datetime import datetime
import tkinter.messagebox as messagebox

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
    print(f"Métriques sauvegardées pour {model_name}: durée={duration}s, énergie={energy}kJ")

def get_app_path():
    """Get the directory where the .exe or .py is located"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def generate_excel_report(session_duration=None):
    """Generate Excel report with all model metrics"""
    try:
        data = []
        for model_name, metrics in model_metrics.items():
            total_duration = sum(metric['duration'] for metric in metrics)
            total_energy = sum(metric['energy'] for metric in metrics)
            data.append({
                'Modèle': model_name,
                'Temps total (s)': round(total_duration, 3),
                'Énergie totale (kJ)': round(total_energy, 3)
            })
        if not data:
            data.append({
                'Modèle': 'Aucun modèle exécuté',
                'Temps total (s)': 0,
                'Énergie totale (kJ)': 0
            })
        df = pd.DataFrame(data)
        filename = os.path.join(get_app_path(), 'rapport_session.xlsx')
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Résumé', index=False)
        print(f"Rapport généré avec succès: {filename}")
        messagebox.showinfo("Rapport Excel", f"Les résultats ont été enregistrés dans :\n{filename}")
        return True
    except Exception as e:
        print(f"Erreur lors de la génération du rapport: {e}")
        return False
