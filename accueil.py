import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import main_gui
import os
import sys

def open_main():
    root.destroy()
    main_gui.main_gui()

def show_about():
    messagebox.showinfo(" À propos ", "Projet réalisé par Ayoub Ouijili \n Encadrant : Dr. EL MKHALET MOUNA\n Année : 2024-2025")
    
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # dossier temporaire PyInstaller
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Fenêtre principale
root = tk.Tk()
root.title("Application Smart IA")
root.geometry("800x500")
root.configure(bg="#f5f5f5")

# Charger et afficher le logo
try:
    logo_image = Image.open(resource_path("logo.png"))
    logo_resized = logo_image.resize((60, 60), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_resized)
    logo_label = ttk.Label(root, image=logo_photo, background="#f5f5f5")
    logo_label.image = logo_photo
    logo_label.pack(pady=(20, 10))
except:
    ttk.Label(root, text="LOGO", font=("Segoe UI", 14), background="#f5f5f5").pack(pady=(20, 10))

# Titre
ttk.Label(root, text="Smart IA Desktop App", font=("Segoe UI", 20, "bold"), background="#f5f5f5", foreground="#1a237e").pack(pady=(10, 20))

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("Accent.TButton", background="#4CAF50", foreground="white", font=("Segoe UI", 12))
style.map("Accent.TButton", background=[("active", "#45A049")])
style.configure("Danger.TButton", background="#f44336", foreground="white", font=("Segoe UI", 12))
style.map("Danger.TButton", background=[("active", "#d32f2f")])
style.configure("Neutral.TButton", background="#607d8b", foreground="white", font=("Segoe UI", 12))
style.map("Neutral.TButton", background=[("active", "#455a64")])

# Boutons
ttk.Button(root, text="🚀 Lancer l'application", command=open_main, style="Accent.TButton", width=30).pack(pady=10)
ttk.Button(root, text="ℹ️ À propos", command=show_about, style="Neutral.TButton", width=30).pack(pady=5)
ttk.Button(root, text="❌ Quitter", command=root.quit, style="Danger.TButton", width=30).pack(pady=20)

root.mainloop()
