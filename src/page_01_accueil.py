import streamlit as st
from pathlib import Path
from utils import slide_header, kpi, callout


def page_accueil():
    slide_header(
        "Variabilité de la Production Photovoltaïque",
        "Analyse et prédiction · Région PACA · Données ouvertes · Pas de temps 30 min · 2020–2025"
    )

    tabs = st.tabs(["Contexte & Objectif", "Démarche, sources & périmètre"])

    # ── Tab 0 : Contexte & Objectif ──────────────────────────────────────────
    with tabs[0]:
        st.markdown("""<div class='kpi-row'>""" +
            kpi("5 ans", "Période d'analyse", "") +
            kpi("30 min", "Résolution temporelle", "accent") +
            kpi("~87 K", "Observations train+valid", "green") +
            kpi("5 pts", "Représentation PACA", "orange") +
        """</div>""", unsafe_allow_html=True)

        col1, col2 = st.columns([1.15, 1])

        with col1:
            st.markdown("<div class='slide-section compact'><h2>Pourquoi ce projet ?</h2>", unsafe_allow_html=True)

            st.markdown("""
**Le photovoltaïque est une énergie exigeante à accueillir sur le réseau**
- Forte croissance des raccordements renouvelables
- Facteur de charge faible, mais réseau dimensionné pour la puissance maximale
- Production dépendante de la météo, donc variable à court terme
            """)

            st.markdown("""
**Le problème opérationnel : la vitesse de variation**
- Un passage nuageux peut faire varier fortement la production en quelques minutes
- Faute d'anticipation : réserves, contraintes locales ou écrêtage préventif
- L'enjeu n'est pas seulement le niveau produit, mais la **rampe** à venir
            """)

            callout(
                "Anticiper les rampes permet de passer d'une logique prudente à une gestion plus ciblée.",
                "info"
            )

            img_path = Path(__file__).parent / "images" / "Evolution_de_la_production_solaire_en_France__2026-06-07.png"
            if img_path.exists():
                st.image(
                    str(img_path),
                    caption="Évolution de la production solaire photovoltaïque en France (source : RTE)"
                )

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section compact'><h2>Ce que ce projet apporte</h2>", unsafe_allow_html=True)

            st.markdown("""
**Un indicateur opérationnel de variabilité**
- Cible : amplitude de variation du TCH à **+30 min**
- Données exclusivement ouvertes
- Alerte calibrée sur données historiques
- Méthodologie explicable et reproductible
            """)

            st.markdown("""
**Question métier**

> Le photovoltaïque régional va-t-il rester stable ou devenir fortement variable dans les 30 prochaines minutes ?
            """)

            callout(
                "Conforme à l'énoncé du projet : outil quantitatif, explicable, reproductible, construit sur données ouvertes.",
                "success"
            )

            st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 1 : Démarche, sources & périmètre ───────────────────────────────
    with tabs[1]:
        col1, col2 = st.columns([1.25, 1])

        with col1:
            st.markdown("<div class='slide-section compact'><h2>Pipeline méthodologique</h2>", unsafe_allow_html=True)

            steps = [
                ("1", "Cadrage", "PACA · cible variabilité · données ouvertes"),
                ("2", "Collecte", "Production · irradiance · météo · astronomie"),
                ("3", "Exploration", "Saisonnalité · corrélations · rampes"),
                ("4", "Features", "Lags · variations · CSI · agrégation régionale"),
                ("5", "Modélisation", "Baseline → ExtraTrees · SHAP · détection Q90"),
            ]

            for num, title, desc in steps:
                st.markdown(f"""
                <div class="mini-step">
                    <span class="mini-num">{num}</span>
                    <span><b>{title}</b> — {desc}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='slide-section compact'><h2>Sources mobilisées</h2>", unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown("""
                <div class="source-card">
                    <div class="source-title">Production</div>
                    <div class="source-main">RTE éCO2mix</div>
                    <div class="source-sub">PV PACA · 30 min</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown("""
                <div class="source-card">
                    <div class="source-title">Atmosphère</div>
                    <div class="source-main">Copernicus CAMS</div>
                    <div class="source-sub">GHI · DHI · BNI</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown("""
                <div class="source-card">
                    <div class="source-title">Météo</div>
                    <div class="source-main">NASA POWER</div>
                    <div class="source-sub">Température · vent · nuages</div>
                </div>
                """, unsafe_allow_html=True)
            with c4:
                st.markdown("""
                <div class="source-card">
                    <div class="source-title">Astronomie</div>
                    <div class="source-main">pvlib</div>
                    <div class="source-sub">Azimut · élévation</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <p style="font-size:0.86rem;color:#555;margin-top:0.6rem;">
            Ces quatre familles de données sont harmonisées au pas de 30 minutes à l'échelle PACA.
            Le détail de la collecte et de la préparation est présenté dans la section suivante.
            </p>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section compact'><h2>Équipe & périmètre</h2>", unsafe_allow_html=True)

            membres = [
                ("Mathilde", "Collecte & exploration", "#1abc9c"),
                ("Moustapha", "Features & modélisation", "#e94560"),
                ("Christophe", "Cadrage · démo · conclusion", "#0f3460"),
            ]
            for nom, role, color in membres:
                st.markdown(f"""
                <div style="margin-bottom:0.45rem;padding:0.45rem 0.7rem;border-radius:8px;
                            border-left:3px solid {color};background:#f8f9fd;font-size:0.86rem;">
                    <b style="color:{color};">{nom}</b> — <span style="color:#555;">{role}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
| Paramètre | Valeur |
|---|---|
| **Région** | PACA |
| **Période** | 2020–2025 |
| **Pas de temps** | 30 min |
| **Points météo** | 5 communes représentatives |
| **Horizon** | +30 min |
| **Cible** | Amplitude de variation du TCH |
            """)

            st.markdown("</div>", unsafe_allow_html=True)
