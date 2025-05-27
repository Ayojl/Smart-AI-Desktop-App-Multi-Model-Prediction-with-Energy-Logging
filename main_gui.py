import customtkinter as ctk
from regression_page import regression_page
from clustering_page import clustering_page
from arima_page import arima_page
from random_forest_page import random_forest_page
from cross_validation_page import cross_validation_page
from utils import generate_excel_report

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Application d'IA")
        self.geometry("800x600")
        self.minsize(700, 500)
        self.configure(bg="#232323")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Carte centrale avec layout grid
        self.card_frame = ctk.CTkFrame(self, corner_radius=25, fg_color="#2d2d2d")
        self.card_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        self.card_frame.grid_columnconfigure(0, weight=1)
        for i in range(8):
            self.card_frame.grid_rowconfigure(i, weight=1)

        # Titre principal
        self.title_label = ctk.CTkLabel(
            self.card_frame,
            text="Application d'Intelligence Artificielle",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=(30, 5), sticky="n")

        # Sous-titre inspirant
        self.subtitle_label = ctk.CTkLabel(
            self.card_frame,
            text="Explorez, comparez et prédisez avec l'IA moderne. Osez l'innovation !",
            font=ctk.CTkFont(size=15, weight="normal"),
            text_color="#bbbbbb"
        )
        self.subtitle_label.grid(row=1, column=0, pady=(0, 15), sticky="n")

        # Bloc de boutons (toujours dans la carte)
        self.buttons_frame = ctk.CTkFrame(self.card_frame, fg_color="#232323", corner_radius=20)
        self.buttons_frame.grid(row=2, column=0, pady=(0, 0), sticky="n")
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1)

        self.create_button("Régression", self.open_regression, "#1a1aff", "#3333ff", 0)
        self.create_button("Clustering", self.open_clustering, "#178a1a", "#24c924", 1)
        self.create_button("ARIMA", self.open_arima, "#7d1fa3", "#b266ff", 2)
        self.create_button("Random Forest", self.open_random_forest, "#ffb300", "#ffd966", 3)
        self.create_button("Cross Validation", self.open_cross_validation, "#a83232", "#ff6666", 4)

        # Espaceur flexible
        self.spacer = ctk.CTkLabel(self.card_frame, text="")
        self.spacer.grid(row=3, column=0, sticky="nswe")

        # Quit button toujours en bas de la carte
        self.quit_button = ctk.CTkButton(
            self.card_frame,
            text="Quitter l'application",
            command=self.quit_app,
            fg_color="#e53935",
            hover_color="#b71c1c",
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=15,
            width=220,
            height=38
        )
        self.quit_button.grid(row=7, column=0, pady=(10, 25), sticky="s")

    def create_button(self, text, command, color, hover, row):
        button = ctk.CTkButton(
            self.buttons_frame,
            text=text,
            command=command,
            fg_color=color,
            hover_color=hover,
            font=ctk.CTkFont(size=17, weight="bold"),
            corner_radius=15,
            width=260,
            height=45
        )
        button.grid(row=row, column=0, pady=8, padx=10, sticky="ew")

    def open_regression(self):
        regression_page(self)
    def open_clustering(self):
        clustering_page(self)
    def open_arima(self):
        arima_page(self)
    def open_random_forest(self):
        random_forest_page(self)
    def open_cross_validation(self):
        cross_validation_page(self)
    def quit_app(self):
        try:
            generate_excel_report()
            self.quit()
        except Exception as e:
            print(f"Error generating report: {e}")
            self.quit()

if __name__ == "__main__":
    app = App()
    app.mainloop()
