import streamlit as st
from modules.database import inserer_etudiant, compter_etudiants

def afficher_collecte():
    st.markdown("## 📋 Formulaire de Collecte")
    st.markdown("*Chaque donnée que tu fournis aide à comprendre la réussite académique en Afrique.*")
    st.info(f"👥 {compter_etudiants()} étudiants ont déjà contribué à ARIA")

    with st.form("formulaire_aria", clear_on_submit=True):

        st.markdown("### 🌍 Informations Générales")
        col1, col2 = st.columns(2)
        with col1:
            pays = st.selectbox("Pays", [
                "Cameroun", "Côte d'Ivoire", "Sénégal", "Mali",
                "Burkina Faso", "Guinée", "Congo", "Gabon",
                "Togo", "Bénin", "Niger", "Tchad", "Autre"
            ])
            ville = st.text_input("Ville")
            genre = st.selectbox("Genre", ["Femme", "Homme", "Autre"])
        with col2:
            universite = st.text_input("Université / École")
            filiere = st.text_input("Filière (ex: Informatique)")
            age = st.number_input("Âge", min_value=15, max_value=40, value=20)

        niveau = st.selectbox("Niveau d'études", [
            "Licence 1", "Licence 2", "Licence 3",
            "Master 1", "Master 2", "Doctorat"
        ])

        st.markdown("---")
        st.markdown("### 📚 Performances Académiques")
        col3, col4 = st.columns(2)
        with col3:
            moyenne_generale = st.slider(
                "Moyenne générale (/20)", 0.0, 20.0, 10.0, 0.5)
        with col4:
            heures_etude = st.slider(
                "Heures d'étude par jour", 0.0, 12.0, 3.0, 0.5)

        acces_internet = st.selectbox(
            "Accès Internet à domicile ?",
            [1, 0], format_func=lambda x: "Oui" if x == 1 else "Non"
        )

        st.markdown("---")
        st.markdown("### 🏠 Charge Invisible (ce que personne ne mesure)")
        st.caption("Note de 1 (très faible) à 10 (très élevé)")

        col5, col6 = st.columns(2)
        with col5:
            charge_familiale = st.slider(
                "💼 Responsabilités familiales", 1, 10, 5)
            pression_financiere = st.slider(
                "💸 Pression financière", 1, 10, 5)
            barriere_linguistique = st.slider(
                "🗣️ Barrière linguistique", 1, 10, 3)
        with col6:
            coupures_electricite = st.slider(
                "🔦 Coupures électricité/semaine", 0, 20, 3)
            temps_transport = st.slider(
                "🚌 Transport/jour (heures)", 0.0, 6.0, 1.0, 0.5)

        st.markdown("---")
        st.markdown("### 🧠 Bien-être Psychologique")

        col7, col8 = st.columns(2)
        with col7:
            niveau_stress = st.slider("😰 Niveau de stress", 1, 10, 5)
            confiance_soi = st.slider("💪 Confiance en soi", 1, 10, 5)
        with col8:
            sentiment_appartenance = st.slider(
                "🤝 Sentiment d'appartenance", 1, 10, 5)
            qualite_sommeil = st.slider("😴 Qualité du sommeil", 1, 10, 5)

        st.markdown("---")
        statut = st.selectbox("📊 Ton statut académique actuel", [
            "En réussite", "En difficulté", "À risque de décrochage"
        ])

        submitted = st.form_submit_button(
            "🚀 Soumettre ma contribution", use_container_width=True)

        if submitted:
            if not ville or not universite or not filiere:
                st.error("❌ Merci de remplir tous les champs texte !")
            else:
                data = {
                    'pays': pays, 'ville': ville, 'universite': universite,
                    'filiere': filiere, 'niveau': niveau, 'genre': genre,
                    'age': age, 'moyenne_generale': moyenne_generale,
                    'heures_etude': heures_etude, 'acces_internet': acces_internet,
                    'charge_familiale': charge_familiale,
                    'pression_financiere': pression_financiere,
                    'barriere_linguistique': barriere_linguistique,
                    'coupures_electricite': coupures_electricite,
                    'temps_transport': temps_transport,
                    'niveau_stress': niveau_stress,
                    'confiance_soi': confiance_soi,
                    'sentiment_appartenance': sentiment_appartenance,
                    'qualite_sommeil': qualite_sommeil,
                    'statut': statut
                }
                inserer_etudiant(data)
                st.success("✅ Merci ! Ta contribution a été enregistrée.")
                st.balloons()