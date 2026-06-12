import streamlit as st


st.set_page_config(
    page_title="Variabilité Solaire PACA",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global CSS - clean white style, powerpoint-like
st.markdown("""
<style>
.warn { border-left:0px solid #f59e0b; background:#fffbeb; padding:14px 16px; border-radius:14px; }
.ok { border-left:0px solid #16a34a; background:#f0fdf4; padding:14px 16px; border-radius:14px; }
/* ---- Base ---- */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%) !important;
}
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
[data-testid="stSidebar"] .stRadio label { color: #ffffff !important; font-weight: 500; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }

/* ---- Slide-like containers ---- */
.slide-header {
    background: linear-gradient(135deg, #0f3460 0%, #e94560 100%);
    color: white;
    padding: 1.2rem 2rem;
    border-radius: 16px;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(15,52,96,0.18);
}
.slide-header h1 { color: white !important; font-size: 1.9rem; margin: 0; font-weight: 700; }
.slide-header p  { color: rgba(255,255,255,0.85) !important; font-size: 0.95rem; margin-top: 0.2rem; }

.slide-section {
    background: #ffffff;
    border: 1.5px solid #e8ecf4;
    border-radius: 14px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.slide-section h2 {
    color: #0f3460 !important;
    font-size: 1.25rem;
    border-bottom: 2px solid #e94560;
    padding-bottom: 0.3rem;
    margin-bottom: 0.7rem;
}

/* ---- KPI cards ---- */
.kpi-row { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
.kpi-card {
    flex: 1; min-width: 150px;
    background: linear-gradient(135deg, #0f3460 0%, #1a5276 100%);
    color: white;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    box-shadow: 0 4px 16px rgba(15,52,96,0.15);
}
.kpi-card .kpi-value { font-size: 2rem; font-weight: 700; }
.kpi-card .kpi-label { font-size: 0.8rem; opacity: 0.85; margin-top: 0.2rem; }
.kpi-card.accent { background: linear-gradient(135deg, #e94560 0%, #c0392b 100%); }
.kpi-card.green  { background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%); }
.kpi-card.orange { background: linear-gradient(135deg, #f39c12 0%, #d35400 100%); }

/* ---- Formula box ---- */
.formula-box {
    background: #f8f9fd;
    border-left: 4px solid #0f3460;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    font-family: 'Courier New', monospace;
    font-size: 1.05rem;
    color: #1a1a2e;
    margin: 1rem 0;
}

/* ---- Step badge ---- */
.step-badge {
    display: inline-block;
    background: #0f3460;
    color: white;
    border-radius: 50%;
    width: 28px; height: 28px;
    text-align: center; line-height: 28px;
    font-weight: 700; font-size: 0.85rem;
    margin-right: 0.5rem;
}

/* ---- Tab styling ---- */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: #f0f4fa;
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    color: #555;
}
.stTabs [aria-selected="true"] {
    background: #0f3460 !important;
    color: white !important;
}

/* ---- Streamlit metric ---- */
[data-testid="metric-container"] {
    background: #f8f9fd;
    border: 1px solid #e0e7f0;
    border-radius: 10px;
    padding: 0.8rem 1rem;
}

/* ---- Tables ---- */
.dataframe { border-radius: 8px; overflow: hidden; }

/* ---- Callout ---- */
.callout {
    background: #fff9e6;
    border-left: 4px solid #f39c12;
    padding: 0.8rem 1.2rem;
    border-radius: 6px;
    margin: 0.8rem 0;
    color: #7d6608;
}
.callout-info {
    background: #eaf4ff;
    border-left: 4px solid #0f3460;
    padding: 0.8rem 1.2rem;
    border-radius: 6px;
    margin: 0.8rem 0;
    color: #154360;
}
.callout-success {
    background: #eafaf1;
    border-left: 4px solid #1abc9c;
    padding: 0.8rem 1.2rem;
    border-radius: 6px;
    margin: 0.8rem 0;
    color: #0e6655;
}

/* ---- Sidebar nav ---- */
.nav-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: rgba(255,255,255,0.45) !important;
    padding: 0.3rem 0;
    display: block;
}

/* ---- Compact mode for soutenance ---- */
.slide-section.compact {
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.8rem;
    border-radius: 10px;
}
.slide-section.compact h2 {
    font-size: 1.05rem;
    margin-bottom: 0.5rem;
    padding-bottom: 0.2rem;
}
.kpi-row {
    gap: 0.6rem;
    margin-bottom: 0.8rem;
}
.kpi-card {
    min-width: 120px;
    padding: 0.75rem 1rem;
    border-radius: 10px;
}
.kpi-card .kpi-value { font-size: 1.45rem; }
.kpi-card .kpi-label { font-size: 0.72rem; }
.mini-step {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 0.45rem;
    padding: 0.45rem 0.65rem;
    background: #f8f9fd;
    border-radius: 8px;
    border-left: 3px solid #0f3460;
    font-size: 0.84rem;
}
.mini-num {
    font-weight: 800;
    color: #e94560;
    min-width: 20px;
    text-align: center;
}
.team-card {
    margin-bottom: 0.55rem;
    padding: 0.55rem 0.75rem;
    border-left: 3px solid #0f3460;
    background: #f8f9fd;
    border-radius: 8px;
}
.team-name {
    font-weight: 700;
    font-size: 0.88rem;
}
.team-role {
    color: #555;
    font-size: 0.8rem;
}

</style>
""", unsafe_allow_html=True)

# ---- Sidebar navigation ----
with st.sidebar:
    # Logo Liora
    from pathlib import Path
    import base64
    logo_path = Path(__file__).parent / "images" / "liora.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"<img src='data:image/png;base64,{logo_b64}' style='width:100%; max-width:140px; margin-bottom:0.5rem;'>", unsafe_allow_html=True)

    st.markdown("## ☀️ Variabilité Solaire")
    st.markdown("**Production PV · Région PACA — 2020–2025**")
    st.markdown("---")
    st.markdown("""
<small style='color:rgba(255,255,255,0.55); font-size:0.72rem; line-height:1.6;'>
Formation Data Scientist<br>
Promotion August 2025<br><br>
Christophe Crestey<br>
Moustapha Ibrahim<br>
Mathilde Blanchard
</small>
""", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<span class="nav-label">Navigation</span>', unsafe_allow_html=True)
    page = st.radio(
        "",
        [
            "1. Accueil",
            "2. Cadrage de l'étude",
            "3. Collecte de données",
            "4. Analyse exploratoire",
            "5. Feature Engineering",
            "6. Modélisation",
            "7. Interprétabilité",
            "8. Prédiction en ligne",
            "9. Conclusion",
            "Annexe - Rampes Critiques",
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(
        "<small style='color:rgba(255,255,255,0.4)'>Projet ML · Prédiction variabilité PV<br>Données RTE/Météo · Pas 30 min</small>",
        unsafe_allow_html=True
    )

# ---- Page routing ----
if page == "1. Accueil":
    from page_01_accueil import page_accueil
    page_accueil()
elif page == "2. Cadrage de l'étude":
    from page_02_cadrage import page_cadrage
    page_cadrage()
elif page == "3. Collecte de données":
    from page_03_collecte import page_collecte
    page_collecte()
elif page == "4. Analyse exploratoire":
    from page_04_exploration import page_exploration
    page_exploration()
elif page == "5. Feature Engineering":
    from page_05_feature_eng import page_feature_engineering
    page_feature_engineering()
elif page == "6. Modélisation":
    from page_06_modelisation import page_modelisation
    page_modelisation()
elif page == "7. Interprétabilité":
    from page_07_interpretabilite import page_interpretabilite
    page_interpretabilite()
elif page == "8. Prédiction en ligne":
    from pages_09_predictions import page_prediction
    page_prediction()
elif page == "9. Conclusion":
    from page_10_conclusion import page_conclusion
    page_conclusion()
elif page == "Annexe - Rampes Critiques":
    from pages_08_rampes import page_rampes
    page_rampes()
