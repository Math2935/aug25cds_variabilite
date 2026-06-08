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

    tabs = st.tabs(["Positionnement & Littérature", "Cadrage méthodologique", "Clustering géographique PACA"])

    # ── Tab 0 : Positionnement & Littérature ─────────────────────────────────
    with tabs[0]:
        st.markdown("<div class='slide-section'><h2>Ce que la littérature fait — et ce qu'elle ne fait pas</h2>", unsafe_allow_html=True)
        st.markdown("""
La recherche académique a bien documenté l'impact des énergies renouvelables sur les systèmes électriques.
Mais elle laisse un vide opérationnel important que ce projet cherche à combler.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Prévision de production — domaine mature**")
            refs_prod = [
                ("Lindas, Goude & Ciais (2025)", "Prédiction de la production solaire et éolienne à l'échelle nationale en France via RTE + ERA5 — benchmark ML complet, EDF R&D / CEA"),
                ("De Giorgi et al. (2014)", "Prévision PV par méthodes statistiques — impact des données météo"),
                ("Malvoni et al.", "Prédiction de production d'un parc PV méditerranéen via irradiance et température"),
                ("IRENA (2020)", "Revue des approches avancées de prévision des renouvelables variables"),
            ]
            for ref, desc in refs_prod:
                color_bg = "#e8f4fd" if "Lindas" in ref else "#eaf4ff"
                color_border = "#0f3460"
                st.markdown(f"""
                <div style="margin-bottom:0.4rem; padding:0.4rem 0.8rem; background:{color_bg}; border-left:3px solid {color_border}; border-radius:6px;">
                    <span style="font-weight:700; color:#0f3460; font-size:0.82rem;">{ref}</span>
                    <span style="color:#555; font-size:0.82rem;"> — {desc}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Volatilité des marchés — documentée mais non anticipée**")
            refs_vol = [
                ("Kiesel & Paraschiv (2017)", "Volatilité des prix de marché induite par les renouvelables"),
                ("Kulakov (2019)", "Modèles à régimes pour la volatilité renouvelable"),
                ("Cramer et al. (2022)", "Lien entre précision météo et volatilité intraday"),
                ("ACER (2023)", "Volatilité croissante avec la pénétration renouvelable"),
                ("Fraunhofer ISE (2022)", "Variabilité de la charge résiduelle à échelle journalière"),
            ]
            for ref, desc in refs_vol:
                st.markdown(f"""
                <div style="margin-bottom:0.4rem; padding:0.4rem 0.8rem; background:#fff3cd; border-left:3px solid #f39c12; border-radius:6px;">
                    <span style="font-weight:700; color:#7d6608; font-size:0.82rem;">{ref}</span>
                    <span style="color:#666; font-size:0.82rem;"> — {desc}</span>
                </div>
                """, unsafe_allow_html=True)
            callout("Ces travaux <strong>mesurent la volatilité comme un effet</strong> — sur les prix, sur les déséquilibres réseau. Ils ne proposent pas d'outil pour l'anticiper à court terme.", "warn")

        with col2:
            st.markdown("**Ce que Lindas et al. (2025) confirme — et ce qu'il ne fait pas**")
            st.markdown("""
<div style="padding:0.8rem 1rem; background:#e8f4fd; border-left:4px solid #0f3460; border-radius:8px; margin-bottom:0.8rem;">
<div style="font-weight:700; color:#0f3460; margin-bottom:0.4rem;">Lindas, Goude & Ciais — EDF R&D / CEA, avril 2025</div>
<div style="color:#444; font-size:0.85rem;">
Construit des datasets et benchmarke des modèles ML pour prédire la production solaire et éolienne à l'échelle nationale en France.
Utilise <strong>RTE éCO2mix comme variable cible + données météo spatiales (ERA5)</strong> — exactement notre approche.<br><br>
Constate que les modèles arborescents ont du mal à extrapoler quand la capacité installée augmente —
ce qui justifie notre choix de <strong>normaliser par la capacité (TCH)</strong> plutôt que de travailler en MW absolus.
</div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div style="padding:0.7rem 1rem; background:#fff3cd; border-left:4px solid #f39c12; border-radius:8px; margin-bottom:0.8rem;">
<div style="font-weight:700; color:#7d6608; margin-bottom:0.2rem;">Ce que cet article ne fait pas</div>
<div style="color:#555; font-size:0.85rem;">Il prédit des <strong>niveaux de production</strong> à horizon journalier.
Il ne prédit pas la <strong>variabilité</strong>, ne détecte pas les rampes critiques,
ne propose pas de seuil opérationnel.</div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("**Ce qui reste absent de la littérature**")
            manques = [
                ("Anticipation à 30 minutes", "Aucun outil opérationnel de détection des rampes à horizon intraday sur données ouvertes"),
                ("Seuil de criticité calibré", "Pas de quantification du niveau à partir duquel une variation devient critique pour le réseau"),
                ("Arbitrage recall/précision laissé à l'opérateur", "Les approches existantes optimisent un critère unique — pas de régime ajustable selon le coût opérationnel"),
            ]
            for titre, desc in manques:
                st.markdown(f"""
                <div style="margin-bottom:0.6rem; padding:0.6rem 0.8rem; background:#eafaf1; border-left:3px solid #1abc9c; border-radius:6px;">
                    <div style="font-weight:700; color:#0e6655; font-size:0.85rem;">{titre}</div>
                    <div style="color:#555; font-size:0.82rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='slide-section'><h2>Où se situe ce projet</h2>", unsafe_allow_html=True)
        st.markdown("""
<div style="display:flex; gap:0.8rem; margin:0.5rem 0; flex-wrap:wrap; align-items:stretch;">
    <div style="flex:1; min-width:160px; padding:0.8rem 1rem; background:#fff3cd; border-radius:10px; border-top:3px solid #f39c12; text-align:center;">
        <div style="font-weight:700; color:#f39c12; font-size:0.85rem; margin-bottom:0.4rem;">Littérature académique</div>
        <div style="color:#555; font-size:0.82rem;">Mesure la volatilité <em>ex post</em> comme effet sur les prix et les réseaux</div>
    </div>
    <div style="display:flex; align-items:center; font-size:1.4rem; color:#ccc; padding:0 0.3rem;">→</div>
    <div style="flex:1.3; min-width:200px; padding:0.8rem 1rem; background:#eafaf1; border-radius:10px; border-top:4px solid #1abc9c; text-align:center;">
        <div style="font-weight:800; color:#1abc9c; font-size:0.9rem; margin-bottom:0.4rem;">Ce projet</div>
        <div style="color:#444; font-size:0.82rem;"><strong>Anticipe</strong> la variabilité physique à 30 min<br>Seuil calibré · Données ouvertes · Choix opérateur</div>
    </div>
    <div style="display:flex; align-items:center; font-size:1.4rem; color:#ccc; padding:0 0.3rem;">←</div>
    <div style="flex:1; min-width:160px; padding:0.8rem 1rem; background:#eaf4ff; border-radius:10px; border-top:3px solid #0f3460; text-align:center;">
        <div style="font-weight:700; color:#0f3460; font-size:0.85rem; margin-bottom:0.4rem;">Prévision de production</div>
        <div style="color:#555; font-size:0.82rem;">Prédit les niveaux — domaine mature, bien investi par la recherche et les opérateurs</div>
    </div>
</div>
        """, unsafe_allow_html=True)
        callout("""
Un article de EDF R&D et du CEA publié en avril 2025 valide notre approche RTE + météo spatiale
pour prédire la production solaire en France à l'échelle régionale.
<strong>Leur travail prédit des niveaux de production. Le nôtre prédit la variabilité.</strong>
Ce sont deux problèmes différents — et le nôtre est le moins étudié.
La littérature ne propose pas d'outil pour anticiper les rampes à 30 minutes sur données ouvertes,
avec un seuil calibré et un compromis recall/précision laissé à l'opérateur.
<strong>C'est exactement ce que ce projet construit.</strong>
        """, "info")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 1 : Cadrage méthodologique ───────────────────────────────────────
    with tabs[1]:
        col1, col2 = st.columns([1.1, 1])

        with col1:
            st.markdown("<div class='slide-section'><h2>Pourquoi la région PACA ?</h2>", unsafe_allow_html=True)
            st.markdown("""
La région **Provence-Alpes-Côte d'Azur** réunit trois atouts majeurs pour cette étude :

- **Fort ensoleillement** : parmi les régions françaises les plus irradiées, avec un gradient marqué Nord–Sud
- **Variabilité météorologique significative** : contrastes littoral / vallées / massifs alpins
- **Parc PV développé** : fort taux de pénétration photovoltaïque, données représentatives
            """)
            callout("PACA est la 2e région française pour la capacité PV installée — un terrain d'étude idéal.", "info")
            img_path = Path(__file__).parent / "images" / "Global_Solar_Irradiation_France.jpg"
            if img_path.exists():
                st.image(str(img_path), caption="Irradiance solaire annuelle moyenne en France (source : Commission européenne – PVGIS / JRC)")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Une contrainte qui est devenue une originalité</h2>", unsafe_allow_html=True)
            st.markdown("**Asymétrie fondamentale des données disponibles :**")
            st.markdown("""
<div style="padding:0.7rem 1rem; background:#fff3cd; border-radius:8px; margin-bottom:0.7rem; border-left:3px solid #f39c12;">
<strong>Variable cible (RTE éCO2mix)</strong><br>
<span style="color:#555; font-size:0.9rem;">Production PV agrégée à l'échelle <strong>régionale</strong> — une seule série temporelle pour toute la PACA</span>
</div>
<div style="padding:0.7rem 1rem; background:#d4edda; border-radius:8px; margin-bottom:0.7rem; border-left:3px solid #28a745;">
<strong>Variables explicatives (CAMS, météo)</strong><br>
<span style="color:#555; font-size:0.9rem;">Données disponibles à haute résolution <strong>spatiale</strong> — collectables pour n'importe quel point géographique</span>
</div>
            """, unsafe_allow_html=True)
            st.markdown("""
Cette contrainte a imposé une question centrale : **où collecter les données météo ?**
La réponse — identifier des points géographiques représentatifs pondérés par le parc PV installé — a donné naissance au clustering géographique, l'une des parties les plus originales du projet.
            """)
            callout("Le clustering n'était pas prévu dans le projet initial. C'est la contrainte des données RTE à maille régionale qui l'a rendu nécessaire — et pertinent.", "warn")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='slide-section'><h2>Démarche de clustering</h2>", unsafe_allow_html=True)
        steps = [
            ("1", "Registre PV national (ODRÉ)", "Extraction des installations PACA avec énergie injectée annuelle par commune"),
            ("2", "Nettoyage & agrégation", "Exclusion des entrées sans commune (~0,25% énergie) et des NaN énergie (~1,7% puissance)"),
            ("3", "KMeans sur (lat, lon)", "Clustering géographique pur — K=5 choisi pour équilibrer représentativité et volume de données"),
            ("4", "Centroïdes énergétiques", "Moyenne pondérée des coordonnées par énergie injectée — préserve la hiérarchie physique"),
            ("5", "Commune représentative", "La commune la plus proche du centroïde énergétique dans chaque cluster"),
        ]
        cols = st.columns(5)
        for i, (num, title, desc) in enumerate(steps):
            with cols[i]:
                st.markdown(f"""
                <div style="text-align:center; padding:0.8rem 0.5rem; background:#f8f9fd; border-radius:10px; border-top:3px solid #0f3460; height:160px;">
                    <div style="font-size:1.5rem; font-weight:700; color:#e94560;">{num}</div>
                    <div style="font-weight:700; color:#0f3460; font-size:0.85rem; margin:0.3rem 0;">{title}</div>
                    <div style="color:#666; font-size:0.78rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2 : Clustering géographique PACA ─────────────────────────────────
    with tabs[2]:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='slide-section'><h2>Sources & variables retenues</h2>", unsafe_allow_html=True)
            st.markdown("""
| Source | Variables utilisées | Licence |
|---|---|---|
| Registre ODRÉ | `energieannuelleglissanteinjectee`, `codeinseecommune` | Etalab OL v2 |
| INSEE communes | `code_insee`, `lat`, `lon`, `nom` | ODbL |
            """)
            callout("Choix de l'énergie <strong>injectée</strong> (vs produite) : taux de NaN bien plus faible et mesure directement observable par le gestionnaire de réseau.", "info")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='slide-section'><h2>Gestion des données manquantes</h2>", unsafe_allow_html=True)
            cleaning = [
                ("Communes sans code INSEE", "45 lignes", "Entrées agrégées sans localisation communale — exclusion (0,25% de l'énergie)", "#f39c12"),
                ("Énergie injectée manquante", "149 lignes", "Installations sans historique d'injection — exclusion (1,70% de la puissance)", "#f39c12"),
                ("Énergie injectée négative", "Quelques lignes", "Valeurs physiquement impossibles — erreurs de saisie — exclusion", "#e94560"),
                ("Doublons", "Vérifiés", "drop_duplicates() appliqué", "#1abc9c"),
            ]
            for label, volume, explication, color in cleaning:
                st.markdown(f"""
                <div style="margin-bottom:0.6rem; padding:0.6rem 0.8rem; border-left:3px solid {color}; background:#f8f9fd; border-radius:6px;">
                    <div style="font-weight:700; font-size:0.88rem; color:#1a1a2e;">{label} <span style="color:{color}; font-size:0.82rem;">({volume})</span></div>
                    <div style="color:#555; font-size:0.82rem;">{explication}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Méthode du coude — choix de K</h2>", unsafe_allow_html=True)
            fig_coude = go.Figure()
            fig_coude.add_trace(go.Scatter(
                x=K_VALUES, y=INERTIAS, mode="lines+markers",
                line=dict(color="#0f3460", width=2.5),
                marker=dict(size=8, color="#0f3460"), name="Inertie"
            ))
            fig_coude.add_trace(go.Scatter(
                x=[5], y=[INERTIAS[3]], mode="markers",
                marker=dict(size=14, color="#e94560", symbol="star"),
                name="K = 5 retenu"
            ))
            fig_coude.add_vline(x=5, line_dash="dash", line_color="#e94560", opacity=0.5)
            fig_coude.update_layout(
                title="Méthode du coude — nombre de clusters optimal",
                xaxis_title="Nombre de clusters K",
                yaxis_title="Inertie intra-cluster",
                height=300, margin=dict(l=20, r=20, t=40, b=20),
                legend=dict(orientation="h", y=-0.25),
                plot_bgcolor="white", paper_bgcolor="white",
            )
            fig_coude.update_xaxes(gridcolor="#f0f0f0", dtick=1)
            fig_coude.update_yaxes(gridcolor="#f0f0f0")
            st.plotly_chart(fig_coude, use_container_width=True)
            callout("""
<strong>K = 5 : un choix pragmatique, pas purement algorithmique.</strong><br>
La courbe du coude ne pointe pas formellement vers K = 5, mais ce choix garantit
une couverture territoriale pertinente (5 zones distinctes en PACA) tout en limitant
le volume de données météo à collecter.
            """, "warn")
            st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns([1.5, 1])

        with col1:
            st.markdown("<div class='slide-section'><h2>Carte PACA — communes représentatives</h2>", unsafe_allow_html=True)
            fig_map = go.Figure()
            for i, row in COMMUNES.iterrows():
                fig_map.add_trace(go.Scattergeo(
                    lat=[row["lat"]], lon=[row["lon"]],
                    mode="markers+text",
                    marker=dict(size=18, color=COLORS[i], symbol="star", line=dict(width=2, color="white")),
                    text=[row["commune"]], textposition="top center",
                    textfont=dict(size=11, color="#1a1a2e"),
                    name=f"Cluster {i} — {row['commune']}", showlegend=True,
                ))
            fig_map.update_layout(
                geo=dict(
                    scope="europe", projection_type="mercator",
                    center=dict(lat=43.8, lon=6.0),
                    lataxis_range=[43.0, 45.0], lonaxis_range=[4.2, 7.8],
                    showland=True, landcolor="#f5f5f0",
                    showcoastlines=True, coastlinecolor="#aaa",
                    showrivers=True, rivercolor="#cce5ff",
                    showframe=False, bgcolor="white",
                ),
                height=380, margin=dict(l=0, r=0, t=10, b=0),
                legend=dict(orientation="v", x=1.0, y=0.5, font=dict(size=10), bgcolor="rgba(255,255,255,0.85)"),
                paper_bgcolor="white",
            )
            st.plotly_chart(fig_map, use_container_width=True)
            img_carte = Path(__file__).parent / "images" / "carte_paca_communes.png"
            if img_carte.exists():
                st.image(str(img_carte), caption="Clustering géographique — communes et distribution du parc PV PACA")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='slide-section'><h2>Les 5 communes représentatives</h2>", unsafe_allow_html=True)
            for i, row in COMMUNES.iterrows():
                st.markdown(f"""
                <div style="margin-bottom:0.7rem; padding:0.8rem 1rem; border-radius:10px; border-left:4px solid {COLORS[i]}; background:#f8f9fd;">
                    <div style="font-weight:700; color:{COLORS[i]}; font-size:0.95rem;">Cluster {i} — {row['commune']}</div>
                    <div style="color:#555; font-size:0.82rem; margin-top:0.2rem;">
                        {row['zone']}<br>
                        Contribution régionale : <strong>{row['contrib_pct']}%</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='slide-section'><h2>Conclusion méthodologique</h2>", unsafe_allow_html=True)
        st.markdown("""
Ces **5 communes** deviennent les **points d'ancrage géographiques** pour toute la suite du pipeline :
chaque variable météorologique, atmosphérique et astronomique sera collectée à ces 5 localisations,
puis agrégée au niveau régional pour être mise en regard de la production RTE.
        """)
        callout("Cruis · Saint-Étienne-le-Laus · Saint-Vallier-de-Thiey · Bras · Eygalières — 5 points pour couvrir la PACA.", "success")
        st.markdown("</div>", unsafe_allow_html=True)
