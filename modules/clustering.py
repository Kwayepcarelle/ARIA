import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from modules.database import charger_donnees

def afficher_clustering():
    st.markdown("## 🤖 Classification Non-Supervisée — K-Means")
    st.markdown("""
    *K-Means découvre automatiquement des groupes d'étudiants
    aux profils similaires — sans étiquettes prédéfinies.*
    """)

    df = charger_donnees()

    if len(df) < 5:
        st.warning("⚠️ Minimum 5 étudiants requis pour le clustering.")
        return

    colonnes = [
        'heures_etude', 'charge_familiale', 'pression_financiere',
        'barriere_linguistique', 'coupures_electricite', 'temps_transport',
        'niveau_stress', 'confiance_soi', 'sentiment_appartenance',
        'qualite_sommeil', 'moyenne_generale'
    ]

    X = df[colonnes].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    st.markdown("---")

    # Méthode du coude
    st.markdown("### 📐 Méthode du Coude — Nombre optimal de clusters")
    inerties = []
    silhouettes = []
    K_range = range(2, min(8, len(df)))

    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inerties.append(km.inertia_)
        silhouettes.append(silhouette_score(X_scaled, km.labels_))

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=list(K_range), y=inerties,
        mode='lines+markers',
        name='Inertie',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=10)
    ))
    fig1.update_layout(
        title="Méthode du Coude",
        xaxis_title="Nombre de clusters (K)",
        yaxis_title="Inertie",
        showlegend=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=list(K_range), y=silhouettes,
        mode='lines+markers',
        name='Score Silhouette',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=10)
    ))
    fig2.update_layout(
        title="Score Silhouette par K",
        xaxis_title="Nombre de clusters (K)",
        yaxis_title="Score Silhouette",
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Choix du K
    k_optimal = st.slider(
        "🎯 Choisis le nombre de clusters :", 2, min(7, len(df)-1), 3
    )

    kmeans = KMeans(n_clusters=k_optimal, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    df_cluster = df.loc[X.index].copy()
    df_cluster['Cluster'] = [f"Groupe {i+1}" for i in labels]

    score_sil = silhouette_score(X_scaled, labels)
    st.metric("📊 Score Silhouette", f"{score_sil:.4f}",
              help="Plus proche de 1 = clusters bien séparés")

    st.markdown("---")

    # Visualisation 2D via PCA
    st.markdown("### 🗺️ Visualisation des Clusters")
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    df_viz = pd.DataFrame({
        'CP1': X_pca[:, 0],
        'CP2': X_pca[:, 1],
        'Cluster': df_cluster['Cluster'].values,
        'Moyenne': df_cluster['moyenne_generale'].values,
        'Stress': df_cluster['niveau_stress'].values
    })

    fig3 = px.scatter(
        df_viz, x='CP1', y='CP2',
        color='Cluster', size='Moyenne',
        title=f"Clusters K-Means (K={k_optimal}) — Projection ACP 2D",
        hover_data=['Moyenne', 'Stress']
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # Profil moyen de chaque cluster
    st.markdown("### 📋 Profil Moyen de Chaque Groupe")
    profils = df_cluster.groupby('Cluster')[colonnes].mean().round(2)
    st.dataframe(profils, use_container_width=True)

    st.markdown("---")

    # Radar chart par cluster
    st.markdown("### 🕸️ Radar — Comparaison des Profils")
    fig4 = go.Figure()
    categories = colonnes

    for cluster in profils.index:
        valeurs = profils.loc[cluster].tolist()
        valeurs_norm = [
            (v - df[col].min()) / (df[col].max() - df[col].min() + 1e-9)
            for v, col in zip(valeurs, colonnes)
        ]
        fig4.add_trace(go.Scatterpolar(
            r=valeurs_norm + [valeurs_norm[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=cluster
        ))

    fig4.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        title="Radar des profils par cluster"
    )
    st.plotly_chart(fig4, use_container_width=True)

    # Répartition des statuts par cluster
    st.markdown("### 🎯 Répartition des Statuts par Groupe")
    repartition = pd.crosstab(
        df_cluster['Cluster'], df_cluster['statut']
    )
    fig5 = px.bar(
        repartition, barmode='group',
        title="Statuts académiques par cluster",
        color_discrete_map={
            "En réussite": "#2ecc71",
            "En difficulté": "#e74c3c",
            "À risque de décrochage": "#f39c12"
        }
    )
    st.plotly_chart(fig5, use_container_width=True)