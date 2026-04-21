import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from modules.database import charger_donnees

def afficher_pca():
    st.markdown("## 🔬 Réduction de Dimensionnalité — ACP")
    st.markdown("""
    *L'Analyse en Composantes Principales (ACP) réduit la complexité
    des données tout en conservant l'essentiel de l'information.*
    """)

    df = charger_donnees()

    if len(df) < 5:
        st.warning("⚠️ Minimum 5 étudiants requis pour l'ACP.")
        return

    colonnes = [
        'heures_etude', 'charge_familiale', 'pression_financiere',
        'barriere_linguistique', 'coupures_electricite', 'temps_transport',
        'niveau_stress', 'confiance_soi', 'sentiment_appartenance',
        'qualite_sommeil', 'moyenne_generale'
    ]

    X = df[colonnes].dropna()
    statuts = df.loc[X.index, 'statut']

    # Standardisation
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ACP complète
    pca_full = PCA()
    pca_full.fit(X_scaled)
    variance_expliquee = pca_full.explained_variance_ratio_ * 100
    variance_cumulee = np.cumsum(variance_expliquee)

    st.markdown("---")

    # Variance expliquée
    st.markdown("### 📊 Variance Expliquée par Composante")
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=[f"CP{i+1}" for i in range(len(variance_expliquee))],
        y=variance_expliquee,
        name="Variance individuelle",
        marker_color='#3498db'
    ))
    fig1.add_trace(go.Scatter(
        x=[f"CP{i+1}" for i in range(len(variance_cumulee))],
        y=variance_cumulee,
        name="Variance cumulée",
        mode='lines+markers',
        line=dict(color='#e74c3c', width=3),
        yaxis='y2'
    ))
    fig1.update_layout(
        title="Variance expliquée par chaque composante principale",
        xaxis_title="Composantes",
        yaxis_title="Variance individuelle (%)",
        yaxis2=dict(
            title="Variance cumulée (%)",
            overlaying='y', side='right'
        ),
        legend=dict(x=0.6, y=0.9)
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Nombre de composantes
    n_comp = st.slider(
        "Nombre de composantes à visualiser", 2, 3, 2
    )

    pca = PCA(n_components=n_comp)
    X_pca = pca.fit_transform(X_scaled)

    st.markdown("---")

    if n_comp == 2:
        st.markdown("### 🗺️ Projection 2D des Étudiants")
        df_pca = pd.DataFrame({
            'CP1': X_pca[:, 0],
            'CP2': X_pca[:, 1],
            'Statut': statuts.values,
            'Moyenne': df.loc[X.index, 'moyenne_generale'].values
        })
        fig2 = px.scatter(
            df_pca, x='CP1', y='CP2',
            color='Statut', size='Moyenne',
            title="Projection ACP 2D — Profils étudiants",
            color_discrete_map={
                "En réussite": "#2ecc71",
                "En difficulté": "#e74c3c",
                "À risque de décrochage": "#f39c12"
            },
            labels={
                'CP1': f'CP1 ({variance_expliquee[0]:.1f}%)',
                'CP2': f'CP2 ({variance_expliquee[1]:.1f}%)'
            }
        )
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.markdown("### 🗺️ Projection 3D des Étudiants")
        df_pca = pd.DataFrame({
            'CP1': X_pca[:, 0],
            'CP2': X_pca[:, 1],
            'CP3': X_pca[:, 2],
            'Statut': statuts.values,
            'Moyenne': df.loc[X.index, 'moyenne_generale'].values
        })
        fig3 = px.scatter_3d(
            df_pca, x='CP1', y='CP2', z='CP3',
            color='Statut', size='Moyenne',
            title="Projection ACP 3D — Profils étudiants",
            color_discrete_map={
                "En réussite": "#2ecc71",
                "En difficulté": "#e74c3c",
                "À risque de décrochage": "#f39c12"
            }
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # Cercle des corrélations
    st.markdown("### 🎯 Contribution des Variables")
    composantes = pd.DataFrame(
        pca.components_[:2].T,
        columns=['CP1', 'CP2'],
        index=colonnes
    )

    fig4 = go.Figure()
    for var in colonnes:
        fig4.add_annotation(
            x=composantes.loc[var, 'CP1'],
            y=composantes.loc[var, 'CP2'],
            text=var, showarrow=True,
            arrowhead=2, arrowcolor='#3498db',
            ax=0, ay=0
        )
    theta = np.linspace(0, 2*np.pi, 100)
    fig4.add_trace(go.Scatter(
        x=np.cos(theta), y=np.sin(theta),
        mode='lines', line=dict(color='gray', dash='dash'),
        name='Cercle unitaire'
    ))
    fig4.update_layout(
        title="Cercle des corrélations",
        xaxis_title=f"CP1 ({variance_expliquee[0]:.1f}%)",
        yaxis_title=f"CP2 ({variance_expliquee[1]:.1f}%)",
        xaxis=dict(range=[-1.2, 1.2]),
        yaxis=dict(range=[-1.2, 1.2]),
        showlegend=False
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.success(f"""
    ✅ **Résultats ACP :**
    - {n_comp} composantes expliquent
      **{variance_cumulee[n_comp-1]:.1f}%** de la variance totale
    - Les variables les plus discriminantes sont visibles
      sur le cercle des corrélations
    """)