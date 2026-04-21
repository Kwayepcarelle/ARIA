import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (classification_report, confusion_matrix,
                              accuracy_score)
from modules.database import charger_donnees

def afficher_classification():
    st.markdown("## 🌳 Classification Supervisée — Random Forest")
    st.markdown("""
    *Random Forest prédit automatiquement si un étudiant est
    en réussite, en difficulté ou à risque de décrochage.*
    """)

    df = charger_donnees()

    if len(df) < 10:
        st.warning("⚠️ Minimum 10 étudiants requis pour la classification.")
        return

    colonnes = [
        'heures_etude', 'charge_familiale', 'pression_financiere',
        'barriere_linguistique', 'coupures_electricite', 'temps_transport',
        'niveau_stress', 'confiance_soi', 'sentiment_appartenance',
        'qualite_sommeil', 'moyenne_generale'
    ]

    X = df[colonnes].dropna()
    y_raw = df.loc[X.index, 'statut']

    le = LabelEncoder()
    y = le.fit_transform(y_raw)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    st.markdown("---")
    st.markdown("### ⚙️ Paramètres du Modèle")

    col1, col2 = st.columns(2)
    with col1:
        n_trees = st.slider("Nombre d'arbres", 10, 200, 100, 10)
    with col2:
        max_depth = st.slider("Profondeur maximale", 2, 20, 5)

    rf = RandomForestClassifier(
        n_estimators=n_trees,
        max_depth=max_depth,
        random_state=42
    )
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    st.markdown("---")
    st.markdown("### 🎯 Performance du Modèle")

    col3, col4 = st.columns(2)
    with col3:
        st.metric("✅ Accuracy", f"{accuracy*100:.1f}%")
    with col4:
        st.metric("🌳 Arbres utilisés", n_trees)

    st.markdown("---")

    # Matrice de confusion
    st.markdown("### 🔲 Matrice de Confusion")
    cm = confusion_matrix(y_test, y_pred)
    labels_classes = le.classes_

    fig1 = px.imshow(
        cm, text_auto=True,
        x=labels_classes, y=labels_classes,
        color_continuous_scale='Blues',
        title="Matrice de Confusion",
        labels=dict(x="Prédit", y="Réel")
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # Importance des features
    st.markdown("### 🏆 Importance des Facteurs")
    importances = pd.DataFrame({
        'Facteur': colonnes,
        'Importance': rf.feature_importances_
    }).sort_values('Importance', ascending=True)

    fig2 = px.bar(
        importances, x='Importance', y='Facteur',
        orientation='h',
        title="Quels facteurs influencent le plus la réussite ?",
        color='Importance',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Prédiction individuelle
    st.markdown("### 🔮 Prédire le Statut d'un Étudiant")
    st.markdown("*Entre les valeurs d'un étudiant pour prédire son statut.*")

    col5, col6 = st.columns(2)
    with col5:
        h_etude = st.slider("📚 Heures d'étude/jour", 0.0, 12.0, 3.0, 0.5)
        charge = st.slider("💼 Charge familiale", 1, 10, 5)
        pression = st.slider("💸 Pression financière", 1, 10, 5)
        barriere = st.slider("🗣️ Barrière linguistique", 1, 10, 3)
        coupures = st.slider("🔦 Coupures électricité/sem", 0, 20, 3)
        transport = st.slider("🚌 Transport/jour (h)", 0.0, 6.0, 1.0, 0.5)

    with col6:
        stress = st.slider("😰 Niveau de stress", 1, 10, 5)
        confiance = st.slider("💪 Confiance en soi", 1, 10, 5)
        appartenance = st.slider("🤝 Sentiment d'appartenance", 1, 10, 5)
        sommeil = st.slider("😴 Qualité du sommeil", 1, 10, 5)
        moyenne = st.slider("📊 Moyenne générale /20", 0.0, 20.0, 10.0, 0.5)

    if st.button("🔮 Prédire maintenant", use_container_width=True):
        input_data = np.array([[
            h_etude, charge, pression, barriere, coupures,
            transport, stress, confiance, appartenance,
            sommeil, moyenne
        ]])
        input_scaled = scaler.transform(input_data)
        prediction = rf.predict(input_scaled)[0]
        probabilites = rf.predict_proba(input_scaled)[0]
        statut_predit = le.inverse_transform([prediction])[0]

        if statut_predit == "En réussite":
            st.success(f"✅ Statut prédit : **{statut_predit}**")
        elif statut_predit == "En difficulté":
            st.error(f"⚠️ Statut prédit : **{statut_predit}**")
        else:
            st.warning(f"🚨 Statut prédit : **{statut_predit}**")

        # Probabilités
        prob_df = pd.DataFrame({
            'Statut': le.classes_,
            'Probabilité (%)': (probabilites * 100).round(1)
        })
        fig3 = px.bar(
            prob_df, x='Statut', y='Probabilité (%)',
            color='Statut',
            title="Probabilités par statut",
            color_discrete_map={
                "En réussite": "#2ecc71",
                "En difficulté": "#e74c3c",
                "À risque de décrochage": "#f39c12"
            }
        )
        st.plotly_chart(fig3, use_container_width=True)