import streamlit as st
from pathlib import Path
from utils import slide_header, section, kpi, callout, step_badge

def page_accueil():
    slide_header(
        "Variabilité de la Production Photovoltaïque",
        "Analyse et prédiction · Région PACA · Données ouvertes · Pas de temps 30 minutes · 2020–2025"
    )

    tabs = st.tabs(["Contexte & Objectif", "Démarche", "Équipe & Périmètre"])

    # ── Tab 0 : Contexte & Objectif ──────────────────────────────────────────
    with tabs[0]:
        st.markdown("""<div class='kpi-row'>""" +
            kpi("5 ans", "Période d'analyse", "") +
            kpi("30 min", "Résolution temporelle", "accent") +
            kpi("~87 K", "Obs. train+valid", "green") +
            kpi("5 pts", "Points géographiques", "orange") +
        """</div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Pourquoi ce projet ?</h2>", unsafe_allow_html=True)
            st.markdown("""
La production photovoltaïque représente aujourd'hui une part croissante du mix électrique en région PACA.
Cette croissance est une bonne nouvelle pour la transition énergétique — mais elle crée de nouvelles contraintes opérationnelles pour les gestionnaires de réseau.

Un passage nuageux peut faire chuter la production régionale de plusieurs dizaines de MW en quelques minutes.
Ces **rampes critiques** déséquilibrent le réseau et contraignent les opérateurs à mobiliser des réserves coûteuses en temps réel, sans préavis suffisant.

**Les outils existants ne répondent pas à ce besoin :**
            """)

            outils = [
                ("Prévision de production RTE", "Prédit les niveaux de production à horizon day-ahead. Ne détecte pas les rampes critiques intraday.", "#f39c12"),
                ("Littérature sur la volatilité", "Documente l'impact sur les marchés et les prix. Ne propose pas d'outil d'anticipation opérationnel.", "#f39c12"),
                ("Données météo standard", "Disponibles mais non transformées en signal d'alerte réseau à 30 minutes.", "#f39c12"),
            ]
            for titre, desc, color in outils:
                st.markdown(f"""
                <div style="margin-bottom:0.5rem; padding:0.5rem 0.8rem; border-left:3px solid {color}; background:#fffbf0; border-radius:6px;">
                    <span style="font-weight:700; color:#444; font-size:0.88rem;">{titre}</span>
                    <span style="color:#777; font-size:0.85rem;"> — {desc}</span>
                </div>
                """, unsafe_allow_html=True)

            img_path = Path(__file__).parent / "images" / "Evolution_de_la_production_solaire_en_France__2026-06-07.png"
            if img_path.exists():
                st.image(str(img_path), caption="Évolution de la production solaire photovoltaïque en France (source : RTE)")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Ce que ce projet apporte</h2>", unsafe_allow_html=True)
            st.markdown("""
Ce projet construit un **système d'alerte opérationnel** : à partir de données météo et de production ouvertes,
il prédit si la production photovoltaïque va connaître une variation forte dans les **30 prochaines minutes**,
et déclenche une alerte si cette variation dépasse un seuil critique calibré sur des données réelles.

**Trois caractéristiques qui le rendent opérationnel :**
            """)

            apports = [
                ("Anticipation à 30 minutes",
                 "Horizon aligné sur les cycles d'ajustement RTE — suffisant pour mobiliser des réserves.",
                 "#1abc9c"),
                ("Seuil calibré sur données réelles",
                 "Q90 = 8% de variation du taux de charge en 30 min — calculé sur 5 ans de production PACA réelle, pas une valeur théorique.",
                 "#1abc9c"),
                ("Choix du niveau de risque laissé à l'opérateur",
                 "Deux régimes : peu de fausses alertes (précision 82%) ou détection maximale (recall 85%). L'arbitrage appartient au gestionnaire de réseau, pas au modèle.",
                 "#1abc9c"),
            ]
            for titre, desc, color in apports:
                st.markdown(f"""
                <div style="margin-bottom:0.8rem; padding:0.7rem 1rem; border-left:4px solid {color}; background:#f0fdf4; border-radius:8px;">
                    <div style="font-weight:700; color:#0e6655; font-size:0.9rem; margin-bottom:0.2rem;">{titre}</div>
                    <div style="color:#555; font-size:0.85rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

            callout("""
<strong>📐 Pourquoi le TCH plutôt que les MW absolus ?</strong><br><br>
Le <strong>TCH (Taux de Charge solaire)</strong> = production observée / capacité installée, en %.<br>
La capacité PV en PACA croît chaque année : un seuil d'alerte en MW perd son sens d'une année à l'autre.
Travailler en TCH rend le modèle <strong>indépendant de la taille du parc</strong> — Lindas et al. (2025, EDF R&D) le confirme expérimentalement.<br><br>
Deux autres avantages : les variations relatives sont <strong>comparables entre saisons et heures</strong> (robustesse aux effets de niveau) ;
et une rampe de +10% ou −10% a le <strong>même impact sur le réseau</strong> — c'est l'amplitude |ΔTCH| qui compte, pas le signe.
            """, "info")

            callout("""
Ce n'est pas une étude académique sur la variabilité solaire.
C'est un outil conçu pour qu'un opérateur réseau puisse l'utiliser —
<strong>85% des rampes critiques détectées avec 30 minutes d'avance,
sur la base de données entièrement ouvertes.</strong>
            """, "success")
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Positionnement scientifique ──
        st.markdown("<div class='slide-section'><h2>Ce que la littérature ne propose pas</h2>", unsafe_allow_html=True)
        st.markdown("""
La littérature scientifique récente documente abondamment l'impact des renouvelables
sur les marchés et les réseaux (Kiesel & Paraschiv 2017, Kulakov 2019, Cramer et al. 2022, ACER 2023) :
volatilité des prix intraday, propagation des erreurs de prévision, instabilité de la charge résiduelle.
Ces travaux **mesurent la volatilité comme un effet** — ils ne proposent pas d'outil pour l'anticiper.
        """)

        st.markdown("""
<div style="display:flex; gap:0.8rem; margin:0.8rem 0; flex-wrap:wrap; align-items:stretch;">
    <div style="flex:1; min-width:180px; padding:0.8rem 1rem; background:#fff3cd; border-radius:10px; border-top:3px solid #f39c12; text-align:center;">
        <div style="font-weight:700; color:#f39c12; font-size:0.85rem; margin-bottom:0.3rem;">Littérature académique</div>
        <div style="color:#555; font-size:0.82rem;">Mesure la volatilité <em>après coup</em> comme effet sur les prix et les réseaux</div>
    </div>
    <div style="display:flex; align-items:center; font-size:1.4rem; color:#ccc; padding:0 0.3rem;">→</div>
    <div style="flex:1.2; min-width:200px; padding:0.8rem 1rem; background:#eafaf1; border-radius:10px; border-top:3px solid #1abc9c; text-align:center;">
        <div style="font-weight:700; color:#1abc9c; font-size:0.85rem; margin-bottom:0.3rem;">Ce projet</div>
        <div style="color:#555; font-size:0.82rem;"><strong>Anticipe</strong> la variabilité physique à 30 min · seuil calibré · données ouvertes · choix opérateur</div>
    </div>
    <div style="display:flex; align-items:center; font-size:1.4rem; color:#ccc; padding:0 0.3rem;">←</div>
    <div style="flex:1; min-width:180px; padding:0.8rem 1rem; background:#eaf4ff; border-radius:10px; border-top:3px solid #0f3460; text-align:center;">
        <div style="font-weight:700; color:#0f3460; font-size:0.85rem; margin-bottom:0.3rem;">Prévision de production</div>
        <div style="color:#555; font-size:0.82rem;">Prédit les niveaux de production — domaine mature, bien investi</div>
    </div>
</div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 1 : Démarche ─────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown("<div class='slide-section'><h2>Pipeline méthodologique</h2>", unsafe_allow_html=True)

        steps = [
            ("1", "Cadrage de l'étude", "Positionnement scientifique, cadrage DataScientest, clustering géographique PACA"),
            ("2", "Collecte de données", "RTE éCO2mix (production), CAMS (atmosphère), Open-Meteo (météo), données astronomiques"),
            ("3", "Analyse exploratoire", "Distribution de la cible, saisonnalités, corrélations, identification des rampes"),
            ("4", "Feature Engineering", "Encodages cycliques (sin/cos), lags temporels, statistiques glissantes, CSI, agrégation régionale"),
            ("5", "Modélisation & Interprétabilité", "Baseline naïve — modèles linéaires — arbres — boosting · ExtraTreesRegressor final · SHAP"),
        ]

        for num, title, desc in steps:
            st.markdown(f"""
            <div style="display:flex; align-items:flex-start; gap:1rem; margin-bottom:1rem; padding:1rem; background:#f8f9fd; border-radius:10px; border-left:4px solid #0f3460;">
                <div style="font-size:1.4rem; font-weight:800; color:#e94560; min-width:32px; text-align:center;">{num}</div>
                <div>
                    <div style="font-weight:700; color:#0f3460; font-size:1rem;">{title}</div>
                    <div style="color:#555; font-size:0.9rem; margin-top:0.2rem;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        callout("Leçon clé : la cohérence temporelle des données prime sur la richesse des sources — choix méthodologique central du projet.", "info")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='slide-section'><h2>Sources de données</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Production PV**")
            st.markdown("- RTE éCO2mix\n- Pas 30 min\n- Maille régionale PACA\n- 2020–2025")
        with col2:
            st.markdown("**Atmosphère & Météo**")
            st.markdown("- CAMS (Copernicus)\n- Open-Meteo\n- 5 points géographiques\n- Irradiance, nuages, aérosols")
        with col3:
            st.markdown("**Astronomie**")
            st.markdown("- Calculs pvlib\n- Azimut, élévation solaire\n- Angle zénithal\n- GHI ciel clair")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2 : Équipe & Périmètre ────────────────────────────────────────────
    with tabs[2]:
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
                <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.8rem; padding:0.8rem 1rem; border-radius:10px; border-left:4px solid {color}; background:#f8f9fd;">
                    <div style="font-weight:700; color:{color}; min-width:160px;">{nom}</div>
                    <div style="color:#555; font-size:0.9rem;">{role}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Périmètre réalisé</h2>", unsafe_allow_html=True)
            st.markdown("""
| Paramètre | Valeur |
|---|---|
| **Région** | Provence-Alpes-Côte d'Azur |
| **Période** | Janvier 2020 – Janvier 2025 |
| **Résolution** | 30 minutes |
| **Points géo** | 5 communes représentatives |
| **Horizon de prédiction** | +30 min |
| **Cible** | Amplitude variation TCH (Taux de Charge) |
            """)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='slide-section'><h2>Trajectoire du projet — 3 temps</h2>", unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-bottom:1.2rem; padding:1rem 1.2rem; border-left:5px solid #e94560; background:#fff5f7; border-radius:10px;">
            <div style="font-weight:800; color:#e94560; font-size:1rem; margin-bottom:0.5rem;">Temps 1 — La vision initiale : indicateur EVI</div>
            <div style="color:#444; font-size:0.9rem;">
            Le projet soumis à DataScientest visait à construire un <strong>indicateur EVI (Energy Volatility &amp; Instability)</strong>,
            inspiré du <strong>VIX financier</strong> — l'indice de volatilité des marchés — adapté aux énergies renouvelables.
            Quatre composantes, neuf sources de données incluant EPEX SPOT, le mécanisme d'ajustement RTE, la qualité de fréquence et les données Enedis.
            </div>
        </div>
        """, unsafe_allow_html=True)

        evi_items = [
            ("EVI-M", "Biais entre prévision météo et production réelle"),
            ("EVI-T", "Dynamique temporelle de la variabilité"),
            ("EVI-R", "Volatilité résiduelle liée aux incertitudes structurelles"),
            ("EVI-S", "Volatilité intégrant signaux réseau et marché (EPEX SPOT, mécanisme d'ajustement RTE)"),
        ]
        for code, desc in evi_items:
            color = "#1abc9c" if code == "EVI-T" else "#ccc"
            st.markdown(f"""
            <div style="display:flex; gap:0.8rem; align-items:center; margin-bottom:0.3rem; padding:0.4rem 0.8rem; background:#f8f9fd; border-radius:6px; border-left:3px solid {color};">
                <span style="font-weight:800; color:{color}; min-width:60px;">{code}</span>
                <span style="color:#555; font-size:0.88rem;">{desc}</span>
                {"<span style='margin-left:auto; background:#1abc9c; color:white; font-size:0.72rem; padding:2px 8px; border-radius:10px;'>Livré</span>" if code == "EVI-T" else ""}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-bottom:1.2rem; padding:1rem 1.2rem; border-left:5px solid #f39c12; background:#fffbf0; border-radius:10px;">
            <div style="font-weight:800; color:#f39c12; font-size:1rem; margin-bottom:0.5rem;">Temps 2 — Le recadrage méthodologique DataScientest</div>
            <div style="color:#444; font-size:0.9rem; margin-bottom:0.8rem;">
            Le canevas méthodologique fourni par DataScientest a recentré le projet sur la variabilité physique,
            avec une variable cible précise, une baseline naïve obligatoire et une rigueur temporelle stricte.
            Ce recadrage a été une force : il a imposé une cohérence que la vision initiale n'aurait pas garantie.
            </div>
        </div>
        """, unsafe_allow_html=True)

        conformite = [
            ("Variable cible V(t) = |P(t)−P(t−1)| / P_capacité", "Conforme", "#1abc9c"),
            ("Pas de 30 min, alignement UTC strict", "Conforme", "#1abc9c"),
            ("Encodages sin/cos heure et jour de l'année", "Conforme", "#1abc9c"),
            ("Baseline naïve physique avant tout ML", "Conforme", "#1abc9c"),
            ("Découpage train/val/test sans fuite temporelle", "Conforme", "#1abc9c"),
            ("MAE principale + détection Q90 métier", "Conforme", "#1abc9c"),
            ("Interprétabilité SHAP exigée", "Conforme", "#1abc9c"),
            ("Horizon multi-step V(t+2), V(t+4) optionnel", "Non réalisé", "#aaa"),
        ]
        for item, statut, color in conformite:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.25rem; padding:0.35rem 0.8rem; background:#f8f9fd; border-radius:6px;">
                <span style="color:#444; font-size:0.85rem;">{item}</span>
                <span style="font-size:0.75rem; font-weight:700; color:{color}; min-width:90px; text-align:right;">{statut}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-bottom:1.2rem; padding:1rem 1.2rem; border-left:5px solid #0f3460; background:#f0f4fa; border-radius:10px;">
            <div style="font-weight:800; color:#0f3460; font-size:1rem; margin-bottom:0.5rem;">Temps 3 — Ce que l'analyse exploratoire a révélé</div>
            <div style="color:#444; font-size:0.9rem; margin-bottom:0.8rem;">
            En travaillant sur les données, trois contributions non prévues dans le canevas ont émergé naturellement.
            Ce sont elles qui donnent au projet son originalité.
            </div>
        </div>
        """, unsafe_allow_html=True)

        decouvertes = [
            ("Clustering géographique",
             "Non prévu dans le canevas. La contrainte RTE à maille régionale a imposé la question : où collecter les données météo ? "
             "La réponse — 5 communes représentatives pondérées par le parc PV installé — est devenue l'une des parties les plus originales du projet.",
             "#0f3460"),
            ("Clear Sky Index (CSI)",
             "Non mentionné dans le canevas. Le CSI mesure l'écart entre le rayonnement observé et le rayonnement théorique par ciel clair. "
             "Il capture directement l'impact des nuages sur la variabilité, indépendamment de la position du soleil.",
             "#0f3460"),
            ("Ratio TCH/GHI — signal candidat de curtailment",
             "Non demandé. Construit en feature engineering pour détecter les situations où la production est anormalement basse "
             "par rapport à l'irradiance disponible — signal candidat d'écrêtage réseau ou de saturation d'onduleurs.",
             "#0f3460"),
        ]

        for titre, desc, color in decouvertes:
            st.markdown(f"""
            <div style="margin-bottom:0.8rem; padding:0.8rem 1rem; border-left:4px solid {color}; background:#f8f9fd; border-radius:8px;">
                <div style="font-weight:700; color:{color}; margin-bottom:0.3rem;">{titre}</div>
                <div style="color:#555; font-size:0.87rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        callout("""
Ce projet n'est pas un projet réduit par rapport à la vision initiale.
C'est un projet qui a suivi un cadre scientifique rigoureux, l'a respecté intégralement,
et l'a enrichi là où la réalité des données l'imposait.
EVI-T livré est le premier jalon solide d'une roadmap plus large.
        """, "info")
        st.markdown("</div>", unsafe_allow_html=True)
