import sqlite3
import pandas as pd
import os

DB_PATH = "aria.db"

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS etudiants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_soumission TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            pays TEXT, ville TEXT, universite TEXT, filiere TEXT,
            niveau TEXT, genre TEXT, age INTEGER,
            moyenne_generale REAL, heures_etude REAL,
            acces_internet INTEGER, charge_familiale INTEGER,
            pression_financiere INTEGER, barriere_linguistique INTEGER,
            coupures_electricite INTEGER, temps_transport REAL,
            niveau_stress INTEGER, confiance_soi INTEGER,
            sentiment_appartenance INTEGER, qualite_sommeil INTEGER,
            statut TEXT
        )
    ''')
    conn.commit()
    conn.close()

def inserer_etudiant(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO etudiants (
            pays, ville, universite, filiere, niveau, genre, age,
            moyenne_generale, heures_etude, acces_internet,
            charge_familiale, pression_financiere, barriere_linguistique,
            coupures_electricite, temps_transport, niveau_stress,
            confiance_soi, sentiment_appartenance, qualite_sommeil, statut
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        str(data['pays']), str(data['ville']), str(data['universite']),
        str(data['filiere']), str(data['niveau']), str(data['genre']),
        int(data['age']), float(data['moyenne_generale']),
        float(data['heures_etude']), int(data['acces_internet']),
        int(data['charge_familiale']), int(data['pression_financiere']),
        int(data['barriere_linguistique']), int(data['coupures_electricite']),
        float(data['temps_transport']), int(data['niveau_stress']),
        int(data['confiance_soi']), int(data['sentiment_appartenance']),
        int(data['qualite_sommeil']), str(data['statut'])
    ))
    conn.commit()
    conn.close()

def charger_donnees():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM etudiants", conn)
    conn.close()
    return df  # ← indenté correctement

def compter_etudiants():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM etudiants")
    count = cursor.fetchone()[0]
    conn.close()
    return count  # ← indenté correctement