import tkinter as tk
from tkinter import Toplevel
import pandas as pd
import os
from config import Config  # Import de la configuration

# Construire le chemin complet vers le fichier Excel en utilisant Config.DATA_FOLDER
data_file_path = os.path.join(Config.DATA_FOLDER, 'DATA_Plan_entrepot.xlsx')

# Charger le plan global depuis la feuille "plan"
try:
    df_plan = pd.read_excel(data_file_path, sheet_name="plan")
except Exception as e:
    print(f"Erreur lors du chargement du plan global : {e}")
    df_plan = None

class EmplacementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plan de l'Entreprise - Polybois")
        self.root.geometry("1600x800")
        
        self.canvas = tk.Canvas(self.root, width=1600, height=800, bg="white")
        self.canvas.pack()
        
        # Vérifier si le plan a bien été chargé
        if df_plan is not None:
            self.draw_plan()
            self.draw_walls()
        else:
            tk.Label(self.root, text="Plan global non disponible", font=("Arial", 16)).pack(pady=20)
    
    def draw_plan(self):
        """Affiche le plan global avec les noms d'entrepôts interactifs."""
        # On s'assure que df_plan n'est pas vide et contient les colonnes nécessaires
        if df_plan is None:
            return
        for _, row in df_plan.dropna(subset=["Value", "Position X", "Position Y"]).iterrows():
            x, y = row["Position X"], row["Position Y"]
            name = row["Value"]
            # Inverser la coordonnée Y pour correspondre à l'affichage (si c'est le besoin)
            text_id = self.canvas.create_text(x, 800 - y, text=name, font=("Arial", 16, "bold"), fill="blue")
            # Liaison du clic pour ouvrir l'entrepôt correspondant
            self.canvas.tag_bind(text_id, "<Button-1>", lambda event, n=name: self.open_entrepot(n))
    
    def draw_walls(self):
        """Dessine les murs du plan global."""
        if df_plan is None:
            return
        # Filtrer pour obtenir les lignes définissant les murs
        df_murs = df_plan.dropna(subset=["Start X", "Start Y", "End X", "End Y"])
        for _, row in df_murs.iterrows():
            x1, y1 = row["Start X"], row["Start Y"]
            x2, y2 = row["End X"], row["End Y"]
            self.canvas.create_line(x1, 800 - y1, x2, 800 - y2, width=3, fill="black")
    
    def open_entrepot(self, name):
        """Ouvre une nouvelle fenêtre représentant le plan intérieur de l'entrepôt sélectionné."""
        new_window = Toplevel(self.root)
        new_window.title(f"Plan intérieur de {name}")
        new_window.geometry("1600x1000")
        
        label = tk.Label(new_window, text=f"Entrepôt {name}", font=("Arial", 18, "bold"))
        label.pack(pady=20)
        
        canvas = tk.Canvas(new_window, width=1600, height=800, bg="lightgrey")
        canvas.pack()
        
        # Utiliser le même chemin absolu pour charger le fichier Excel
        try:
            # On construit le nom de la feuille à partir du nom de l'entrepôt (à adapter selon ton mapping)
            feuille = name.lower().replace(" ", "_")
            df_interieur = pd.read_excel(data_file_path, sheet_name=feuille)
            for _, row in df_interieur.dropna(subset=["Value", "Position X", "Position Y"]).iterrows():
                x, y = row["Position X"], row["Position Y"]
                item_name = row["Value"]
                canvas.create_text(x, 800 - y, text=item_name, font=("Arial", 14, "bold"), fill="green")
            # Dessiner les murs internes, s'ils sont définis
            df_murs_int = df_interieur.dropna(subset=["Start X", "Start Y", "End X", "End Y"])
            for _, row in df_murs_int.iterrows():
                x1, y1 = row["Start X"], row["Start Y"]
                x2, y2 = row["End X"], row["End Y"]
                canvas.create_line(x1, 800 - y1, x2, 800 - y2, width=3, fill="black")
        except Exception as e:
            tk.Label(new_window, text="Aucun plan disponible pour cet entrepôt.", font=("Arial", 14)).pack(pady=20)
            print(e)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmplacementApp(root)
    root.mainloop()
