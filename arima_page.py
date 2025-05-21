import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import time
from utils import save_model_metrics

data = None

def generate_arima_data():
    np.random.seed(42)
    data = pd.Series(np.random.randn(100).cumsum())
    return data

def arima_page(parent):
    window = tk.Toplevel(parent)
    window.title("ARIMA Model")
    window.geometry("500x600")
    window.configure(bg="#f0f8ff")

    global data
    data = generate_arima_data()

    def run_arima():
        try:
            p = int(entry_p.get())
            d = int(entry_d.get())
            q = int(entry_q.get())
            if not (0 <= p <= 2 and 0 <= d <= 2 and 0 <= q <= 2):
                raise ValueError("p, d, and q must be between 0 and 2")
        except ValueError as ve:
            messagebox.showerror("Invalid Input", str(ve))
            return

        start = time.time()
        model = ARIMA(data, order=(p, d, q))
        model_fit = model.fit()
        end = time.time()

        prediction = model_fit.predict(start=0, end=len(data)-1)

        plt.figure()
        plt.plot(data, label="Original")
        plt.plot(prediction, label="Predicted", linestyle='dashed')
        plt.title(f"ARIMA({p},{d},{q}) Forecast")
        plt.legend()
        plt.show()

        duration = end - start
        energy = duration * 0.5

        save_model_metrics(f"ARIMA({p},{d},{q})", duration, energy)
        messagebox.showinfo("ARIMA Executed", f"Execution Time: {duration:.2f}s\nEstimated Energy: {energy:.2f} kJ")

    def retour():
        window.destroy()

    tk.Label(window, text="ARIMA Model (p, d, q)", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=10)

    frame = tk.Frame(window, bg="#f0f8ff")
    frame.pack(pady=10)

    tk.Label(frame, text="p (0-2):", bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
    entry_p = tk.Entry(frame, width=5)
    entry_p.grid(row=0, column=1)

    tk.Label(frame, text="d (0-2):", bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5)
    entry_d = tk.Entry(frame, width=5)
    entry_d.grid(row=1, column=1)

    tk.Label(frame, text="q (0-2):", bg="#f0f8ff").grid(row=2, column=0, padx=5, pady=5)
    entry_q = tk.Entry(frame, width=5)
    entry_q.grid(row=2, column=1)

    tk.Button(window, text="Run ARIMA", command=run_arima,
              bg="#1e88e5", fg="white", font=("Arial", 12), width=30).pack(pady=15)

    tk.Button(window, text="Back", command=retour,
              bg="#ef5350", fg="white", font=("Arial", 12), width=30).pack(pady=5)
