import streamlit as st
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from utils import slide_header, section, kpi, callout, step_badge

COMMUNES = pd.DataFrame({
    "commune":   ["Cruis", "Saint-Étienne-le-Laus", "Saint-Vallier-de-Thiey", "Bras", "Eygalières"],
    "prefix":    ["cru",   "sel",                   "svt",                    "bra",  "eyg"],
    "cluster":   [0,        1,                       2,                        3,      4],
    "lat":       [43.9833,  44.5333,                 43.7333,                  43.4500, 43.7167],
    "lon":       [5.8833,   6.1333,                  6.8500,                   6.1500,  4.9500],
    "zone":      ["Alpes de Haute-Provence", "Hautes-Alpes", "Alpes-Maritimes", "Var", "Bouches-du-Rhône"],
    "contrib_pct": [18.2,   14.7,                    16.1,                     22.4,   28.6],
})

K_VALUES = list(range(2, 10))
INERTIAS  = [0.82, 0.61, 0.47, 0.38, 0.31, 0.26, 0.22, 0.19]
COLORS = px.colors.qualitative.Bold


def page_cadrage():
    slide_header(
        "Cadrage de l'étude",
        "Positionnement scientifique · Cadrage méthodologique · Ancrage géographique PACA"
    )

    tabs = st.tabs(["Positionnement & Cadrage", "Clustering géographique PACA"])

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 0 : Positionnement & Cadrage (fusionné)
    # ══════════════════════════════════════════════════════════════════════════
    with tabs[0]:

        # ── Littérature : résumé compact ──
        st.markdown("<div class='slide-section'><h2>Ce que la littérature fait — et ce qu'elle ne fait pas</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
<p style="font-weight:700; color:#1a1a2e; font-size:0.9rem; margin-bottom:0.4rem;">Prévision de production <span style="font-weight:400; color:#666;">— domaine mature</span></p>
<div style="padding:0.3rem 0.7rem; background:#e8f4fd; border-left:2px solid #0f3460; border-radius:4px; margin-bottom:0.2rem; font-size:0.82rem;">
<span style="font-weight:600; color:#0f3460;">Lindas et al. (2025)</span> <span style="color:#555;">— RTE + météo spatiale → benchmark ML · prédit des <strong>niveaux</strong>, pas la variabilité</span></div>
<div style="padding:0.3rem 0.7rem; background:#e8f4fd; border-left:2px solid #0f3460; border-radius:4px; margin-bottom:0.5rem; font-size:0.82rem;">
<span style="font-weight:600; color:#0f3460;">De Giorgi (2014) · IRENA (2020)</span> <span style="color:#555;">— prévision PV, approches avancées ENR</span></div>

<p style="font-weight:700; color:#1a1a2e; font-size:0.9rem; margin-bottom:0.4rem;">Volatilité des marchés <span style="font-weight:400; color:#666;">— documentée, non anticipée</span></p>
<div style="padding:0.3rem 0.7rem; background:#fff3cd; border-left:2px solid #f39c12; border-radius:4px; font-size:0.82rem;">
<span style="font-weight:600; color:#7d6608;">Kiesel (2017) · Cramer (2022) · ACER (2023)</span> <span style="color:#666;">— volatilité prix et réseau liée aux ENR</span></div>
            """, unsafe_allow_html=True)
            callout("Ces travaux <strong>mesurent la volatilité comme un effet</strong> — aucun n'anticipe les rampes à court terme.", "warn")

        with col2:
            st.markdown("**Ce que ce projet apporte — et que la littérature ne fait pas**")
            manques = [
                ("Anticipation à 30 min", "Détection des rampes sur données ouvertes"),
                ("Seuil calibré sur 5 ans", "Quantification du niveau critique pour le réseau"),
                ("Seuil ajustable", "Régime adaptable au coût opérationnel de l'alerte"),
            ]
            for titre, desc in manques:
                st.markdown(f"""
                <div style="margin-bottom:0.4rem; padding:0.4rem 0.8rem; background:#eafaf1;
                            border-left:3px solid #1abc9c; border-radius:6px;">
                    <span style="font-weight:700; color:#0e6655; font-size:0.85rem;">{titre}</span>
                    <span style="color:#555; font-size:0.82rem;"> — {desc}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Schéma de positionnement ──
        st.markdown("""
<div style="display:flex; gap:0.8rem; margin:0 0 1.5rem 0; flex-wrap:wrap; align-items:stretch;">
    <div style="flex:1; min-width:160px; padding:0.8rem 1rem; background:#fff3cd;
                border-radius:10px; border-top:3px solid #f39c12; text-align:center;">
        <div style="font-weight:700; color:#f39c12; font-size:0.85rem; margin-bottom:0.3rem;">Littérature</div>
        <div style="color:#555; font-size:0.82rem;">Mesure la volatilité <em>ex post</em></div>
    </div>
    <div style="display:flex; align-items:center; font-size:1.4rem; color:#ccc;">→</div>
    <div style="flex:1.3; min-width:200px; padding:0.8rem 1rem; background:#eafaf1;
                border-radius:10px; border-top:4px solid #1abc9c; text-align:center;">
        <div style="font-weight:800; color:#1abc9c; font-size:0.9rem; margin-bottom:0.3rem;">Ce projet</div>
        <div style="color:#444; font-size:0.82rem;"><strong>Anticipe</strong> la variabilité à 30 min</div>
    </div>
    <div style="display:flex; align-items:center; font-size:1.4rem; color:#ccc;">←</div>
    <div style="flex:1; min-width:160px; padding:0.8rem 1rem; background:#eaf4ff;
                border-radius:10px; border-top:3px solid #0f3460; text-align:center;">
        <div style="font-weight:700; color:#0f3460; font-size:0.85rem; margin-bottom:0.3rem;">Prévision production</div>
        <div style="color:#555; font-size:0.82rem;">Prédit les niveaux — domaine mature</div>
    </div>
</div>
        """, unsafe_allow_html=True)

        # ── Pourquoi PACA + asymétrie ──
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Pourquoi la région PACA ?</h2>", unsafe_allow_html=True)
            st.markdown("""
- **Fort ensoleillement** — parmi les régions les plus irradiées de France
- **Variabilité météo** — contrastes littoral / vallées / massifs alpins
- **Parc PV développé** — 2e région française en capacité installée
            """)
            img_path = Path(__file__).parent / "images" / "Global_Solar_Irradiation_France.jpg"
            if img_path.exists():
                st.image(str(img_path), caption="Irradiance solaire annuelle moyenne en France (PVGIS / JRC)")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Asymétrie des données → clustering</h2>", unsafe_allow_html=True)
            st.markdown("""
<div style="padding:0.6rem 1rem; background:#fff3cd; border-radius:8px;
            margin-bottom:0.5rem; border-left:3px solid #f39c12;">
<strong>Variable cible (RTE)</strong> — production PV agrégée <strong>régionale</strong>, une seule série
</div>
<div style="padding:0.6rem 1rem; background:#d4edda; border-radius:8px;
            margin-bottom:0.7rem; border-left:3px solid #28a745;">
<strong>Variables explicatives (CAMS, météo)</strong> — haute résolution <strong>spatiale</strong>
</div>
            """, unsafe_allow_html=True)
            st.markdown("""
**Question :** où collecter les données météo ?

→ Identifier des points représentatifs pondérés par le parc PV installé
            """)
            callout("Le clustering n'était pas prévu — c'est la contrainte RTE qui l'a rendu nécessaire.", "warn")
            st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 1 : Clustering géographique PACA
    # ══════════════════════════════════════════════════════════════════════════
    with tabs[1]:

        col1, col2, col3 = st.columns([1.4, 1, 1])

        # ── Colonne 1 : Carte ──
        with col1:
            st.markdown("<div class='slide-section'><h2>Carte PACA</h2>", unsafe_allow_html=True)
            img_carte = Path(__file__).parent / "images" / "carte_paca_communes.png"
            if img_carte.exists():
                st.image(str(img_carte), caption="Communes représentatives du parc PV")
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Colonne 2 : 5 communes ──
        with col2:
            st.markdown("<div class='slide-section'><h2>5 communes</h2>", unsafe_allow_html=True)
            for i, row in COMMUNES.iterrows():
                st.markdown(f"""
                <div style="margin-bottom:0.5rem; padding:0.5rem 0.8rem; border-radius:8px;
                            border-left:4px solid {COLORS[i]}; background:#f8f9fd;">
                    <span style="font-weight:700; color:{COLORS[i]}; font-size:0.9rem;">
                        {row['commune']}</span>
                    <span style="color:#555; font-size:0.82rem;">
                        · {row['zone'].split(' ')[0] if len(row['zone']) > 20 else row['zone']}
                        · <strong>{row['contrib_pct']} %</strong>
                    </span>
                </div>
                """, unsafe_allow_html=True)
            callout("<strong>5 points d'ancrage</strong> pour la collecte météo, atmosphère et astronomie.", "success")
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Colonne 3 : Coude KMeans ──
        with col3:
            st.markdown("<div class='slide-section'><h2>KMeans non supervisé</h2>", unsafe_allow_html=True)
            fig_coude = go.Figure()
            fig_coude.add_trace(go.Scatter(
                x=K_VALUES, y=INERTIAS, mode="lines+markers",
                line=dict(color="#0f3460", width=2.5),
                marker=dict(size=7, color="#0f3460"), name="Inertie"
            ))
            fig_coude.add_trace(go.Scatter(
                x=[5], y=[INERTIAS[3]], mode="markers",
                marker=dict(size=14, color="#e94560", symbol="star"),
                name="K = 5"
            ))
            fig_coude.add_vline(x=5, line_dash="dash", line_color="#e94560", opacity=0.4)
            fig_coude.update_layout(
                xaxis_title="K", yaxis_title="Inertie",
                height=280, margin=dict(l=10, r=10, t=20, b=20),
                legend=dict(orientation="h", y=-0.3, font=dict(size=10)),
                plot_bgcolor="white", paper_bgcolor="white",
            )
            fig_coude.update_xaxes(gridcolor="#f0f0f0", dtick=1)
            fig_coude.update_yaxes(gridcolor="#f0f0f0")
            st.plotly_chart(fig_coude, use_container_width=True)
            st.markdown("""
K=5 : choix pragmatique — couverture territoriale + volume de données maîtrisé.
            """)
            st.markdown("</div>", unsafe_allow_html=True)
