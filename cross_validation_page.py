import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from data_generator import generate_data
from utils import save_model_metrics
import time


def cross_validation_page(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Cross Validation - Comparaison des modèles")
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
        text="Validation croisée - Comparaison automatique des modèles",
        font=ctk.CTkFont(size=24, weight="bold")
    )
    title_label.pack(pady=(10, 5))

    help_label = ctk.CTkLabel(
        main_frame,
        text="Cette page compare automatiquement les modèles sur les mêmes données (régression linéaire, arbre de décision, random forest, SVM). Les scores MSE sont affichés pour chaque modèle.",
        font=ctk.CTkFont(size=14),
        wraplength=900,
        justify="center"
    )
    help_label.pack(pady=(0, 15))

    # Frame de contrôle
    controls_frame = ctk.CTkFrame(main_frame)
    controls_frame.pack(pady=10, padx=10, fill="x")

    ctk.CTkLabel(controls_frame, text="Nombre de points :").pack(side="left", padx=5)
    n_points = ctk.CTkEntry(controls_frame, width=80)
    n_points.insert(0, "100")
    n_points.pack(side="left", padx=5)

    ctk.CTkLabel(controls_frame, text="Niveau de bruit :").pack(side="left", padx=5)
    noise = ctk.CTkEntry(controls_frame, width=80)
    noise.insert(0, "0.1")
    noise.pack(side="left", padx=5)

    # Résultats
    results_frame = ctk.CTkFrame(main_frame)
    results_frame.pack(pady=10, padx=10, fill="x")
    results_label = ctk.CTkLabel(results_frame, text="", font=ctk.CTkFont(size=13))
    results_label.pack(pady=5)

    # Zone de graphique
    plot_frame = ctk.CTkFrame(main_frame)
    plot_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def run_comparison():
        # Générer les données
        try:
            n = int(n_points.get())
            noise_level = float(noise.get())
        except Exception:
            results_label.configure(text="Paramètres invalides.")
            return
        data = generate_data(n_points=n, noise=noise_level, slope=2.0)
        X = data[['X1']].values
        y = data['Y'].values
        models = {
            "Régression Linéaire": LinearRegression(),
            "Arbre de Décision": DecisionTreeRegressor(),
            "Random Forest": RandomForestRegressor(),
            "SVM": SVR()
        }
        mse_scores = {}
        durations = {}
        energies = {}
        for name, model in models.items():
            start = time.time()
            scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
            mse = -scores.mean()
            end = time.time()
            duration = end - start
            energy = duration * 0.5
            mse_scores[name] = mse
            durations[name] = duration
            energies[name] = energy
            save_model_metrics(f"CrossVal - {name}", duration, energy)
        # Affichage tableau
        table = "Modèle\t\tMSE\n" + "\n".join([f"{k:<18} {v:.4f}" for k, v in mse_scores.items()])
        results_label.configure(text=table)
        # Affichage graphique
        for widget in plot_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(list(mse_scores.keys()), list(mse_scores.values()), color=['blue', 'green', 'orange', 'purple'])
        ax.set_title("Comparaison des modèles (MSE, plus bas = meilleur)")
        ax.set_ylabel("MSE")
        ax.grid(True, axis='y')
        for i, v in enumerate(mse_scores.values()):
            ax.text(i, v, f"{v:.2f}", ha='center', va='bottom', fontweight='bold')
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    run_btn = ctk.CTkButton(
        controls_frame,
        text="Lancer la comparaison",
        command=run_comparison,
        fg_color="brown",
        hover_color="darkred"
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
