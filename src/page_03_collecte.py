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
# PAGE COLLECTE DE DONNEES
# ─────────────────────────────────────────────────────────────────────────────
def page_collecte():
    slide_header(
        "Collecte de données",
        "Construction du jeux de données · Sources multiples"
    )

    tabs = st.tabs([
        "Objectifs",
        "Production énergétique",
        "Position du soleil",
        "Atmosphère",
        "Météo",
        "Aggrégation"
    ])


    # ── Tab 0 : Objectifs ──────────────────────────────────────────────
    with tabs[0]:
        callout("""<h3>Besoins</h3>

- Nous avons besoin de prédire l'arrivée de **rampes critiques** sur le réseau.
- Ces rampes critiques surviennent lorsque la **production** d'énergie des panneaux solaires **augmente ou chute brutalement**.
- Une manière de caractériser ce changement de production est de calculer la **variabilité** de cette dernière.""")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Variable cible")
            st.markdown("- Il **n'existe pas** de jeux de données la fournissant directement la `variabilité de la production solaire` : il faut la **calculer** !")
            st.markdown("- Parmi les **nombreuses** méthodes de calcul de la **variabilité**, nous faisons le choix d'utiliser la suivante :")
            st.markdown(r"""
$$
| \Delta Production (t+1) | = | Production (t+1) - Production (t) |
$$
""")
            st.markdown("""- Pourquoi prendre la valeur absolue ?
    - Seule l'**intensité** de la variation intéresse le gestionnaire de réseau : le **sens** de la variation n'a pas besoin d'être prédit (allège le problème).
    - La distribution de la variabilité signée est **centrée autour de 0** et plutôt **symétrique** : un modèle risquerait de **converger vers 0** et de **manquer des rampes**.""")
            st.markdown("- La production d'énergie peut être **brute** ou **normalisée** par rapport à la **capacité de production**.")
            callout("""Comme le parc de production d'énergie solaire évolue actuellement fortement et par à coup, nous faisons le choix d'utiliser la <strong>production normalisée</strong> pour limiter l'impact de l'évolution du parc sur notre futur modèle.""", "success")



        with col2:
            img_path = Path(__file__).parent / "images" / "evol_solar.png"
            if img_path.exists():
                st.image(str(img_path), caption="Évolution de la production solaire photovoltaïque en France (source : RTE)")

        st.markdown("### Variables explicatives")
        st.markdown("Les données de production à elles seules ne suffisent pas à expliquer leurs variations. Nos recherches dans la littérature scientifique nous a donné d'autres pistes de variables complémentaires :")
        st.markdown("    - la **position du soleil** dans le ciel ;")
        st.markdown("    - la composition de l'**atmosphère** ; et bien sûr")
        st.markdown("    - la **météo**.")


    # ── Tab 1 : Production énergétique ───────────────────────────────────────────
    with tabs[1]:
        callout("""<h3>Source</h3>

- Provenance <b>RTE</b> : jeux de données <b>éCO2Mix</b>, distribué par <i>Ordré</i> Opendata Réseaux-Energies sous licence Ouverte 2.0 (Etalab)

- Forme : **une archive zip par année**, contenant un jeu de données en CSV.
""")

        callout("""<h3>Nettoyage</h3>

- Sélection des <b>années contenant les données</b> de production normalisées.
- <b>Elimination</b> des observations <i>ne contenant pas la production normalisée</i>.
- Rétention des <b>variables communes</b> à toutes les années retenues (les variables disponibles varient d'une année à une autre) pour <b>concaténer</b> les années entre elles.
- <b>Abandon</b> des <i>variables</i> <b>ne concernant pas</b> l'<i>énergie solaire</i> (éCO2Mix contient toutes les sources d'énergies ainsi que les échanges entre réseaux).
- Détermination du <b>fuseau horaire</b> et <b>conversion au fuseau UTC</b>, avec gestion des observations manquantes créées à cette occasion.
- <b>Calcul de la variable cible</b> à t + 30 minutes.
""", "warn")

        callout(f"""<h3>Bilan</h3>

<div class='kpi-row'>
                {kpi("2013–2025", "Années disponibles")}
                {kpi("2020–2025", "Années retenues", "orange")}
                {kpi("30 min", "Résolution temporelle", "green")}
                {kpi("7", "Colonnes finales", "accent")}
                </div>
""", "success")



    # ── Tab 2 : Position du solei ──────────────────────────────────────────────
    with tabs[2]:
        callout("""<h3>Source</h3>

- Provenance : <b>PySolar</b>, librairie Python sous licence GPL v3.

- Forme : calcul de nouvelles variables à l'aide de la librairie PySolar et des coordonnées géographique.
""")

        callout("""<h3>Collecte</h3>


""", "warn")

        callout(f"""<h3>Bilan</h3>

<div class='kpi-row'>
                {kpi("2013–2025", "Années disponibles")}
                {kpi("2020–2025", "Années retenues", "orange")}
                {kpi("30 min", "Résolution temporelle", "green")}
                {kpi("7", "Colonnes finales", "accent")}
                </div>
""", "success")


    # ── Tab 3 : Atmosphère ───────────────────────────────────────────────────
    with tabs[3]:
        pass


    # ── Tab 4 : Météo ───────────────────────────────────────────────────
    with tabs[4]:
        pass


    # ── Tab 5 : Aggrégation ───────────────────────────────────────────────────
    with tabs[5]:
        pass

