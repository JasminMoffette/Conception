import sqlite3
import os
from config import Config

class Database:
    def __init__(self, db_name=None):
        # Si aucun nom de fichier n'est fourni, on utilise celui défini dans la config
        if db_name is None:
            # S'assurer que le dossier instance existe
            os.makedirs(Config.INSTANCE_FOLDER, exist_ok=True)
            db_name = os.path.join(Config.INSTANCE_FOLDER, "inventaire.db")
        
        # Initialisation de la connexion à la base de données
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Accès aux résultats comme un dictionnaire
        self.cursor = self.conn.cursor()      # Création du curseur
        self.creer_tables()

    def creer_tables(self):
        """ Crée les tables nécessaires à l'application si elles n'existent pas déjà. """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produits (
                code TEXT PRIMARY KEY,
                description TEXT,
                materiaux TEXT,
                categorie TEXT,
                statut TEXT,            
                po TEXT,
                emplacement TEXT,
                dimension TEXT,
                projet TEXT,
                quantite INTEGER,
                cp TEXT,
                fournisseur TEXT,
                coupe TEXT,
                no_catalogue TEXT,
                fsc TEXT,
                historique TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projet_produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_produit TEXT,
                projet TEXT,
                quantite INTEGER,
                FOREIGN KEY (code_produit) REFERENCES produits (code)
            )
        ''')
        self.conn.commit()

    def fermer_connexion(self):
        """ Ferme la connexion à la base de données. """
        self.conn.close()
