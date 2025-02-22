import tkinter as tk
from tkinter import Toplevel
import pandas as pd

# Charger les données du plan d'entreprise
df = pd.read_excel("DATA_Plan_entrepot.xlsx")

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
        """Affiche le plan avec les noms d'entrepôts interactifs."""
        for _, row in df.dropna(subset=["Value", "Position X", "Position Y"]).iterrows():
            x, y = row["Position X"], row["Position Y"]
            name = row["Value"]
            text_id = self.canvas.create_text(x, 800 - y, text=name, font=("Arial", 16, "bold"), fill="blue")
            self.canvas.tag_bind(text_id, "<Button-1>", lambda event, n=name: self.open_entrepot(n))
    
    def draw_walls(self):
        """Dessine les murs de l'entrepôt sur le canevas."""
        df_murs = df.dropna(subset=["Start X", "Start Y", "End X", "End Y"])
        for _, row in df_murs.iterrows():
            x1, y1 = row["Start X"], row["Start Y"]
            x2, y2 = row["End X"], row["End Y"]
            self.canvas.create_line(x1, 800 - y1, x2, 800 - y2, width=3, fill="black")
    
    def open_entrepot(self, name):
        """Ouvre une nouvelle fenêtre représentant l'intérieur de l'entrepôt sélectionné."""
        new_window = Toplevel(self.root)
        new_window.title(f"{name}")
        new_window.geometry("800x600")
        
        label = tk.Label(new_window, text=f"Entrepot {name}", font=("Arial", 18, "bold"))
        label.pack(pady=20)
        
        canvas = tk.Canvas(new_window, width=800, height=500, bg="lightgrey")
        canvas.pack()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = EmplacementApp(root)
    root.mainloop()
