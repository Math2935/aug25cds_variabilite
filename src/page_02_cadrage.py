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
# PAGE CADRAGE GEOGRAPHIQUE
# ─────────────────────────────────────────────────────────────────────────────
def page_cadrage():
    slide_header(
        "Cadrage Géographique",
        "PACA : un contexte géographique diversifié · Littoral · Montagnes"
    )

    tabs = st.tabs([
        "Méthodologie",
        "Traitement des données",
        "Résultats du clustering",
    ])

    # ── Tab 0 : Méthodologie ───────────────────────────────────────────
    with tabs[0]:
        st.markdown("#### Une région pour plusieurs contextes géographiques")


    # ── Tab 1 : Traitement des données ──────────────────────────────────────────────
    with tabs[1]:
        pass


    # ── Tab 2 : Résultats du clustering ──────────────────────────────────────────────
    with tabs[2]:
        pass
