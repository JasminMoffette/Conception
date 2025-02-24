import sqlite3

class Database:
    def __init__(self, db_name="inventaire.db"):
        """ Initialise la connexion à la base de données et crée les tables si elles n'existent pas. """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
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
        self.conn.commit()

    def fermer_connexion(self):
        """ Ferme la connexion à la base de données. """
        self.conn.close()
