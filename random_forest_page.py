import tkinter as tk
from data_generator import generate_data
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import time
from tkinter import messagebox
from utils import save_model_metrics

data = None

def random_forest_page(parent):
    window = tk.Toplevel(parent)
    window.title("Random Forest")
    window.geometry("500x400")
    window.configure(bg="#e0f7fa")

    def generate():
        global data
        data = generate_data()
        messagebox.showinfo("Succès", "Données générées")

    def run_model():
        global data
        if data is None:
            messagebox.showwarning("Erreur", "Générez d'abord les données")
            return

        start = time.time()

        X = data[['X1', 'X2', 'X3']]
        y = data['Y']
        model = RandomForestRegressor()
        model.fit(X, y)
        y_pred = model.predict(X)
        mse = mean_squared_error(y, y_pred)

        importances = model.feature_importances_
        plt.figure()
        plt.bar(X.columns, importances)
        plt.title("Importance des Variables (Random Forest)")
        plt.ylabel("Importance")
        plt.grid(True)
        plt.show()

        end = time.time()
        duration = end - start
        energy = duration * 0.5

        save_model_metrics("Random Forest", duration, energy)
        messagebox.showinfo("Résultat", f"MSE : {mse:.4f}\n\nTemps : {duration:.2f}s\nÉnergie : {energy:.2f} kJ")

    def retour():
        window.destroy()

    tk.Label(window, text="Random Forest", font=("Arial", 18, "bold"), bg="#e0f7fa").pack(pady=30)
    tk.Button(window, text="Générer des données", command=generate, bg="#66bb6a", fg="white", width=30, height=2).pack(pady=10)
    tk.Button(window, text="Exécuter le modèle", command=run_model, bg="#42a5f5", fg="white", width=30, height=2).pack(pady=10)
    tk.Button(window, text="Retour", command=retour, bg="#ef5350", fg="white", width=30, height=2).pack(pady=10)
