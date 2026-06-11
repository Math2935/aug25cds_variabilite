import streamlit as st
import pandas as pd

from utils import slide_header, kpi, callout


def page_conclusion():
    slide_header(
        "Conclusion & Perspectives",
        "Bilan · Conformité au cadre · Limites · Pistes d'amélioration"
    )

    tabs = st.tabs([
        "Bilan",
        "Ce qui a été atteint",
        "Limites",
        "Perspectives",
    ])

    # ── Tab 0 : Bilan ────────────────────────────────────────────────────────
    with tabs[0]:

        st.markdown("""<div class='kpi-row'>""" +
            kpi("0.467", "MAE test", "") +
            kpi("0.89", "R² test", "green") +
            kpi("85.5%", "Recall (seuil opt.)", "accent") +
            kpi("14.5%", "Rampes manquées", "orange") +
        """</div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Ce que le modèle atteint</h2>", unsafe_allow_html=True)
            st.markdown("""
- **R² = 0.89 sur la variabilité** — pas sur la production elle-même
- Variabilité = signal résiduel, le plus dur à prédire
- 11 % restants = phénomènes absents des données ouvertes
  (curtailment, onduleurs, micro-météo)
            """)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Recall vs Précision</h2>", unsafe_allow_html=True)
            st.markdown("**Deux régimes — le choix appartient à l'opérateur :**")

            df_seuils = pd.DataFrame({
                "Seuil": ["Q90 = 8.04", "Optimisé = 7.37"],
                "Recall": ["76.6 %", "85.5 %"],
                "Précision": ["81.9 %", "67.7 %"],
                "Traduction": [
                    "Peu de fausses alertes",
                    "Détection maximale"
                ]
            })
            st.dataframe(df_seuils, use_container_width=True, hide_index=True)

            callout("""
<strong>Décision économique :</strong> coût d'une rampe manquée
vs coût d'une fausse alerte ?
            """, "info")
            st.markdown("</div>", unsafe_allow_html=True)

        callout("""
<strong>85 % des rampes critiques détectées avec 30 minutes d'avance,
sur données ouvertes exclusivement.</strong>
        """, "success")

    # ── Tab 1 : Ce qui a été atteint ─────────────────────────────────────────
    with tabs[1]:

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Conformité au cadre méthodologique</h2>", unsafe_allow_html=True)

            conformite = [
                ("Variable cible |ΔTCH(t+30min)|", "✅"),
                ("Pas de 30 min, UTC strict", "✅"),
                ("Encodages cycliques sin/cos", "✅"),
                ("Baseline naïve avant ML", "✅"),
                ("Découpage chronologique sans fuite", "✅"),
                ("MAE + détection Q90", "✅"),
                ("Interprétabilité SHAP", "✅"),
                ("Multi-step optionnel", "❌"),
            ]
            for exigence, statut in conformite:
                color = "#1abc9c" if statut == "✅" else "#aaa"
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center;
                            margin-bottom:0.3rem; padding:0.4rem 0.8rem;
                            background:#f8f9fd; border-radius:6px;">
                    <span style="color:#444; font-size:0.88rem;">{exigence}</span>
                    <span style="font-size:1rem; min-width:30px; text-align:right;">{statut}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>3 apports non prévus dans le canevas</h2>", unsafe_allow_html=True)

            apports = [
                ("Clustering géographique",
                 "5 communes représentatives pondérées par le parc PV installé",
                 "#0f3460"),
                ("Clear Sky Index (CSI)",
                 "Impact des nuages indépendant de la position du soleil",
                 "#0f3460"),
                ("Ratio TCH / GHI",
                 "Signal candidat de curtailment / saturation onduleurs",
                 "#0f3460"),
            ]
            for titre, desc, color in apports:
                st.markdown(f"""
                <div style="margin-bottom:0.8rem; padding:0.8rem 1rem;
                            border-left:4px solid {color}; background:#f8f9fd;
                            border-radius:8px;">
                    <div style="font-weight:700; color:{color}; margin-bottom:0.2rem;">{titre}</div>
                    <div style="color:#555; font-size:0.88rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

            callout("""
Cadre rigoureux respecté intégralement,
<strong>enrichi là où les données l'imposaient.</strong>
            """, "info")
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2 : Limites ──────────────────────────────────────────────────────
    with tabs[2]:

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Les 11 % incompressibles</h2>", unsafe_allow_html=True)

            limites = [
                ("Curtailment RTE",
                 "Production coupée pour raisons réseau — invisible dans les données météo",
                 "#e94560"),
                ("Saturation onduleurs",
                 "Oscillations rapides décorrélées de la météo",
                 "#f39c12"),
                ("Micro-météo locale",
                 "5 points ne capturent pas tous les phénomènes spatiaux",
                 "#0f3460"),
            ]
            for titre, desc, color in limites:
                st.markdown(f"""
                <div style="margin-bottom:0.8rem; padding:0.8rem 1rem;
                            border-left:4px solid {color}; background:#f8f9fd;
                            border-radius:8px;">
                    <div style="font-weight:700; color:{color}; margin-bottom:0.2rem;">{titre}</div>
                    <div style="color:#555; font-size:0.88rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Limites de conception</h2>", unsafe_allow_html=True)
            st.markdown("""
| Limite | Impact |
|---|---|
| Cible en valeur absolue | Intensité, pas direction |
| Horizon fixe 30 min | Pas de multi-horizon |
| Agrégation régionale | Perte de variabilité spatiale |
| Météo 1h interpolée | Bruit aux transitions |
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 3 : Perspectives ─────────────────────────────────────────────────
    with tabs[3]:

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Améliorations techniques</h2>", unsafe_allow_html=True)

            ameliorations = [
                ("Multi-horizon", "Prédire à 30 min, 1h, 2h simultanément"),
                ("Résolution spatiale fine", "Données Enedis par commune"),
                ("Architectures séquentielles", "CNN / LSTM sur la structure temporelle"),
                ("Labellisation curtailment", "Détecter et exclure les épisodes via TCH/GHI"),
                ("Prévisions météo en entrée", "Utiliser les prévisions (pas seulement les observations) comme features"),
            ]
            for titre, desc in ameliorations:
                st.markdown(f"""
                <div style="margin-bottom:0.5rem; padding:0.5rem 0.8rem;
                            background:#f0f4fa; border-radius:8px;">
                    <span style="font-weight:700; color:#0f3460;">{titre}</span>
                    <span style="color:#555; font-size:0.88rem;"> — {desc}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Ouvertures métier</h2>", unsafe_allow_html=True)

            ouvertures = [
                ("Prévisions météo opérationnelles", "Mesure du biais prévision / réel"),
                ("Données Enedis communales", "Variabilité locale invisible à maille régionale"),
                ("Prix EPEX SPOT intraday", "Signal de tension système"),
                ("Mécanisme d'ajustement RTE", "Proxy de déséquilibre réseau"),
                ("Qualité de fréquence", "Indicateur temps réel offre / demande"),
            ]
            for titre, desc in ouvertures:
                st.markdown(f"""
                <div style="margin-bottom:0.5rem; padding:0.5rem 0.8rem;
                            background:#f0f4fa; border-radius:8px;">
                    <span style="font-weight:700; color:#0f3460;">{titre}</span>
                    <span style="color:#555; font-size:0.88rem;"> — {desc}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        callout("""
<strong>Outil quantitatif, explicable, reproductible, sur données ouvertes</strong>
— conforme à l'objectif de l'énoncé.
        """, "success")
