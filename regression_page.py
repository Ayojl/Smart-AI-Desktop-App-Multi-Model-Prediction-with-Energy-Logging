import tkinter as tk
from data_generator import generate_data
import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import messagebox
from utils import save_model_metrics

data = None

def regression_page(parent):
    window = tk.Toplevel(parent)
    window.title("Régression Linéaire")
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
        X = data[['X1']].values
        y = data['Y'].values
        X_b = np.c_[np.ones((len(X), 1)), X]
        theta = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y
        y_pred = X_b @ theta

        plt.figure()
        plt.scatter(X, y)
        plt.plot(X, y_pred, color='red')
        plt.title("Régression Linéaire")
        plt.grid(True)
        plt.show()

        end = time.time()
        duration = end - start
        energy = duration * 0.5

        save_model_metrics("Régression Linéaire", duration, energy)
        messagebox.showinfo("Résultat", f"Temps : {duration:.2f}s\nÉnergie : {energy:.2f} kJ")

    def retour():
        window.destroy()

    tk.Label(window, text="Régression Linéaire", font=("Arial", 18, "bold"), bg="#e0f7fa").pack(pady=30)
    tk.Button(window, text="Générer des données", command=generate, bg="#66bb6a", fg="white", width=30, height=2).pack(pady=10)
    tk.Button(window, text="Exécuter le modèle", command=run_model, bg="#42a5f5", fg="white", width=30, height=2).pack(pady=10)
    tk.Button(window, text="Retour", command=retour, bg="#ef5350", fg="white", width=30, height=2).pack(pady=10)
