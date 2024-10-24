import sqlite3

# Connexion à la base de données (ou création de la base de données si elle n'existe pas)
connexion = sqlite3.connect('bdd.db')
curseur = connexion.cursor()

# Création de la table "User"
curseur.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')
# Création de la table "Animaux"
curseur.execute('''
    CREATE TABLE IF NOT EXISTS Animaux (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    race TEXT NOT NULL,
    age INTEGER NOT NULL,
    description TEXT NOT NULL,
    soin TEXT,
    soigneur TEXT NOT NULL
    )
''')

# Validation des changements et fermeture de la connexion
connexion.commit()
connexion.close()

print("Base de données et table créées avec succès.")
