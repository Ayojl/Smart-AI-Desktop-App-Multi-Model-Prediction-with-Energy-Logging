import tkinter as tk
from tkinter import ttk, messagebox
from data_generator import generate_data
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from utils import save_model_metrics
import time
import numpy as np
import pandas as pd

data = None

def cross_validation_page(parent):
    window = tk.Toplevel(parent)
    window.title("Cross-Validation")
    window.geometry("500x500")
    window.configure(bg="#e0f7fa")

    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(),
        "Random Forest": RandomForestRegressor(),
        "Support Vector Regressor": SVR()
    }

    selected_model = tk.StringVar()
    selected_model.set("Linear Regression")

    def generate():
        global data
        data = generate_data()
        messagebox.showinfo("Data Generated", "Synthetic data has been generated.")

    def run_model():
        global data
        if data is None:
            messagebox.showwarning("Error", "Please generate data first.")
            return

        model_name = selected_model.get()
        model = models[model_name]

        start = time.time()
        X = data[['X1', 'X2', 'X3']]
        y = data['Y']
        scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
        mse_scores = -scores
        mse = mse_scores.mean()
        end = time.time()

        duration = end - start
        energy = duration * 0.5

        save_model_metrics(f"Cross-Validation - {model_name}", duration, energy)

        messagebox.showinfo(
            "Results",
            f"Model: {model_name}\nMSE Scores: {np.round(mse_scores, 4)}\n\nAverage MSE: {mse:.4f}\n\n"
            f"Execution Time: {duration:.2f}s\nEstimated Energy: {energy:.2f} kJ"
        )

    def retour():
        window.destroy()

    tk.Label(window, text="Cross-Validation", font=("Arial", 18, "bold"), bg="#e0f7fa").pack(pady=10)

    tk.Button(window, text="Generate Data", command=generate,
              bg="#66bb6a", fg="white", font=("Arial", 12), width=30).pack(pady=10)

    tk.Label(window, text="Choose a model to evaluate:", bg="#e0f7fa", font=("Arial", 12)).pack(pady=5)

    combo = ttk.Combobox(window, textvariable=selected_model, values=list(models.keys()), state="readonly", width=30)
    combo.pack(pady=5)

    tk.Button(window, text="Run Cross-Validation", command=run_model,
              bg="#42a5f5", fg="white", font=("Arial", 12), width=30).pack(pady=10)

    tk.Button(window, text="Back", command=retour,
              bg="#ef5350", fg="white", font=("Arial", 12), width=30).pack(pady=10)
