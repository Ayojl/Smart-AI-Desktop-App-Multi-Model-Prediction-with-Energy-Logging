import tkinter as tk
from tkinter import messagebox
from regression_page import regression_page
from clustering_page import clustering_page
from arima_page import arima_page
from random_forest_page import random_forest_page
from cross_validation_page import cross_validation_page
from utils import export_metrics_to_excel

def quitter_application(root):
    export_metrics_to_excel()
    messagebox.showinfo("Fin", "Les résultats ont été enregistrés dans metrics.xlsx")
    root.destroy()

def main_gui():
    root = tk.Tk()
    root.title("Smart IA - Modèles d'Intelligence Artificielle")
    root.geometry("600x600")
    root.configure(bg="#f5f5f5")

    tk.Label(root, text="Smart IA - Choisissez un Modèle",
             font=("Arial", 18, "bold"), bg="#f5f5f5").pack(pady=20)

    # Régression
    tk.Button(root, text="Régression Linéaire",
              command=lambda: regression_page(root),
              bg="#42a5f5", fg="white", font=("Arial", 12), width=30, height=2).pack(pady=5)

    # Clustering
    tk.Button(root, text="Clustering",
              command=lambda: clustering_page(root),
              bg="#8e24aa", fg="white", font=("Arial", 12), width=30, height=2).pack(pady=5)

    # ARIMA
    tk.Button(root, text="ARIMA",
              command=lambda: arima_page(root),
              bg="#ffb300", fg="black", font=("Arial", 12), width=30, height=2).pack(pady=5)

    # Random Forest
    tk.Button(root, text="Random Forest",
              command=lambda: random_forest_page(root),
              bg="#388e3c", fg="white", font=("Arial", 12), width=30, height=2).pack(pady=5)

    # Cross-Validation
    tk.Button(root, text="Validation Croisée",
              command=lambda: cross_validation_page(root),
              bg="#5d4037", fg="white", font=("Arial", 12), width=30, height=2).pack(pady=5)

    # Quitter
    tk.Button(root, text="Quitter l'application",
              command=lambda: quitter_application(root),
              bg="#d32f2f", fg="white", font=("Arial", 12), width=30, height=2).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
