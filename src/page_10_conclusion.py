import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils import slide_header, kpi, callout, formula


def page_conclusion():
    slide_header(
        "Conclusion & Perspectives",
        "Bilan du projet · Lecture métier des résultats · Roadmap EVI"
    )

    tabs = st.tabs([
        "Bilan & Lecture métier",
        "Limites structurelles",
        "Perspectives & Roadmap",
    ])

    # ── Tab 0 : Bilan & Lecture métier ───────────────────────────────────────
    with tabs[0]:

        st.markdown("""<div class='kpi-row'>""" +
            kpi("0.467", "MAE test", "") +
            kpi("0.89", "R² test", "green") +
            kpi("85.5%", "Recall rampes (seuil opt.)", "accent") +
            kpi("14.5%", "Rampes critiques manquées", "orange") +
        """</div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Pourquoi R² = 0.89 est un bon résultat</h2>", unsafe_allow_html=True)
            st.markdown("""
Le R² mesure la **part de variance expliquée**. Atteindre **0.89 sur la variabilité** — et non sur la production elle-même — est remarquable.

La variabilité est par nature le **signal résiduel le plus difficile à prédire** : ce qui échappe à la tendance, aux cycles, à la saisonnalité. Prédire la production moyenne atteindrait probablement 0.97+ sans effort, mais ne servirait à rien opérationnellement.

> Ce projet prédit ce qui est difficile à prévoir — et le fait bien.
            """)
            callout("""
Les 11% d'erreur restants ne sont pas un échec du modèle.<br>
Ce sont des phénomènes <strong>structurellement absents des données</strong> :
curtailment, saturation des onduleurs, événements météo très locaux.
Le modèle ne peut pas apprendre ce qu'il ne voit pas.
            """, "warn")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Le vrai choix : recall vs précision</h2>", unsafe_allow_html=True)
            st.markdown("""
Le projet propose deux régimes opérationnels — **le choix appartient à l'opérateur réseau**, pas au data scientist :
            """)

            df_seuils = pd.DataFrame({
                "Seuil": ["Q90 = 8.04", "Optimisé = 7.37"],
                "Recall": ["76.6%", "85.5%"],
                "Précision": ["81.9%", "67.7%"],
                "Traduction opérationnelle": [
                    "Peu de fausses alertes — mobilisation ciblée",
                    "Moins de rampes manquées — couverture maximale"
                ]
            })
            st.dataframe(df_seuils, use_container_width=True, hide_index=True)

            callout("""
<strong>Ce n'est pas un problème mathématique — c'est une décision économique.</strong><br>
Quel est le coût d'une rampe non détectée (risque réseau, délestage) versus une fausse alerte
(mobilisation inutile d'une centrale de réserve) ?
Si une rampe manquée coûte 10x plus qu'une fausse alerte — seuil optimisé.
            """, "info")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='slide-section'><h2>Ce que ce projet livre réellement</h2>", unsafe_allow_html=True)
        st.markdown("""
> **"Nous avons construit un système d'alerte, pas un modèle de prédiction parfait.
> La perfection n'est pas atteignable car une partie des variations a des causes institutionnelles
> et techniques invisibles dans les données météo.
> Mais 85% de détection des rampes critiques avec 30 minutes d'avance, c'est un outil réellement utile —
> et le choix du seuil d'alerte appartient à l'opérateur, pas au data scientist."**
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 1 : Limites structurelles ────────────────────────────────────────
    with tabs[1]:

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Les 11% incompressibles</h2>", unsafe_allow_html=True)
            st.markdown("""
Ces erreurs ne sont **pas dues au modèle** — elles reflètent des phénomènes absents des données d'entraînement :
            """)

            limites = [
                ("Curtailment (écrêtage RTE)",
                 "Quand RTE coupe la production car le réseau est saturé, la production chute brutalement alors que le rayonnement est maximum. Le modèle voit GHI élevé + CSI proche de 1 et prédit stabilité. Mais la production s'effondre pour une raison institutionnelle invisible dans les données météo.",
                 "#e94560"),
                ("Saturation des onduleurs",
                 "Les onduleurs ont une puissance de coupure maximale. Par très fort ensoleillement, ils se coupent automatiquement puis redémarrent — générant des oscillations rapides totalement décorrélées de la météo.",
                 "#f39c12"),
                ("Événements météo très locaux",
                 "Cellule orageuse isolée, effet de brise thermique... Les 5 points représentatifs ne capturent pas tous les micro-phénomènes spatiaux.",
                 "#0f3460"),
            ]

            for titre, desc, color in limites:
                st.markdown(f"""
                <div style="margin-bottom:1rem; padding:0.8rem 1rem; border-left:4px solid {color}; background:#f8f9fd; border-radius:8px;">
                    <div style="font-weight:700; color:{color}; margin-bottom:0.3rem;">{titre}</div>
                    <div style="color:#555; font-size:0.88rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Le signal TCH/GHI — un détecteur candidat</h2>", unsafe_allow_html=True)
            st.markdown("""
Le projet a anticipé partiellement ces phénomènes avec le **ratio TCH/GHI** construit en feature engineering :
            """)
            formula("R_TCH/GHI(t) = TCH_solaire(t) / GHI_region(t)")
            st.markdown("""
Quand le GHI est élevé mais ce ratio est faible : production anormalement basse, signal candidat de curtailment ou de saturation onduleur.

**Ce ratio n'est pas une étiquette certaine** — c'est une variable candidate dont la pertinence est laissée au modèle. Approche honnête : on ne sur-interprète pas les données disponibles.
            """)
            callout("""
Pour aller plus loin :<br>
- Données de curtailment RTE (existent, non publiques à granularité fine)<br>
- Données techniques des parcs (puissance crête, type d'onduleurs)<br>
- Détecter ces épisodes via TCH/GHI et les <strong>exclure de l'entraînement</strong>
pour un modèle plus pur sur la variabilité atmosphérique
            """, "warn")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='slide-section'><h2>Limites de conception</h2>", unsafe_allow_html=True)
            st.markdown("""
| Limite | Impact |
|---|---|
| Cible en valeur absolue (pas de signe) | On prédit l'intensité, pas la direction |
| Horizon fixe à 30 min | Pas de prédiction multi-horizon |
| Agrégation régionale RTE | Perd la variabilité spatiale interne |
| Données NASA POWER (vent, temp., nébulosité) à résolution 1h interpolées à 30 min | Bruit théorique aux transitions — **atténué en pratique** : ces variables n'apparaissent pas dans le top 20 de la permutation importance ; le modèle s'appuie principalement sur les variables CAMS (15 min natif, agrégées par sommation) |
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2 : Perspectives & Roadmap ───────────────────────────────────────
    with tabs[2]:

        st.markdown("<div class='slide-section'><h2>Le projet soumis : indicateur EVI</h2>", unsafe_allow_html=True)
        st.markdown("""
Le projet soumis à DataScientest visait à construire un **indicateur EVI (Energy Volatility & Instability)**,
inspiré du **VIX financier** — l'indice de volatilité des marchés — mais adapté aux énergies renouvelables,
à partir de données ouvertes exclusivement.

**Ce projet livre EVI-T** — le premier jalon, solide et cohérent. Les trois autres composantes constituent la roadmap naturelle.
        """)

        evi_data = [
            ("EVI-T", "Dynamique Temporelle", "Livré", "Variabilité observée sur données ouvertes météo + production. Pipeline complet, modèle ExtraTrees, R²=0.89.", "#1abc9c"),
            ("EVI-M", "Biais Météo", "Jalon 2", "Écart entre prévision météo NWP et production réelle. Nécessite Météo-France ou ECMWF opérationnel.", "#f39c12"),
            ("EVI-R", "Volatilité Résiduelle", "Jalon 3", "Incertitudes structurelles non capturées par la physique — données Enedis par commune.", "#0f3460"),
            ("EVI-S", "Signaux Réseau & Marché", "Jalon 4", "EPEX SPOT, mécanisme d'ajustement RTE, qualité fréquence, NEBEF. Intégration temporelle complexe.", "#e94560"),
        ]

        for code, nom, statut, desc, color in evi_data:
            badge_color = "#1abc9c" if statut == "Livré" else "#aaa"
            st.markdown(f"""
            <div style="margin-bottom:1rem; padding:1rem 1.2rem; border-left:5px solid {color}; background:#f8f9fd; border-radius:10px; display:flex; align-items:flex-start; gap:1rem;">
                <div style="min-width:70px; text-align:center;">
                    <div style="font-size:1.3rem; font-weight:800; color:{color};">{code}</div>
                    <div style="font-size:0.7rem; background:{badge_color}; color:white; border-radius:10px; padding:2px 6px; margin-top:4px;">{statut}</div>
                </div>
                <div>
                    <div style="font-weight:700; color:#1a1a2e; margin-bottom:0.2rem;">{nom}</div>
                    <div style="color:#555; font-size:0.87rem;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='slide-section'><h2>Pourquoi EVI-M, R, S n'ont pas été livrés</h2>", unsafe_allow_html=True)
        st.markdown("""
Les sources de données n'étaient pas absentes — elles existent presque toutes sur des plateformes ouvertes.
Le problème était la **complexité d'intégration temporelle** :
        """)

        obstacles = [
            ("Enedis par commune", "Données annuelles — inutilisables comme feature à 30 min"),
            ("Prix EPEX SPOT", "Horaires ou quart-horaires, avec conventions de timezone qui varient entre les marchés"),
            ("Fréquence réseau RTE", "Données sous-minutées, nécessitant un travail d'agrégation non trivial"),
            ("Mécanisme d'ajustement", "Entrées asynchrones — les activations ne tombent pas régulièrement"),
        ]
        for source, probleme in obstacles:
            st.markdown(f"""
            <div style="display:flex; gap:1rem; margin-bottom:0.5rem; padding:0.5rem 0.8rem; background:#f8f9fd; border-radius:6px; border-left:3px solid #e94560;">
                <span style="font-weight:700; color:#0f3460; min-width:180px;">{source}</span>
                <span style="color:#555; font-size:0.88rem;">{probleme}</span>
            </div>
            """, unsafe_allow_html=True)

        callout("""
Aligner tout cela avec une série cible à 30 min UTC sur 5 ans représente 3 à 4 semaines de travail supplémentaire.
Nous avons préféré un pipeline cohérent sur la composante physique à un assemblage fragile de sources hétérogènes.
<strong>CAMS et NASA POWER</strong> — APIs bien documentées, en UTC, gratuites et stables (CAMS : 15 min natif · NASA POWER : 1h interpolé) —
ont permis de construire un pipeline propre, reproductible et documenté.
        """, "info")
        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Améliorations techniques identifiées</h2>", unsafe_allow_html=True)
            ameliorations = [
                ("Multi-horizon", "Prédire à 30 min, 1h, 2h simultanément — un seul modèle multi-output"),
                ("Résolution spatiale", "Passer de 5 points à une grille fine avec données Enedis par commune"),
                ("CNN / LSTM", "Exploiter la structure temporelle des séries — les fenêtres glissantes actuelles sont une approximation"),
                ("Labellisation curtailment", "Détecter et exclure les épisodes d'écrêtage via TCH/GHI pour un modèle plus pur"),
                ("Allègement du pipeline d'inférence", "Température, vent, humidité et nébulosité (NASA POWER) n'apparaissent pas dans le top de la permutation importance — une sélection explicite supprimerait la dépendance à cette API en production, sans perte de performance"),
                ("Données NWP", "Intégrer les prévisions météo opérationnelles (ECMWF open data) comme feature"),
            ]
            for titre, desc in ameliorations:
                st.markdown(f"""
                <div style="margin-bottom:0.6rem; padding:0.6rem 0.8rem; background:#f0f4fa; border-radius:8px;">
                    <span style="font-weight:700; color:#0f3460;">{titre}</span>
                    <span style="color:#555; font-size:0.87rem;"> — {desc}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Vers un usage opérationnel réel</h2>", unsafe_allow_html=True)
            st.markdown("""
**Sources internes (opérateur réseau) :**
- Données Enedis de production par commune — meilleure cible spatiale
- Données de curtailment RTE — nettoyer les labels d'entraînement
- Historique des incidents réseau — feature contextuelle

**Croisement avec les marchés :**
- Prix EPEX SPOT intraday — signal de tension système
- Mécanisme d'ajustement RTE — proxy de déséquilibre réseau
- Qualité de fréquence — indicateur temps réel de l'équilibre offre/demande
            """)
            callout("""
<strong>La leçon centrale :</strong><br>
La cohérence temporelle des données prime sur la richesse des sources.
Ce projet est le premier jalon d'une roadmap plus large —
ce que nous avions imaginé, ce que les données nous ont permis de faire,
et ce que ça ouvre.
            """, "info")
            st.markdown("</div>", unsafe_allow_html=True)
