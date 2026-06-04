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
        "Production énergétique",
        "Position du soleil",
        "Atmosphère",
        "Météo",
        "Aggrégation"
    ])

    # ── Tab 0 : Production énergétique ───────────────────────────────────────────
    with tabs[0]:
        st.markdown("#### Résumé chiffré :")

        st.markdown(f"""<div class='kpi-row'>
                {kpi("2013–2025", "Années disponibles")}
                {kpi("2020–2025", "Années retenues", "orange")}
                {kpi("30 min", "Résolution temporelle", "green")}
                {kpi("7", "Colonnes finales", "accent")}
                </div>""", unsafe_allow_html=True)






    # ── Tab 1 : Position du solei ──────────────────────────────────────────────
    with tabs[1]:
        pass


    # ── Tab 2 : Atmosphère ───────────────────────────────────────────────────
    with tabs[2]:
        pass


    # ── Tab 3 : Météo ───────────────────────────────────────────────────
    with tabs[3]:
        pass


    # ── Tab 4 : Aggrégation ───────────────────────────────────────────────────
    with tabs[4]:
        pass

