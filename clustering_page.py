import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import numpy as np
import time
from utils import save_model_metrics

data = None

def clustering_page(parent):
    window = tk.Toplevel(parent)
    window.title("Clustering (KMeans)")
    window.geometry("500x550")
    window.configure(bg="#fff3e0")

    def generate_data():
        global data
        try:
            n_clusters = int(entry_clusters.get())
            if n_clusters <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un entier positif pour les clusters.")
            return

        X, _ = make_blobs(n_samples=200, centers=n_clusters, n_features=2, random_state=42)
        data = X
        messagebox.showinfo("Succès", "Les données ont été générées.")

    def run_clustering():
        if data is None:
            messagebox.showwarning("Alerte", "Veuillez d'abord générer les données.")
            return

        try:
            n_clusters = int(entry_clusters.get())
            random_state = entry_random.get()
            random_state = int(random_state) if random_state.strip() else None
        except ValueError:
            messagebox.showerror("Erreur", "Entrée invalide pour les paramètres.")
            return

        start = time.time()
        model = KMeans(n_clusters=n_clusters, random_state=random_state)
        y_kmeans = model.fit_predict(data)
        end = time.time()

        plt.figure()
        plt.scatter(data[:, 0], data[:, 1], c=y_kmeans, cmap='viridis')
        plt.title(f"Clustering - KMeans (k={n_clusters})")
        plt.show()

        duration = end - start
        energy = duration * 0.5
        save_model_metrics(f"KMeans (k={n_clusters})", duration, energy)

        messagebox.showinfo("Terminé", f"Temps : {duration:.2f}s\nÉnergie : {energy:.2f} kJ")

    def retour():
        window.destroy()

    tk.Label(window, text="Clustering - KMeans", font=("Arial", 16, "bold"), bg="#fff3e0").pack(pady=10)

    form = tk.Frame(window, bg="#fff3e0")
    form.pack(pady=10)

    tk.Label(form, text="n_clusters :", bg="#fff3e0").grid(row=0, column=0, padx=5, pady=5)
    entry_clusters = tk.Entry(form, width=10)
    entry_clusters.insert(0, "3")
    entry_clusters.grid(row=0, column=1)

    tk.Label(form, text="random_state :", bg="#fff3e0").grid(row=1, column=0, padx=5, pady=5)
    entry_random = tk.Entry(form, width=10)
    entry_random.insert(0, "42")
    entry_random.grid(row=1, column=1)

    tk.Button(window, text="Générer les données", command=generate_data,
              bg="#66bb6a", fg="white", font=("Arial", 12), width=30).pack(pady=10)

    tk.Button(window, text="Lancer Clustering", command=run_clustering,
              bg="#42a5f5", fg="white", font=("Arial", 12), width=30).pack(pady=10)

    tk.Button(window, text="Retour", command=retour,
              bg="#ef5350", fg="white", font=("Arial", 12), width=30).pack(pady=10)
