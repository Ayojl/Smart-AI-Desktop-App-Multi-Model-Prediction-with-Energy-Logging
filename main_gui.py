import tkinter as tk
from regression_page import regression_page
from clustering_page import clustering_page
from arima_page import arima_page
from random_forest_page import random_forest_page
from cross_validation_page import cross_validation_page
from utils import export_metrics_to_excel
from tkinter import messagebox

def quitter_application(root):
    export_metrics_to_excel()
    messagebox.showinfo("Fin", "Les résultats ont été enregistrés dans metrics.xlsx")
    root.destroy()

def main_window():
    root = tk.Tk()
    root.title("Smart IA - Modèles")
    root.geometry("700x550")
    root.configure(bg="#e0f7fa")

    tk.Label(root, text="Choisissez un modèle IA", font=("Arial", 18, "bold"), bg="#e0f7fa", fg="#003366").pack(pady=30)
    frame = tk.Frame(root, bg="#e0f7fa")
    frame.pack()

    tk.Button(frame, text="Régression Linéaire", width=25, height=2, bg="#cce5ff",
              command=lambda: regression_page(root)).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(frame, text="Clustering", width=25, height=2, bg="#cce5ff",
              command=lambda: clustering_page(root)).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(frame, text="ARIMA", width=25, height=2, bg="#cce5ff",
              command=lambda: arima_page(root)).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(frame, text="Random Forest", width=25, height=2, bg="#cce5ff",
              command=lambda: random_forest_page(root)).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(frame, text="Validation Croisée", width=25, height=2, bg="#cce5ff",
              command=lambda: cross_validation_page(root)).grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(root, text="❌ Quitter l'application", command=lambda: quitter_application(root),
              bg="#ef5350", fg="white", font=("Arial", 12), width=30, height=2).pack(pady=30)
    
    

    root.mainloop()
