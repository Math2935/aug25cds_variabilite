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
# PAGE ANALYSE EXPLORATOIRE
# ─────────────────────────────────────────────────────────────────────────────
def page_exploration():
    slide_header(
        "Analyse exploratoire",
        "Exploration des variables disponibles · Relation entre variables cible et explicatives"
    )

    tabs = st.tabs([
        "Variables disponibles",
        "Données communales",
        "Données régionales",
        "Variable cible",
    ])

    # ── Tab 0 : Variables disponibles ───────────────────────────────────────────
    with tabs[0]:
        pass


    # ── Tab 1 : Données communales ──────────────────────────────────────────────
    with tabs[1]:
        pass


    # ── Tab 2 : Données régionales ───────────────────────────────────────────────────
    with tabs[2]:
        pass


    # ── Tab 3 : Variable cible ───────────────────────────────────────────────────
    with tabs[3]:
        pass


