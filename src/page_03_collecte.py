import streamlit as st
import pandas as pd
import numpy as np
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
        st.markdown("### Variable cible")
        st.markdown("- Il **n'existe pas** de jeux de données la fournissant directement la `variabilité de la production solaire` :arrow_right: Il faut la **calculer** !")
        st.markdown("- Parmi les **nombreuses** méthodes de calcul de la **variabilité**, nous faisons le choix d'utiliser la suivante :")
        st.markdown(r"""
$$
| \Delta Production (t+1) | = | Production (t+1) - Production (t) |
$$
""")
        st.markdown("- La production d'énergie peut être **brute** ou **normalisée** par rapport à la **capacité de production**.")
        callout("""Comme le parc de production d'énergie solaire évolue actuellement fortement et par à coup, nous faisons le choix d'utiliser la <strong>production normalisée</strong> pour limiter l'impact de l'évolution du parc sur notre futur modèle.""")


        st.markdown("### Variables explicatives")
        st.markdown("Les données de production à elles seules ne suffisent pas à expliquer leurs variations. Nos recherches dans la littérature scientifique nous a donné d'autres pistes de variables complémentaires :")
        st.markdown("    - la **position du soleil** dans le ciel ;")
        st.markdown("    - la composition de l'**atmosphère** ; et bien sûr")
        st.markdown("    - la **météo**.")


    # ── Tab 1 : Production énergétique ───────────────────────────────────────────
    with tabs[1]:


        st.markdown("### Résumé chiffré")

        st.markdown(f"""<div class='kpi-row'>
                {kpi("2013–2025", "Années disponibles")}
                {kpi("2020–2025", "Années retenues", "orange")}
                {kpi("30 min", "Résolution temporelle", "green")}
                {kpi("7", "Colonnes finales", "accent")}
                </div>""", unsafe_allow_html=True)






    # ── Tab 2 : Position du solei ──────────────────────────────────────────────
    with tabs[2]:
        pass


    # ── Tab 3 : Atmosphère ───────────────────────────────────────────────────
    with tabs[3]:
        pass


    # ── Tab 4 : Météo ───────────────────────────────────────────────────
    with tabs[4]:
        pass


    # ── Tab 5 : Aggrégation ───────────────────────────────────────────────────
    with tabs[5]:
        pass

