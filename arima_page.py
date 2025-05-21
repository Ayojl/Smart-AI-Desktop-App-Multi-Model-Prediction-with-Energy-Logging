import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import time
from tkinter import messagebox
from utils import save_model_metrics

ts = None

def arima_page(parent):
    window = tk.Toplevel(parent)
    window.title("ARIMA")
    window.geometry("500x400")
    window.configure(bg="#e0f7fa")

    def generate():
        global ts
        ts = np.cumsum(np.random.randn(200))
        messagebox.showinfo("Succès", "Série temporelle générée")

    def run_model():
        global ts
        if ts is None:
            messagebox.showwarning("Erreur", "Générez d'abord la série")
            return

        start = time.time()

        model = ARIMA(ts, order=(2, 1, 2))
        fit = model.fit()
        forecast = fit.predict(start=190, end=210)

        plt.figure()
        plt.plot(ts, label="Série réelle")
        plt.plot(range(190, 211), forecast, label="Prévision", color='red')
        plt.title("Prévision ARIMA")
        plt.legend()
        plt.grid(True)
        plt.show()

        end = time.time()
        duration = end - start
        energy = duration * 0.5
        save_model_metrics("ARIMA", duration, energy)
        messagebox.showinfo("Résultat", f"Temps : {duration:.2f}s\nÉnergie : {energy:.2f} kJ")

    def retour():
        window.destroy()

    tk.Label(window, text="ARIMA (Time Series)", font=("Arial", 18, "bold"), bg="#e0f7fa").pack(pady=30)
    tk.Button(window, text="Générer la série", command=generate, bg="#66bb6a", fg="white", width=30, height=2).pack(pady=10)
    tk.Button(window, text="Exécuter ARIMA", command=run_model, bg="#42a5f5", fg="white", width=30, height=2).pack(pady=10)
    tk.Button(window, text="Retour", command=retour, bg="#ef5350", fg="white", width=30, height=2).pack(pady=10)
