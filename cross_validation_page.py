import tkinter as tk
from data_generator import generate_data
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import time
from tkinter import messagebox
from utils import save_model_metrics

data = None

def cross_validation_page(parent):
    window = tk.Toplevel(parent)
    window.title("Validation Croisée")
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
        model = LinearRegression()
        scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
        mse_scores = -scores
        mse = mse_scores.mean()

        plt.boxplot(mse_scores)
        plt.title("Distribution des MSE - Validation Croisée")
        plt.ylabel("MSE")
        plt.grid(True)
        plt.show()

        end = time.time()
        duration = end - start
        energy = duration * 0.5

        save_model_metrics("Validation Croisée", duration, energy)
        messagebox.showinfo("Résultat", f"MSE moyen : {mse:.4f}\n\nTemps : {duration:.2f}s\nÉnergie : {energy:.2f} kJ")

    def retour():
        window.destroy()

    tk.Label(window, text="Validation Croisée", font=("Arial", 18, "bold"), bg="#e0f7fa").pack(pady=30)
    tk.Button(window, text="Générer des données", command=generate, bg="#66bb6a", fg="white", width=30, height=2).pack(pady=10)
    tk.Button(window, text="Exécuter le modèle", command=run_model, bg="#42a5f5", fg="white", width=30, height=2).pack(pady=10)
    tk.Button(window, text="Retour", command=retour, bg="#ef5350", fg="white", width=30, height=2).pack(pady=10)
