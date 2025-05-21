import tkinter as tk
from tkinter import messagebox
from sklearn.ensemble import RandomForestRegressor
from data_generator import generate_data
from utils import save_model_metrics
import time
import matplotlib.pyplot as plt

data = None

def random_forest_page(parent):
    window = tk.Toplevel(parent)
    window.title("Random Forest")
    window.geometry("500x600")
    window.configure(bg="#f1f8e9")

    global data

    def generate():
        global data
        data = generate_data()
        messagebox.showinfo("Success", "Synthetic data has been generated.")

    def run_rf():
        if data is None:
            messagebox.showwarning("No Data", "Please generate data first.")
            return

        try:
            n_estimators = int(entry_estimators.get())
            max_depth = entry_depth.get()
            max_depth = int(max_depth) if max_depth.strip() else None
            random_state = entry_random.get()
            random_state = int(random_state) if random_state.strip() else None
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integer values.")
            return

        start = time.time()
        X = data[['X1', 'X2', 'X3']]
        y = data['Y']
        model = RandomForestRegressor(n_estimators=n_estimators,
                                      max_depth=max_depth,
                                      random_state=random_state)
        model.fit(X, y)
        predictions = model.predict(X)
        end = time.time()

        plt.figure()
        plt.plot(y.values, label="True")
        plt.plot(predictions, label="Predicted", linestyle='dashed')
        plt.title("Random Forest Regression")
        plt.legend()
        plt.show()

        duration = end - start
        energy = duration * 0.5
        save_model_metrics("Random Forest", duration, energy)
        messagebox.showinfo("Finished", f"Time: {duration:.2f}s\nEnergy: {energy:.2f} kJ")

    def retour():
        window.destroy()

    tk.Label(window, text="Random Forest Parameters", font=("Arial", 16, "bold"), bg="#f1f8e9").pack(pady=10)

    form = tk.Frame(window, bg="#f1f8e9")
    form.pack(pady=10)

    tk.Label(form, text="n_estimators:", bg="#f1f8e9").grid(row=0, column=0, padx=5, pady=5)
    entry_estimators = tk.Entry(form, width=10)
    entry_estimators.insert(0, "100")
    entry_estimators.grid(row=0, column=1)

    tk.Label(form, text="max_depth:", bg="#f1f8e9").grid(row=1, column=0, padx=5, pady=5)
    entry_depth = tk.Entry(form, width=10)
    entry_depth.insert(0, "5")
    entry_depth.grid(row=1, column=1)

    tk.Label(form, text="random_state:", bg="#f1f8e9").grid(row=2, column=0, padx=5, pady=5)
    entry_random = tk.Entry(form, width=10)
    entry_random.insert(0, "42")
    entry_random.grid(row=2, column=1)

    tk.Button(window, text="Generate Data", command=generate,
              bg="#66bb6a", fg="white", font=("Arial", 12), width=30).pack(pady=10)

    tk.Button(window, text="Run Random Forest", command=run_rf,
              bg="#42a5f5", fg="white", font=("Arial", 12), width=30).pack(pady=10)

    tk.Button(window, text="Back", command=retour,
              bg="#ef5350", fg="white", font=("Arial", 12), width=30).pack(pady=10)
