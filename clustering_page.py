import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import time
from tkinter import messagebox
from utils import save_model_metrics

data = None
clusters = None

def clustering_page(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Clustering")
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
        text="Clustering K-Means",
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

    # Number of samples
    ctk.CTkLabel(params_frame, text="Nombre d'échantillons:").pack(side="left", padx=5)
    n_samples = ctk.CTkEntry(params_frame, width=100)
    n_samples.insert(0, "300")
    n_samples.pack(side="left", padx=5)

    # Number of clusters
    ctk.CTkLabel(params_frame, text="Nombre de clusters:").pack(side="left", padx=5)
    n_clusters = ctk.CTkEntry(params_frame, width=100)
    n_clusters.insert(0, "3")
    n_clusters.pack(side="left", padx=5)

    # Cluster standard deviation
    ctk.CTkLabel(params_frame, text="Écart-type des clusters:").pack(side="left", padx=5)
    cluster_std = ctk.CTkEntry(params_frame, width=100)
    cluster_std.insert(0, "1.0")
    cluster_std.pack(side="left", padx=5)

    def generate():
        global data
        try:
            n = int(n_samples.get())
            k = int(n_clusters.get())
            std = float(cluster_std.get())
            
            # Generate synthetic data
            data, _ = make_blobs(
                n_samples=n,
                centers=k,
                cluster_std=std,
                random_state=42
            )
            messagebox.showinfo("Succès", "Données générées")
            run_model()  # Automatically run model after generating data
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides")

    def run_model():
        global data, clusters
        if data is None:
            messagebox.showwarning("Erreur", "Générez d'abord les données")
            return

        start = time.time()
        k = int(n_clusters.get())
        
        # Perform clustering
        kmeans = KMeans(n_clusters=k, random_state=42)
        clusters = kmeans.fit_predict(data)

        # Clear previous plot
        for widget in plot_frame.winfo_children():
            widget.destroy()

        # Create new plot
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = ax.scatter(data[:, 0], data[:, 1], c=clusters, cmap='viridis')
        ax.set_title("Clustering K-Means")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)
        
        # Add legend
        legend1 = ax.legend(*scatter.legend_elements(),
                          title="Clusters")
        ax.add_artist(legend1)

        # Embed plot in tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        end = time.time()
        duration = end - start
        energy = duration * 0.5

        # Calculate metrics
        inertia = kmeans.inertia_
        
        # Update metrics
        metrics_text = f"Temps d'exécution: {duration:.2f}s\nÉnergie consommée: {energy:.2f} kJ\nInertie: {inertia:.2f}"
        metrics_label.configure(text=metrics_text)
        
        save_model_metrics("Clustering", duration, energy)

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
