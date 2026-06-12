import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import plotly.graph_objects as go
from utils import load_dataset, load_model, get_xy

from utils import slide_header, section, kpi, formula, callout
from utils import load_dataset, load_model, check_data_available, check_model_available, get_xy


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ANALYSE EXPLORATOIRE
# ─────────────────────────────────────────────────────────────────────────────
def page_exploration():
    slide_header(
        "Analyse exploratoire",
        "Exploration des variables disponibles · Relation entre variables cible et explicatives"
    )

    tabs = st.tabs([
        "Bilan général",
        "Variables communales",
        "Variables explicatives",
        "Variable cible",
    ])

    # ── Tab 0 : Bilan général ───────────────────────────────────────────
    with tabs[0]:
        callout("""<h3>Bilan général de la collecte</h3>

- Pas de créneau manquant : on a une observation toutes les 30 minutes.
- Pas de doublon.
- Pas de valeur manquante.
""")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 6 variables régionales")
            st.markdown("""

- **`cible`** : variabilité absolue du taux de charge de la production solaire à t + 30 minutes.
- **`variabilité`** : cible signée (pour tests).
- **`consommation`** : consommation électrique totale du périmètre considéré sur l'intervalle de temps donné.
- **`production brute`** : production électrique issue des installations photovoltaïques sur le périmètre considéré.
- **`couverture`** : taux de couverture de la production solaire.
- **`production normalisée`** : taux de charge de la production solaire.
""")

            st.markdown("### 5 x 2 variables communales de positionnement solaire")
            st.markdown("""

- **`altitude`** : altitude solaire (en degrés), représentant l'élévation du soleil au-dessus de l'horizon (valeurs négatives durant la nuit).
- **`azimuth`** : azimut solaire (en degrés), indiquant la direction du soleil par rapport au nord (0–360° selon la convention).
""")

            st.markdown("### 5 x 4 variables communales météorologiques")
            st.markdown("""

- **`nébulosité`** : nébulosité ou fraction de couverture nuageuse (exprimée selon les produits en fraction, pourcentage ou indice adimensionnel).
- **`température`** : température de l'air à 2 mètres du sol (en °C ou en K selon la source ; une vérification des unités est nécessaire).
- **`humidité`** : humidité de l'air (généralement humidité relative en %, ou humidité spécifique selon la source).
- **`vitesse du vent`** : vitesse du vent mesurée à 2 mètres du sol (m/s).
""")

        with col2:
            st.markdown("### 5 x 10 variables communales atmosphériques")
            st.markdown("""
- **`irradiance au sommet de l'atmosphère`** *(Top Of Atmosphere)* : rayonnement solaire incident au sommet de l'atmosphère (Wh/m²), utilisé pour le contrôle de cohérence et la normalisation des séries.
- **`composante directe horizontale`** *(BHI pour Beam Horizontal Irradiance)* : composante directe du rayonnement solaire projetée sur le plan horizontal (Wh/m²).
- **`composante directe normale`** *(BNI pour Beam Normal Irradiance)* : irradiance directe normale, reçue sur un plan perpendiculaire aux rayons solaires (Wh/m²).
- **`composante diffuse horizontale`** *(DHI pour Diffuse Horizontal Irradiance)* : composante diffuse du rayonnement solaire reçue sur un plan horizontal (Wh/m²).
- **`irradiance globale horizontale`** *(GHI pour Global Horizontal Irradiance)* : irradiance globale reçue sur un plan horizontal (composantes directe et diffuse) exprimée en Wh/m².
- **`BHI par temps clair`** : composante directe horizontale en conditions de ciel clair (Wh/m²).
- **`BNI par temps clair`** : irradiance directe normale en conditions de ciel clair (Wh/m²).
- **`DHI par temps clair`** : composante diffuse horizontale en conditions de ciel clair (Wh/m²).
- **`GHI par temps clair`** : irradiance globale horizontale en conditions de ciel clair, utilisée comme référence théorique sans nuages (Wh/m²).
- **`fiabilité`** : fiabilité des données atmosphériques.
""")

    # ── Tab 1 : Variables communales ──────────────────────────────────────────────
    with tabs[1]:
        col1, col2 = st.columns(2)

        with col1:
            callout("""<h3>Ressemblances</h3>

- Les variables des différentes communes semblent avoir une distribution similaire.
- On analyse leur colinéarité par le critère du **VIF** (*Variance Inflation Factor*).
""", "warn")
            img_path = Path(__file__).parent / "images" / "var_communes.png"
            if img_path.exists():
                st.image(str(img_path), caption="Comparaisons de variables prises aux cinq communes", width=1000)



        with col2:
            st.markdown("### VIF")
            st.markdown("""Le VIF mesure à quel point la variance d'un coefficient de régression est amplifiée en raison de la multicolinéarité entre les variables explicatives d'un modèle.

Si les variables sont colinéaires, le VIF est supérieur à 5:

- 10 <= VIF : multicolinéarité significative
- 5 <= VIF < 10 : colinéarité importante (à investiguer)
- 1 <= VIF < 5 : pas de colinéarité

### Méthode

Pour chaque type de variable collectée au niveau communal (azimuth, nébolosité, ...) :
- On regroupe les cinq variables (une par commune)
- On calcule le VIF sur ces cinq variables
""")

            st.markdown("### Résultats")
            st.markdown("""

- 81\% de nos variables communales semblent colinéaires (13 sur les 16)
- Les variables qui ne semblent pas colinéaires entre elles sont liées à la météo :
    - la nébulosité,
    - la vitesse du vent, et
    - la composante diffuse horizontale de l'irradiance (sans doute lié à la nébulosité)

### Solution

Par soucis de simplification on agrège les données communales, au moyen d'une **somme pondérée**, où les poids sont définis à partir de la contribution énergétique de chaque commune, afin d'obtenir des indicateurs météorologiques régionaux cohérents avec la répartition spatiale de la production solaire.
""")


    # ── Tab 2 : Variables explicatives ───────────────────────────────────────────────────
    with tabs[2]:
        callout("""<h3>Distribution des variables</h3>

- Les **ordres de grandeurs** sont **différents** d'une variable à une autre : certaines méthodes de modélisation nécessiteront une normalisation.
- Présence de **valeurs extrêmes** pour certaines variables.
- Mais ces valeurs extrêmes restent dans des plages de valeurs normales et ne paraissent **pas aberrantes**.
""")
        img_path = Path(__file__).parent / "images" / "distrib.png"
        if img_path.exists():
            st.image(str(img_path), caption="Exemple de distributions de variables du jeu de données", width=1000)


    # ── Tab 3 : Variable cible ───────────────────────────────────────────────────
    with tabs[3]:
        callout("<h3>Aperçu sur une journée</h3>")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
