import tkinter as tk
from tkinter import Toplevel
import pandas as pd

# Charger le plan global depuis la feuille "plan"
df_plan = pd.read_excel("DATA_Plan_entrepot.xlsx", sheet_name="plan")

class EmplacementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plan de l'Entreprise - Polybois")
        self.root.geometry("1600x800")
        
        self.canvas = tk.Canvas(self.root, width=1600, height=800, bg="white")
        self.canvas.pack()
        
        self.draw_plan()
        self.draw_walls()
    
    def draw_plan(self):
        """Affiche le plan global avec les noms d'entrepôts interactifs."""
        for _, row in df_plan.dropna(subset=["Value", "Position X", "Position Y"]).iterrows():
            x, y = row["Position X"], row["Position Y"]
            name = row["Value"]
            text_id = self.canvas.create_text(x, 800 - y, text=name, font=("Arial", 16, "bold"), fill="blue")
            # Lors d'un clic, on ouvre l'entrepôt correspondant
            self.canvas.tag_bind(text_id, "<Button-1>", lambda event, n=name: self.open_entrepot(n))
    
    def draw_walls(self):
        """Dessine les murs du plan global."""
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
        
        # Ici, on détermine le nom de la feuille à charger.
        # Par exemple, si l'entrepôt s'appelle "Entrepôt A", on charge la feuille "entrepot_A"
        feuille = name.lower().replace(" ", "_")  # adapte si besoin le mapping des noms
        
        try:
            df_interieur = pd.read_excel("DATA_Plan_entrepot.xlsx", sheet_name=feuille)
            # Afficher les éléments (noms et emplacements) du plan intérieur
            for _, row in df_interieur.dropna(subset=["Value", "Position X", "Position Y"]).iterrows():
                x, y = row["Position X"], row["Position Y"]
                item_name = row["Value"]
                canvas.create_text(x, 800 - y, text=item_name, font=("Arial", 14, "bold"), fill="green")
            # Dessiner également les murs internes, s'ils sont définis
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
