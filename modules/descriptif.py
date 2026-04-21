import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.database import charger_donnees

def afficher_descriptif():
    st.markdown("## 📊 Analyse Descriptive")

    df = charger_donnees()

    if len(df) < 2:
        st.warning("⚠️ Pas assez de données. Remplis d'abord le formulaire !")
        return

    # KPI en haut
    st.markdown("### 🎯 Vue d'ensemble")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Étudiants", len(df))
    with col2:
        st.metric("📈 Moyenne générale", f"{df['moyenne_generale'].mean():.2f}/20")
    with col3:
        st.metric("😰 Stress moyen", f"{df['niveau_stress'].mean():.1f}/10")
    with col4:
        st.metric("💸 Pression financière", f"{df['pression_financiere'].mean():.1f}/10")

    st.markdown("---")

    # Distribution des moyennes
    st.markdown("### 📈 Distribution des Moyennes Générales")
    fig1 = px.histogram(
        df, x="moyenne_generale", nbins=20,
        color="statut",
        title="Distribution des moyennes par statut",
        color_discrete_map={
            "En réussite": "#2ecc71",
            "En difficulté": "#e74c3c",
            "À risque de décrochage": "#f39c12"
        },
        labels={"moyenne_generale": "Moyenne /20", "count": "Nombre"}
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # Charge invisible vs Moyenne
    st.markdown("### 🔬 Impact de la Charge Invisible sur la Réussite")
    col5, col6 = st.columns(2)

    with col5:
        fig2 = px.scatter(
            df, x="charge_familiale", y="moyenne_generale",
            color="statut", size="pression_financiere",
            title="Charge familiale vs Moyenne",
            labels={
                "charge_familiale": "Charge familiale /10",
                "moyenne_generale": "Moyenne /20"
            },
            color_discrete_map={
                "En réussite": "#2ecc71",
                "En difficulté": "#e74c3c",
                "À risque de décrochage": "#f39c12"
            }
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col6:
        fig3 = px.scatter(
            df, x="heures_etude", y="moyenne_generale",
            color="statut", size="niveau_stress",
            title="Heures d'étude vs Moyenne",
            labels={
                "heures_etude": "Heures d'étude/jour",
                "moyenne_generale": "Moyenne /20"
            },
            color_discrete_map={
                "En réussite": "#2ecc71",
                "En difficulté": "#e74c3c",
                "À risque de décrochage": "#f39c12"
            }
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # Heatmap de corrélation
    st.markdown("### 🔥 Carte de Corrélation — Facteurs Invisibles")
    colonnes = [
        'moyenne_generale', 'heures_etude', 'charge_familiale',
        'pression_financiere', 'barriere_linguistique',
        'coupures_electricite', 'temps_transport', 'niveau_stress',
        'confiance_soi', 'sentiment_appartenance', 'qualite_sommeil'
    ]
    corr = df[colonnes].corr()
    fig4 = px.imshow(
        corr, text_auto=".2f",
        color_continuous_scale="RdBu_r",
        title="Corrélations entre tous les facteurs",
        aspect="auto"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # Stats par pays
    st.markdown("### 🌍 Analyse par Pays")
    if df['pays'].nunique() > 1:
        fig5 = px.box(
            df, x="pays", y="moyenne_generale",
            color="pays",
            title="Distribution des moyennes par pays"
        )
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    # Tableau statistiques descriptives
    st.markdown("### 📋 Statistiques Descriptives Complètes")
    stats = df[colonnes].describe().round(2)
    st.dataframe(stats, use_container_width=True)