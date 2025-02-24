import sqlite3

class Database:
    def __init__(self, db_name="inventaire.db"):
        """ Initialise la connexion à la base de données et crée les tables si elles n'existent pas. """
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # ✅ Permet d'accéder aux résultats comme un dictionnaire
        self.cursor = self.conn.cursor()  # ✅ Ajoute self.cursor ici !
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