La variabilité est :

- **forte** lors du lever et du coucher du soleil, avec une forte dispersion
- **faible** en milieu de journée, avec une dispersion plus faible, lorsque la production est forte.

La production est comme on s'y attend plus forte au midi solaire qu'en début et en fin de journée.
""")
        with col2:
            img_path = Path(__file__).parent / "images" / "cible_tch_jour.png"
            if img_path.exists():
                st.image(str(img_path), caption="Cible et Production moyennes sur une journée", width=800)


        callout("<h3>Aperçu sur une année</h3>")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
La variabilité est :

- *légèrement* plus **forte** au début du printemps et à la fin de l'été jusqu'en automne, avec une forte dispersion
- *légèrement* plus **faible** en hiver et en fin de printemps début de l'été, avec une dispersion plus faible.

La production est comme on s'y attend plus forte en été qu'en hiver.
""")
        with col2:
            img_path = Path(__file__).parent / "images" / "cible_tch_mois.png"
            if img_path.exists():
                st.image(str(img_path), caption="Cible et Production moyennes sur une année", width=800)

        callout("<h3>Cible en fonction de l'irradiance globale</h3>")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
La variabilité :

- **augmente** tant que l'irradiance ne dépasse pas un certain seuil (lever et coucher du soleil, intempéries).


- **décroit** après que l'irradiance ait dépassé le seuil (milieu de journée, par temps clair).

Comme on peut s'y atendre, la production de manière régulière avec l'irradiance.
""")
        with col2:
            img_path = Path(__file__).parent / "images" / "cible_tch_ghi.png"
            if img_path.exists():
                st.image(str(img_path), caption="Cible et Production en fonction de l'irradiance globale", width=800)

