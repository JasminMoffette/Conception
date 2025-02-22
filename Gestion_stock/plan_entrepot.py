import tkinter as tk
import pandas as pd

# Charger l'Excel
df = pd.read_excel("DATA_Plan_entrepot.xlsx")

# Création de l'interface Tkinter
root = tk.Tk()
root.title("Plan de l'Entreprise - Polybois")
canvas = tk.Canvas(root, width=1600, height=800, bg="white")
canvas.pack()

# Déterminer les limites du plan
min_x = min(df["Start X"].min(), df["End X"].min(), df["Position X"].min())
max_x = max(df["Start X"].max(), df["End X"].max(), df["Position X"].max())
min_y = min(df["Start Y"].min(), df["End Y"].min(), df["Position Y"].min())
max_y = max(df["Start Y"].max(), df["End Y"].max(), df["Position Y"].max())

# Calcul de l'échelle pour adapter à la fenêtre
echelle_x = 1500 / (max_x - min_x)
echelle_y = 700 / (max_y - min_y)

def convertir_coord(x, y):
    """Convertit les coordonnées en fonction de l'échelle et centre dans le canevas."""
    new_x = (x - min_x) * echelle_x + 50
    new_y = 800 - ((y - min_y) * echelle_y + 50)
    return new_x, new_y

# Dessiner les murs
df_murs = df.dropna(subset=["Start X", "Start Y", "End X", "End Y"])
for _, row in df_murs.iterrows():
    x1, y1 = convertir_coord(row["Start X"], row["Start Y"])
    x2, y2 = convertir_coord(row["End X"], row["End Y"])
    canvas.create_line(x1, y1, x2, y2, width=7, fill="black")

# Dessiner les textes depuis l'Excel
df_textes = df.dropna(subset=["Value", "Position X", "Position Y", "Height"])
for _, row in df_textes.iterrows():
    x, y = convertir_coord(row["Position X"], row["Position Y"])
    text = row["Value"]
    size = int(row["Height"]) if not pd.isna(row["Height"]) else 12
    canvas.create_text(x, y, text=text, font=("Arial", size, "bold"), fill="blue")


root.mainloop()

