import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import time
from tkinter import messagebox
from utils import save_model_metrics
from sklearn.metrics import mean_squared_error

data = None
model = None


def arima_page(parent):
    window = ctk.CTkToplevel(parent)
    window.title("ARIMA - Prédiction de séries temporelles")
    window.geometry("1100x850")
    window.transient(parent)
    window.grab_set()
    def on_close():
        window.destroy()
    window.protocol("WM_DELETE_WINDOW", on_close)

    # Main frame
    main_frame = ctk.CTkFrame(window)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Titre et explication
    title_label = ctk.CTkLabel(
        main_frame,
        text="Modèle ARIMA",
        font=ctk.CTkFont(size=28, weight="bold")
    )
    title_label.pack(pady=(10, 5))

    help_label = ctk.CTkLabel(
        main_frame,
        text="ARIMA est un modèle de prévision pour séries temporelles. Choisissez vos paramètres, générez des données ou importez-en, puis prédisez le futur !",
        font=ctk.CTkFont(size=14),
        wraplength=900,
        justify="center"
    )
    help_label.pack(pady=(0, 15))

    # Paramètres utilisateur
    controls_frame = ctk.CTkFrame(main_frame)
    controls_frame.pack(pady=10, padx=10, fill="x")

    # Nombre de points
    ctk.CTkLabel(controls_frame, text="Nombre de points :").grid(row=0, column=0, padx=5, pady=5)
    n_points = ctk.CTkEntry(controls_frame, width=80)
    n_points.insert(0, "100")
    n_points.grid(row=0, column=1, padx=5, pady=5)

    # Paramètres ARIMA
    ctk.CTkLabel(controls_frame, text="p (AR) :").grid(row=0, column=2, padx=5, pady=5)
    p_param = ctk.CTkEntry(controls_frame, width=50)
    p_param.insert(0, "2")
    p_param.grid(row=0, column=3, padx=5, pady=5)

    ctk.CTkLabel(controls_frame, text="d (I) :").grid(row=0, column=4, padx=5, pady=5)
    d_param = ctk.CTkEntry(controls_frame, width=50)
    d_param.insert(0, "1")
    d_param.grid(row=0, column=5, padx=5, pady=5)

    ctk.CTkLabel(controls_frame, text="q (MA) :").grid(row=0, column=6, padx=5, pady=5)
    q_param = ctk.CTkEntry(controls_frame, width=50)
    q_param.insert(0, "2")
    q_param.grid(row=0, column=7, padx=5, pady=5)

    # Horizon de prédiction
    ctk.CTkLabel(controls_frame, text="Horizon de prédiction :").grid(row=0, column=8, padx=5, pady=5)
    horizon_entry = ctk.CTkEntry(controls_frame, width=60)
    horizon_entry.insert(0, "10")
    horizon_entry.grid(row=0, column=9, padx=5, pady=5)

    # Génération ou importation de données
    data_frame = ctk.CTkFrame(main_frame)
    data_frame.pack(pady=10, padx=10, fill="x")

    def generate():
        global data
        try:
            n = int(n_points.get())
            t = np.linspace(0, 10, n)
            trend = 0.5 * t
            seasonal = 2 * np.sin(2 * np.pi * t)
            noise = np.random.normal(0, 0.5, n)
            data = pd.Series(trend + seasonal + noise)
            messagebox.showinfo("Succès", "Données générées !")
            run_model()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération : {e}")

    generate_btn = ctk.CTkButton(
        data_frame,
        text="Générer des données",
        command=generate,
        fg_color="green",
        hover_color="darkgreen"
    )
    generate_btn.pack(side="left", padx=10)

    # Zone de graphique
    plot_frame = ctk.CTkFrame(main_frame)
    plot_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Zone de résultats
    results_frame = ctk.CTkFrame(main_frame)
    results_frame.pack(pady=10, padx=10, fill="x")

    metrics_label = ctk.CTkLabel(
        results_frame,
        text="",
        font=ctk.CTkFont(size=13)
    )
    metrics_label.pack(pady=5)

    def run_model():
        global data, model
        if data is None:
            messagebox.showwarning("Erreur", "Générez ou importez d'abord les données")
            return
        try:
            p = int(p_param.get())
            d = int(d_param.get())
            q = int(q_param.get())
            horizon = int(horizon_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Tous les paramètres doivent être des entiers")
            return
        start = time.time()
        model = ARIMA(data, order=(p, d, q))
        results = model.fit()
        forecast = results.get_forecast(steps=horizon)
        forecast_mean = forecast.predicted_mean
        conf_int = forecast.conf_int()
        # Calcul du MSE sur la partie train (si possible)
        try:
            pred_train = results.fittedvalues
            mse = mean_squared_error(data[max(p, d, q):], pred_train[max(p, d, q):])
        except Exception:
            mse = None
        # Affichage graphique
        for widget in plot_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data.index, data.values, label='Données réelles')
        ax.plot(range(len(data), len(data) + len(forecast_mean)), forecast_mean, label='Prévision', color='red')
        ax.fill_between(range(len(data), len(data) + len(forecast_mean)), conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='red', alpha=0.1)
        ax.set_title("Prévision ARIMA")
        ax.set_xlabel("Temps")
        ax.set_ylabel("Valeur")
        ax.grid(True)
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        end = time.time()
        duration = end - start
        energy = duration * 0.5
        aic = results.aic
        bic = results.bic
        metrics_text = f"Temps d'exécution: {duration:.2f}s | Énergie: {energy:.2f} kJ\nAIC: {aic:.2f} | BIC: {bic:.2f} | MSE: {mse:.4f}" if mse is not None else f"Temps d'exécution: {duration:.2f}s | Énergie: {energy:.2f} kJ\nAIC: {aic:.2f} | BIC: {bic:.2f}"
        metrics_label.configure(text=metrics_text)
        save_model_metrics("ARIMA", duration, energy)

    run_btn = ctk.CTkButton(
        data_frame,
        text="Exécuter le modèle",
        command=run_model,
        fg_color="blue",
        hover_color="darkblue"
    )
    run_btn.pack(side="left", padx=10)

    # Bouton retour
    def retour():
        on_close()

    back_btn = ctk.CTkButton(
        main_frame,
        text="Retour",
        command=retour,
        fg_color="red",
        hover_color="darkred"
    )
    back_btn.pack(pady=10)
