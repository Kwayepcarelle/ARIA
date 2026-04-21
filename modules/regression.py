import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from modules.database import charger_donnees

def afficher_regression():
    st.markdown("## 📈 Analyse par Régression Linéaire")
    st.markdown("*Comprendre quels facteurs influencent vraiment la moyenne.*")

    df = charger_donnees()

    if len(df) < 5:
        st.warning("⚠️ Minimum 5 étudiants requis pour la régression.")
        return

    colonnes_features = [
        'heures_etude', 'charge_familiale', 'pression_financiere',
        'barriere_linguistique', 'coupures_electricite', 'temps_transport',
        'niveau_stress', 'confiance_soi', 'sentiment_appartenance',
        'qualite_sommeil'
    ]

    labels_features = {
        'heures_etude': "📚 Heures d'étude",
        'charge_familiale': '💼 Charge familiale',
        'pression_financiere': '💸 Pression financière',
        'barriere_linguistique': '🗣️ Barrière linguistique',
        'coupures_electricite': '🔦 Coupures électricité',
        'temps_transport': '🚌 Temps de transport',
        'niveau_stress': '😰 Niveau de stress',
        'confiance_soi': '💪 Confiance en soi',
        'sentiment_appartenance': "🤝 Sentiment d'appartenance",
        'qualite_sommeil': '😴 Qualité du sommeil'
    }

    tab1, tab2 = st.tabs([
        "📊 Régression Simple", "📊 Régression Multiple"
    ])

    with tab1:
        st.markdown("### 📊 Régression Linéaire Simple")
        st.markdown("*Un seul facteur pour prédire la moyenne.*")

        facteur = st.selectbox(
            "Choisis le facteur à analyser :",
            colonnes_features,
            format_func=lambda x: labels_features[x]
        )

        X = df[[facteur]].values
        y = df['moyenne_generale'].values

        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("R² Score", f"{r2:.4f}")
        with col2:
            st.metric("RMSE", f"{rmse:.4f}")
        with col3:
            st.metric("Coefficient", f"{model.coef_[0]:.4f}")

        # Ligne de régression manuelle sans statsmodels
        x_range = np.linspace(X.min(), X.max(), 100)
        y_range = model.predict(x_range.reshape(-1, 1))

        fig = px.scatter(
            df, x=facteur, y='moyenne_generale',
            color='statut',
            title=f"Régression : {labels_features[facteur]} → Moyenne générale",
            color_discrete_map={
                "En réussite": "#2ecc71",
                "En difficulté": "#e74c3c",
                "À risque de décrochage": "#f39c12"
            }
        )
        fig.add_trace(go.Scatter(
            x=x_range, y=y_range,
            mode='lines',
            name='Droite de régression',
            line=dict(color='#e94560', width=3, dash='dash')
        ))
        st.plotly_chart(fig, use_container_width=True)

        st.info(f"""
        📌 **Interprétation :**
        - R² = {r2:.4f} → Le modèle explique **{r2*100:.1f}%** de la variance
        - Coefficient = {model.coef_[0]:.4f} → Chaque point de **{facteur}**
          change la moyenne de **{model.coef_[0]:.4f} points**
        - Intercept = {model.intercept_:.4f}
        """)

    with tab2:
        st.markdown("### 📊 Régression Linéaire Multiple")
        st.markdown("*Plusieurs facteurs combinés pour prédire la moyenne.*")

        features_choisies = st.multiselect(
            "Choisis les facteurs :",
            colonnes_features,
            default=['heures_etude', 'confiance_soi',
                     'pression_financiere', 'niveau_stress'],
            format_func=lambda x: labels_features[x]
        )

        if len(features_choisies) < 2:
            st.warning("Choisis au moins 2 facteurs.")
            return

        X_multi = df[features_choisies].values
        y_multi = df['moyenne_generale'].values

        X_train, X_test, y_train, y_test = train_test_split(
            X_multi, y_multi, test_size=0.2, random_state=42
        )

        model_multi = LinearRegression()
        model_multi.fit(X_train, y_train)
        y_pred_multi = model_multi.predict(X_test)

        r2_multi = r2_score(y_test, y_pred_multi)
        rmse_multi = np.sqrt(mean_squared_error(y_test, y_pred_multi))

        col4, col5 = st.columns(2)
        with col4:
            st.metric("R² Score (test)", f"{r2_multi:.4f}")
        with col5:
            st.metric("RMSE (test)", f"{rmse_multi:.4f}")

        coef_df = pd.DataFrame({
            'Facteur': [labels_features[f] for f in features_choisies],
            'Coefficient': model_multi.coef_
        }).sort_values('Coefficient', ascending=True)

        fig2 = px.bar(
            coef_df, x='Coefficient', y='Facteur',
            orientation='h',
            title="Impact de chaque facteur sur la moyenne",
            color='Coefficient',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=y_test, y=y_pred_multi,
            mode='markers',
            marker=dict(color='#3498db', size=10),
            name='Prédictions'
        ))
        fig3.add_trace(go.Scatter(
            x=[y_test.min(), y_test.max()],
            y=[y_test.min(), y_test.max()],
            mode='lines',
            line=dict(color='red', dash='dash'),
            name='Ligne parfaite'
        ))
        fig3.update_layout(
            title="Valeurs réelles vs Prédictions",
            xaxis_title="Valeurs réelles",
            yaxis_title="Valeurs prédites"
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.info(f"""
        📌 **Interprétation :**
        - R² = {r2_multi:.4f} → Le modèle explique **{r2_multi*100:.1f}%**
          de la variance avec {len(features_choisies)} facteurs
        - RMSE = {rmse_multi:.4f} → Erreur moyenne de prédiction
        """)
