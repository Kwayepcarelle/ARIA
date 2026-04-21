import streamlit as st
from modules.database import init_database
from modules.collecte import afficher_collecte
from modules.descriptif import afficher_descriptif
from modules.regression import afficher_regression
from modules.pca import afficher_pca
from modules.clustering import afficher_clustering
from modules.classification import afficher_classification

st.set_page_config(
    page_title="ARIA — African Resilience & Intelligence Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_database()
from seed_data import generer_donnees_demo
generer_donnees_demo()

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1 class="main-title">🎓 ARIA</h1>
    <p class="main-subtitle">African Resilience & Intelligence Analytics</p>
    <p class="tagline">"We measure what others ignore"</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🧭 Navigation")
    st.markdown("---")
    page = st.radio(
        "Choisir un module :",
        [
            "🏠 Accueil",
            "📋 Collecte de Données",
            "📊 Analyse Descriptive",
            "📈 Régression Linéaire",
            "🔬 Réduction ACP",
            "🤖 Clustering K-Means",
            "🌳 Classification RF"
        ]
    )
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; padding:1rem;'>
        <p style='font-size:0.8rem; color:#a8dadc;'>
            INF 232 EC2 — TP Analyse de Données<br>
            Développé avec ❤️ pour l'Afrique<br>
            Python • Streamlit • SQLite
        </p>
    </div>
    """, unsafe_allow_html=True)

if page == "🏠 Accueil":
    st.markdown("## 🌍 Bienvenue sur ARIA")
    st.markdown("""
    **ARIA** est la première plateforme au monde qui mesure
    l'impact de la **charge invisible** sur la réussite
    académique des étudiants africains.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("""
        ### 🔬 Notre Mission
        Quantifier ce que personne ne mesure :
        la pression familiale, financière et
        psychologique que portent les étudiants
        africains au quotidien.
        """)
    with col2:
        st.success("""
        ### 📊 Notre Approche
        Collecte de données anonymes +
        analyse par Machine Learning pour
        révéler les vrais facteurs de réussite
        académique en Afrique.
        """)
    with col3:
        st.warning("""
        ### 🎯 Notre Impact
        Aider les universités africaines à
        identifier les étudiants à risque
        et à leur apporter un soutien ciblé
        avant qu'il ne soit trop tard.
        """)

    st.markdown("---")
    st.markdown("## 🗺️ Comment utiliser ARIA ?")

    etapes = {
        "1️⃣ Collecte": "Remplis le formulaire avec tes données réelles",
        "2️⃣ Descriptif": "Explore les statistiques et graphiques",
        "3️⃣ Régression": "Découvre quels facteurs influencent ta moyenne",
        "4️⃣ ACP": "Visualise les profils étudiants en 2D et 3D",
        "5️⃣ Clustering": "Découvre les groupes naturels d'étudiants",
        "6️⃣ Classification": "Prédit le statut académique d'un étudiant"
    }

    cols = st.columns(3)
    for i, (titre, desc) in enumerate(etapes.items()):
        with cols[i % 3]:
            st.markdown(f"""
            <div style='background:#1a1a2e; padding:1rem;
                        border-radius:10px; margin:0.5rem 0;
                        border-left:4px solid #e94560;'>
                <b style='color:#e94560;'>{titre}</b><br>
                <small style='color:#a8dadc;'>{desc}</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    > *"Dans les universités africaines, des milliers d'étudiants
    > brillants échouent non pas par manque d'intelligence,
    > mais à cause de fardeaux invisibles que personne ne mesure.
    > ARIA change ça."*
    """)

elif page == "📋 Collecte de Données":
    afficher_collecte()
elif page == "📊 Analyse Descriptive":
    afficher_descriptif()
elif page == "📈 Régression Linéaire":
    afficher_regression()
elif page == "🔬 Réduction ACP":
    afficher_pca()
elif page == "🤖 Clustering K-Means":
    afficher_clustering()
elif page == "🌳 Classification RF":
    afficher_classification()