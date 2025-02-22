import tkinter as tk
from tkinter import messagebox

class WarehouseGUI:
    def __init__(self, root, rows=10, cols=10):
        self.root = root
        self.root.title("Entrepôt Polybois")
        
        self.rows = rows
        self.cols = cols
        self.storage_grid = [[None for _ in range(cols)] for _ in range(rows)]
        
        self.create_widgets()
        self.create_grid()
    
    def create_widgets(self):
        title = tk.Label(self.root, text="Plan d'Entrepôt", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=self.cols, pady=10)
    
    def create_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = tk.Button(
                    self.root, 
                    text=f"{r},{c}", 
                    width=6, height=3, 
                    bg="lightgray",  # Couleur par défaut
                    command=lambda row=r, col=c: self.show_cell_info(row, col)
                )
                cell.grid(row=r+1, column=c, padx=2, pady=2)
                self.storage_grid[r][c] = cell
    
    def show_cell_info(self, row, col):
        messagebox.showinfo("Informations", f"Emplacement: {row}, {col}\nStatut: Disponible")

if __name__ == "__main__":
    root = tk.Tk()
    app = WarehouseGUI(root, rows=10, cols=10)
    root.mainloop()
