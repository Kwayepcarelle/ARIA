import sqlite3
import random
from modules.database import init_database, DB_PATH

def generer_donnees_demo():
    init_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM etudiants")
    if cursor.fetchone()[0] > 0:
        print("Données déjà présentes.")
        conn.close()
        return

    pays_villes = {
        "Cameroun": ["Yaoundé", "Douala", "Bafoussam"],
        "Côte d'Ivoire": ["Abidjan", "Bouaké", "Yamoussoukro"],
        "Sénégal": ["Dakar", "Thiès", "Saint-Louis"],
        "Mali": ["Bamako", "Sikasso", "Mopti"],
        "Burkina Faso": ["Ouagadougou", "Bobo-Dioulasso"],
        "Guinée": ["Conakry", "Kankan"],
        "Gabon": ["Libreville", "Port-Gentil"],
        "Togo": ["Lomé", "Sokodé"]
    }

    universites = [
        "Université de Yaoundé I",
        "Université de Douala",
        "Université Félix Houphouët-Boigny",
        "Université Cheikh Anta Diop",
        "Université de Bamako",
        "Université de Ouagadougou",
        "Université de Conakry",
        "Université Omar Bongo"
    ]

    filieres = [
        "Informatique", "Mathématiques", "Physique",
        "Économie", "Droit", "Médecine",
        "Lettres Modernes", "Géographie"
    ]

    niveaux = [
        "Licence 1", "Licence 2", "Licence 3",
        "Master 1", "Master 2"
    ]

    genres = ["Femme", "Homme"]

    statuts = ["En réussite", "En difficulté", "À risque de décrochage"]

    random.seed(42)
    etudiants = []

    for _ in range(150):
        pays = random.choice(list(pays_villes.keys()))
        ville = random.choice(pays_villes[pays])

        # Facteurs invisibles
        charge = random.randint(1, 10)
        pression = random.randint(1, 10)
        barriere = random.randint(1, 10)
        coupures = random.randint(0, 15)
        transport = round(random.uniform(0.5, 4.0), 1)
        stress = random.randint(1, 10)
        confiance = random.randint(1, 10)
        appartenance = random.randint(1, 10)
        sommeil = random.randint(1, 10)
        heures = round(random.uniform(0.5, 8.0), 1)
        acces = random.choice([0, 1])

        # Calcul réaliste de la moyenne
        score_positif = (confiance * 0.3 + sommeil * 0.2 +
                        appartenance * 0.2 + heures * 0.8)
        score_negatif = (charge * 0.2 + pression * 0.2 +
                        stress * 0.2 + barriere * 0.1 +
                        coupures * 0.1 + transport * 0.3)
        moyenne = round(
            max(3.0, min(19.5, 10 + score_positif - score_negatif +
                        random.uniform(-2, 2))), 1
        )

        # Statut basé sur la moyenne
        if moyenne >= 12:
            statut = "En réussite"
        elif moyenne >= 8:
            statut = "En difficulté"
        else:
            statut = "À risque de décrochage"

        etudiants.append((
            pays, ville,
            random.choice(universites),
            random.choice(filieres),
            random.choice(niveaux),
            random.choice(genres),
            random.randint(18, 30),
            moyenne, heures, acces,
            charge, pression, barriere,
            coupures, transport, stress,
            confiance, appartenance, sommeil,
            statut
        ))

    cursor.executemany('''
        INSERT INTO etudiants (
            pays, ville, universite, filiere, niveau, genre, age,
            moyenne_generale, heures_etude, acces_internet,
            charge_familiale, pression_financiere, barriere_linguistique,
            coupures_electricite, temps_transport, niveau_stress,
            confiance_soi, sentiment_appartenance, qualite_sommeil, statut
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', etudiants)

    conn.commit()
    conn.close()
    print(f"✅ {len(etudiants)} étudiants de démo générés avec succès !")

if __name__ == "__main__":
    generer_donnees_demo()
