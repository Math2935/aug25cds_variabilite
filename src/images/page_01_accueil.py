import streamlit as st
from pathlib import Path
from utils import slide_header, kpi, callout


def page_accueil():
    slide_header(
        "Variabilité de la Production Photovoltaïque",
        "Analyse et prédiction · Région PACA · Données ouvertes · Pas de temps 30 min · 2020–2025"
    )

    tabs = st.tabs(["Contexte & objectif", "Démarche, équipe & périmètre"])

    # ── Tab 0 : Contexte & Objectif ──────────────────────────────────────────
    with tabs[0]:
        st.markdown(
            """<div class='kpi-row'>""" +
            kpi("5 ans", "Période d'analyse", "") +
            kpi("30 min", "Résolution temporelle", "accent") +
            kpi("~87 K", "Observations train+valid", "green") +
            kpi("5 pts", "Points géographiques", "orange") +
            """</div>""",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1.15, 1])

        with col1:
            st.markdown("<div class='slide-section compact'><h2>Pourquoi ce projet ?</h2>", unsafe_allow_html=True)

            st.markdown("""
**Les ENR intermittentes complexifient l'exploitation du réseau.**  
La production photovoltaïque dépend fortement de la météo : un passage nuageux peut provoquer une baisse rapide de production en quelques minutes.

**Le sujet opérationnel n'est pas seulement le niveau de production, mais sa vitesse de variation.**  
Une rampe mal anticipée peut conduire à une mobilisation de réserves, un écrêtage conservateur ou une perte de production renouvelable valorisable.

**Objectif : anticiper les fortes variations à court terme pour passer d'une gestion prudente à une gestion ciblée.**
            """)

            img_path = Path(__file__).parent / "images" / "Evolution_de_la_production_solaire_en_France__2026-06-07.png"
            if img_path.exists():
                st.image(
                    str(img_path),
                    caption="Évolution de la production solaire photovoltaïque en France (source : RTE)",
                    use_container_width=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section compact'><h2>Ce que le projet apporte</h2>", unsafe_allow_html=True)

            st.markdown("""
**Un indicateur opérationnel de variabilité**
- Cible : amplitude de variation du **TCH solaire** au prochain pas de temps
- Horizon : **+30 minutes**
- Données : production RTE + météo + atmosphère + astronomie
- Méthode : reproductible, explicable, sans fuite temporelle

**Une lecture orientée réseau**
- Détection des rampes critiques
- Seuil d'alerte calibré sur train + validation
- Arbitrage explicite entre recall et précision
            """)

            callout(
                "Conforme au cadrage : <strong>outil quantitatif, explicable, reproductible, construit sur données ouvertes.</strong>",
                "info"
            )

            st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 1 : Démarche, équipe & périmètre ────────────────────────────────
    with tabs[1]:
        col1, col2 = st.columns([1.35, 1])

        with col1:
            st.markdown("<div class='slide-section compact'><h2>Démarche projet</h2>", unsafe_allow_html=True)

            steps = [
                ("1", "Cadrage", "positionnement scientifique · cible variabilité · région PACA"),
                ("2", "Collecte", "RTE éCO2mix · CAMS · Open-Meteo · pvlib"),
                ("3", "Exploration", "saisonnalités · corrélations · identification des rampes"),
                ("4", "Feature engineering", "lags · variations · CSI · agrégation régionale"),
                ("5", "Modélisation", "baseline → modèles ML · ExtraTrees final · SHAP"),
                ("6", "Détection", "passage régression → événements critiques Q90"),
            ]

            for num, title, desc in steps:
                st.markdown(f"""
                <div class="mini-step">
                    <span class="mini-num">{num}</span>
                    <span><b>{title}</b> — {desc}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='slide-section compact'><h2>Sources de données</h2>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**Production PV**  ")
                st.markdown("RTE éCO2mix  ")
                st.markdown("PACA · 30 min")
            with c2:
                st.markdown("**Météo & atmosphère**  ")
                st.markdown("Open-Meteo · CAMS  ")
                st.markdown("Irradiance · nuages · aérosols")
            with c3:
                st.markdown("**Astronomie**  ")
                st.markdown("pvlib  ")
                st.markdown("Azimut · élévation · ciel clair")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section compact'><h2>Équipe</h2>", unsafe_allow_html=True)

            membres = [
                ("Mathilde Blanchard", "collecte & analyse exploratoire", "#1abc9c"),
                ("Moustapha Ibrahim", "feature engineering & modélisation", "#e94560"),
                ("Christophe Crestey", "cadrage, clustering, démo & conclusion", "#0f3460"),
            ]
            for nom, role, color in membres:
                st.markdown(f"""
                <div class="team-card" style="border-left-color:{color};">
                    <div class="team-name" style="color:{color};">{nom}</div>
                    <div class="team-role">{role}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='slide-section compact'><h2>Périmètre réalisé</h2>", unsafe_allow_html=True)

            st.markdown("""
| Paramètre | Valeur |
|---|---|
| **Région** | PACA |
| **Période** | 2020–2025 |
| **Résolution** | 30 min |
| **Points météo** | 5 communes représentatives |
| **Horizon** | +30 min |
| **Cible** | amplitude de variation du TCH |
            """)

            st.markdown("</div>", unsafe_allow_html=True)
