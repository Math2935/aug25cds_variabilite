import streamlit as st
from pathlib import Path
from utils import slide_header, kpi, callout


def page_accueil():
    slide_header(
        "Variabilité de la Production Photovoltaïque",
        "Analyse et prédiction · Région PACA · Données ouvertes · Pas de temps 30 min · 2020–2025"
    )

    tabs = st.tabs(["Contexte & Démarche", "Équipe & Périmètre"])

    # ── Tab 0 : Contexte & Démarche ───────────────────────────────────────────
    with tabs[0]:
        st.markdown("""<div class='kpi-row'>""" +
            kpi("5 ans", "Période d'analyse", "") +
            kpi("30 min", "Résolution temporelle", "accent") +
            kpi("~87 K", "Observations (train+valid)", "green") +
            kpi("5 pts", "Points géographiques", "orange") +
        """</div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Pourquoi ce projet ?</h2>", unsafe_allow_html=True)
            items = [
                ("Les ENR intermittentes perturbent le réseau",
                 "Un passage nuageux = chute de plusieurs dizaines de MW en minutes"),
                ("Les rampes critiques forcent un écrêtage conservateur",
                 "Pas un problème de demande — un problème de vitesse de variation"),
                ("Anticiper les rampes",
                 "Passer de la précaution à la gestion ciblée"),
            ]
            for titre, desc in items:
                st.markdown(f"""
                <div style="margin-bottom:0.5rem; padding:0.5rem 0.8rem; background:#f8f9fd;
                            border-left:3px solid #0f3460; border-radius:6px;">
                    <div style="font-weight:700; color:#0f3460; font-size:0.9rem;">{titre}</div>
                    <div style="color:#555; font-size:0.82rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

            img_path = Path(__file__).parent / "images" / "Evolution_de_la_production_solaire_en_France__2026-06-07.png"
            if img_path.exists():
                st.image(str(img_path), caption="Évolution de la production solaire PV en France (source : RTE)")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Démarche</h2>", unsafe_allow_html=True)
            steps = [
                ("1", "Cadrage", "Positionnement scientifique · clustering géographique PACA"),
                ("2", "Collecte", "RTE éCO2mix · CAMS · Open-Meteo · Astronomie"),
                ("3", "Exploration", "Distribution cible · saisonnalités · identification rampes"),
                ("4", "Feature Engineering", "Encodages cycliques · lags · CSI · agrégation régionale"),
                ("5", "Modélisation", "Baseline → ExtraTrees final · SHAP"),
            ]
            for num, title, desc in steps:
                st.markdown(f"""
                <div style="display:flex; align-items:flex-start; gap:0.8rem; margin-bottom:0.4rem;
                            padding:0.4rem 0.8rem; background:#f8f9fd; border-radius:8px;
                            border-left:3px solid #e94560;">
                    <div style="font-size:1.1rem; font-weight:800; color:#e94560; min-width:20px;">{num}</div>
                    <div>
                        <span style="font-weight:700; color:#0f3460; font-size:0.88rem;">{title}</span>
                        <span style="color:#666; font-size:0.8rem;"> — {desc}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            callout("""
Outil <strong>quantitatif, explicable, reproductible</strong> — données ouvertes exclusivement.
            """, "info")
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 1 : Équipe & Périmètre ────────────────────────────────────────────
    with tabs[1]:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Équipe</h2>", unsafe_allow_html=True)
            membres = [
                ("Mathilde Blanchard", "Collecte de données & analyse exploratoire", "#1abc9c"),
                ("Moustapha Ibrahim", "Feature engineering & modélisation", "#e94560"),
                ("Christophe Crestey", "Clustering géographique, introduction, conclusion & démo", "#0f3460"),
            ]
            for nom, role, color in membres:
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.7rem;
                            padding:0.7rem 1rem; border-radius:10px; border-left:4px solid {color};
                            background:#f8f9fd;">
                    <div style="font-weight:700; color:{color}; min-width:160px;">{nom}</div>
                    <div style="color:#555; font-size:0.88rem;">{role}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Périmètre</h2>", unsafe_allow_html=True)
            st.markdown("""
| Paramètre | Valeur |
|---|---|
| **Région** | Provence-Alpes-Côte d'Azur |
| **Période** | Janvier 2020 – Janvier 2025 |
| **Résolution** | 30 minutes |
| **Points géo** | 5 communes représentatives |
| **Horizon** | +30 min |
| **Cible** | Amplitude variation TCH |
            """)
            st.markdown("</div>", unsafe_allow_html=True)
