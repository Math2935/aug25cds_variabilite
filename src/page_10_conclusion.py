import streamlit as st
import pandas as pd

from utils import slide_header, kpi, callout


def page_conclusion():
    slide_header(
        "Conclusion & Perspectives",
        "Bilan du projet · Enseignements · Opportunités de déploiement"
    )

    tabs = st.tabs([
        "Bilan & Résultats",
        "Progrès & Enseignements",
        "Perspectives",
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 0 : Bilan & Résultats
    # ══════════════════════════════════════════════════════════════════════════
    with tabs[0]:

        st.markdown("""<div class='kpi-row'>""" +
            kpi("0.467", "MAE test", "") +
            kpi("0.89", "R² test", "green") +
            kpi("85.5%", "Détection rampes", "accent") +
            kpi("14.5%", "Manquées", "orange") +
        """</div>""", unsafe_allow_html=True)

        st.markdown("<div class='slide-section'><h2>Ce que nous avons démontré</h2>", unsafe_allow_html=True)

        items = [
            "La variabilité photovoltaïque est prédictible à court terme.",
            "Des données ouvertes suffisent pour construire un modèle performant.",
            "Les variables météorologiques expliquent une grande partie des fluctuations observées.",
            "Plus de 8 rampes critiques sur 10 sont détectées avec 30 minutes d'avance."
        ]

        for item in items:
            st.markdown(f"""
            <div style="display:flex; align-items:flex-start; gap:0.8rem; margin-bottom:0.6rem;
                        padding:0.6rem 1rem; background:#eafaf1; border-radius:8px;
                        border-left:3px solid #1abc9c;">
                <span style="font-size:1.2rem; color:#1abc9c; min-width:24px; font-weight:700;">✅</span>
                <span style="color:#444; font-size:0.95rem;">{item}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        callout("""
<strong>85 % des rampes critiques détectées avec 30 minutes d'avance,
sur données ouvertes exclusivement.</strong>
        """, "success")

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 1 : Progrès & Enseignements
    # ══════════════════════════════════════════════════════════════════════════
    with tabs[1]:

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Ce qui a été atteint</h2>", unsafe_allow_html=True)

            conformite = [
                ("Variable cible |ΔTCH(t+30min)|", "✅"),
                ("Pas de 30 min, UTC strict", "✅"),
                ("Encodages cycliques sin/cos", "✅"),
                ("Baseline naïve avant ML", "✅"),
                ("Découpage chronologique sans fuite", "✅"),
                ("MAE + détection Q90", "✅"),
                ("Interprétabilité SHAP", "✅"),
            ]
            for exigence, statut in conformite:
                color = "#1abc9c" if statut == "✅" else "#aaa"
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center;
                            margin-bottom:0.3rem; padding:0.3rem 0.8rem;
                            background:#f8f9fd; border-radius:6px;">
                    <span style="color:#444; font-size:0.85rem;">{exigence}</span>
                    <span style="font-size:0.95rem; min-width:30px; text-align:right;">{statut}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>3 apports enrichissants</h2>", unsafe_allow_html=True)

            apports = [
                ("Clustering géographique",
                 "5 communes représentatives pondérées par le parc PV installé",
                 "#0f3460"),
                ("Clear Sky Index (CSI)",
                 "Impact des nuages indépendant de la position du soleil",
                 "#0f3460"),
                ("Ratio TCH / GHI",
                 "Signal candidat d'écrêtement / saturation onduleurs",
                 "#0f3460"),
            ]
            for titre, desc, color in apports:
                st.markdown(f"""
                <div style="margin-bottom:0.7rem; padding:0.7rem 1rem;
                            border-left:4px solid {color}; background:#f8f9fd;
                            border-radius:8px;">
                    <div style="font-weight:700; color:{color}; margin-bottom:0.2rem; font-size:0.95rem;">{titre}</div>
                    <div style="color:#555; font-size:0.82rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # ── Limites ──
        st.markdown("<div class='slide-section'><h2>Les 11 % incompressibles</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Phénomènes observés mais non explicables par la météo :**")
            limites = [
                ("Écrêtement production",
                 "Production coupée pour raisons réseau — invisible dans les données météo"),
                ("Saturation onduleurs",
                 "Oscillations rapides décorrélées de la météo"),
                ("Micro-météo locale",
                 "5 points ne capturent pas tous les phénomènes spatiaux"),
            ]
            for titre, desc in limites:
                st.markdown(f"""
                <div style="margin-bottom:0.5rem; padding:0.5rem 0.8rem; background:#eafaf1;
                            border-left:3px solid #1abc9c; border-radius:6px;">
                    <span style="font-weight:700; color:#0e6655; font-size:0.85rem;">{titre}</span>
                    <span style="color:#555; font-size:0.82rem;"> — {desc}</span>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("**Choix de conception :**")
            choix = [
                ("Cible en valeur absolue", "Intensité de la variation, pas sa direction"),
                ("Horizon fixe 30 min", "Pas de prévision multi-horizon"),
                ("Agrégation régionale", "Perte de la variabilité spatiale fine"),
            ]
            for titre, desc in choix:
                st.markdown(f"""
                <div style="margin-bottom:0.5rem; padding:0.5rem 0.8rem; background:#eafaf1;
                            border-left:3px solid #1abc9c; border-radius:6px;">
                    <span style="font-weight:700; color:#0e6655; font-size:0.85rem;">{titre}</span>
                    <span style="color:#555; font-size:0.82rem;"> — {desc}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 2 : Perspectives
    # ══════════════════════════════════════════════════════════════════════════
    with tabs[2]:

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Améliorations identifiées</h2>", unsafe_allow_html=True)

            ameliorations = [
                "Prévision multi-horizon (30 min, 1 h, 2 h)",
                "Extension à d'autres régions françaises",
                "Intégration de prévisions météorologiques opérationnelles",
                "Utilisation de données de production plus fines spatialement",
                "Allègement du modèle — suppression des variables les moins pertinentes absentes du top 20 SHAP",
            ]
            for item in ameliorations:
                st.markdown(f"""
                <div style="margin-bottom:0.5rem; padding:0.5rem 0.8rem;
                            background:#f0f4fa; border-radius:8px;">
                    <span style="color:#0f3460; font-size:0.9rem;">• {item}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Valeur métier</h2>", unsafe_allow_html=True)

            st.markdown("""
Pour un opérateur réseau, une telle approche pourrait contribuer à :
            """)

            ouvertures = [
                "Anticiper les rampes critiques",
                "Améliorer la conduite préventive du réseau",
                "Réduire les contraintes liées à l'intermittence des ENR",
                "Mieux préparer les mécanismes d'ajustement et de flexibilité",
            ]
            for item in ouvertures:
                st.markdown(f"""
                <div style="margin-bottom:0.5rem; padding:0.5rem 0.8rem;
                            background:#eafaf1; border-radius:8px;">
                    <span style="color:#0e6655; font-size:0.9rem;">• {item}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
