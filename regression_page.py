import customtkinter as ctk
from data_generator import generate_data
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from tkinter import messagebox
from utils import save_model_metrics

data = None

def regression_page(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Régression Linéaire")
    window.geometry("1000x800")
    window.transient(parent)
    window.grab_set()
    def on_close():
        window.destroy()
    window.protocol("WM_DELETE_WINDOW", on_close)
    
    # Create main frame
    main_frame = ctk.CTkFrame(window)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Title
    title_label = ctk.CTkLabel(
        main_frame,
        text="Régression Linéaire",
        font=ctk.CTkFont(size=24, weight="bold")
    )
    title_label.pack(pady=20)

    # Create frames for controls and plot
    controls_frame = ctk.CTkFrame(main_frame)
    controls_frame.pack(pady=10, padx=20, fill="x")
    
    plot_frame = ctk.CTkFrame(main_frame)
    plot_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Data generation parameters
    params_frame = ctk.CTkFrame(controls_frame)
    params_frame.pack(pady=10, padx=10, fill="x")

    # Number of points
    ctk.CTkLabel(params_frame, text="Nombre de points:").pack(side="left", padx=5)
    n_points = ctk.CTkEntry(params_frame, width=100)
    n_points.insert(0, "100")
    n_points.pack(side="left", padx=5)

    # Noise level
    ctk.CTkLabel(params_frame, text="Niveau de bruit:").pack(side="left", padx=5)
    noise = ctk.CTkEntry(params_frame, width=100)
    noise.insert(0, "0.1")
    noise.pack(side="left", padx=5)

    # Slope
    ctk.CTkLabel(params_frame, text="Pente:").pack(side="left", padx=5)
    slope = ctk.CTkEntry(params_frame, width=100)
    slope.insert(0, "2.0")
    slope.pack(side="left", padx=5)

    def generate():
        global data
        try:
            n = int(n_points.get())
            noise_level = float(noise.get())
            slope_value = float(slope.get())
            data = generate_data(n_points=n, noise=noise_level, slope=slope_value)
            messagebox.showinfo("Succès", "Données générées")
            run_model()  # Automatically run model after generating data
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides")

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

        # Clear previous plot
        for widget in plot_frame.winfo_children():
            widget.destroy()

        # Create new plot
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(X, y, label='Données')
        ax.plot(X, y_pred, color='red', label='Régression')
        ax.set_title("Régression Linéaire")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)
        ax.legend()

        # Embed plot in tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        end = time.time()
        duration = end - start
        energy = duration * 0.5

        # Update metrics
        metrics_text = f"Temps d'exécution: {duration:.2f}s\nÉnergie consommée: {energy:.2f} kJ\nPente estimée: {theta[1]:.2f}\nOrdonnée à l'origine: {theta[0]:.2f}"
        metrics_label.configure(text=metrics_text)
        
        save_model_metrics("Régression Linéaire", duration, energy)

    # Buttons frame
    button_frame = ctk.CTkFrame(controls_frame)
    button_frame.pack(pady=10, padx=10, fill="x")

    generate_btn = ctk.CTkButton(
        button_frame,
        text="Générer des données",
        command=generate,
        fg_color="green",
        hover_color="darkgreen"
    )
    generate_btn.pack(side="left", padx=5)

    run_btn = ctk.CTkButton(
        button_frame,
        text="Exécuter le modèle",
        command=run_model,
        fg_color="blue",
        hover_color="darkblue"
    )
    run_btn.pack(side="left", padx=5)

    # Metrics display
    metrics_label = ctk.CTkLabel(
        controls_frame,
        text="",
        font=ctk.CTkFont(size=12)
    )
    metrics_label.pack(pady=10)

    def retour():
        on_close()

    # Back button
    back_btn = ctk.CTkButton(
        main_frame,
        text="Retour",
        command=retour,
        fg_color="red",
        hover_color="darkred"
    )
    back_btn.pack(pady=10)
