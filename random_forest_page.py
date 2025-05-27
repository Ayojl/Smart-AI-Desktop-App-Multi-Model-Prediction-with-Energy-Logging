import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import time
from tkinter import messagebox
from utils import save_model_metrics

data = None
X_train = None
X_test = None
y_train = None
y_test = None

def random_forest_page(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Random Forest")
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
        text="Random Forest",
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
    n_samples.insert(0, "1000")
    n_samples.pack(side="left", padx=5)

    # Number of features
    ctk.CTkLabel(params_frame, text="Nombre de variables:").pack(side="left", padx=5)
    n_features = ctk.CTkEntry(params_frame, width=100)
    n_features.insert(0, "10")
    n_features.pack(side="left", padx=5)

    # Number of trees
    ctk.CTkLabel(params_frame, text="Nombre d'arbres:").pack(side="left", padx=5)
    n_trees = ctk.CTkEntry(params_frame, width=100)
    n_trees.insert(0, "100")
    n_trees.pack(side="left", padx=5)

    def generate():
        global data, X_train, X_test, y_train, y_test
        try:
            n = int(n_samples.get())
            n_feat = int(n_features.get())
            
            # Generate synthetic classification data
            X, y = make_classification(
                n_samples=n,
                n_features=n_feat,
                n_informative=n_feat//2,
                n_redundant=n_feat//4,
                random_state=42
            )
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            data = (X, y)
            messagebox.showinfo("Succès", "Données générées")
            run_model()  # Automatically run model after generating data
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides")

    def run_model():
        global data, X_train, X_test, y_train, y_test
        if data is None:
            messagebox.showwarning("Erreur", "Générez d'abord les données")
            return

        try:
            n_estimators = int(n_trees.get())
        except ValueError:
            messagebox.showerror("Erreur", "Le nombre d'arbres doit être un entier")
            return

        start = time.time()
        
        # Train Random Forest
        rf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        rf.fit(X_train, y_train)
        
        # Get feature importances
        importances = rf.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        # Get predictions
        y_pred = rf.predict(X_test)
        accuracy = rf.score(X_test, y_test)

        # Clear previous plot
        for widget in plot_frame.winfo_children():
            widget.destroy()

        # Create new plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot feature importances
        ax1.bar(range(len(importances)), importances[indices])
        ax1.set_title("Importance des Variables")
        ax1.set_xlabel("Variables")
        ax1.set_ylabel("Importance")
        ax1.set_xticks(range(len(importances)))
        ax1.set_xticklabels([f"Var {i+1}" for i in indices], rotation=45)
        
        # Plot confusion matrix
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(y_test, y_pred)
        im = ax2.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        ax2.set_title("Matrice de Confusion")
        ax2.set_xlabel("Prédictions")
        ax2.set_ylabel("Valeurs Réelles")
        plt.colorbar(im, ax=ax2)
        
        # Add text annotations to confusion matrix
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax2.text(j, i, format(cm[i, j], 'd'),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")

        plt.tight_layout()

        # Embed plot in tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        end = time.time()
        duration = end - start
        energy = duration * 0.5
        
        # Update metrics
        metrics_text = f"Temps d'exécution: {duration:.2f}s\nÉnergie consommée: {energy:.2f} kJ\nPrécision: {accuracy:.2f}"
        metrics_label.configure(text=metrics_text)
        
        save_model_metrics("Random Forest", duration, energy)

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
