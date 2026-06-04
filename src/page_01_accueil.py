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
# PAGE ACCUEIL
# ─────────────────────────────────────────────────────────────────────────────
def page_accueil():
    slide_header(
        "Analyse et Prédiction de la Variabilité Solaire",
        "Région PACA · Données ouvertes · Pas de temps 30 minutes · 2020–2025"
    )

    # KPIs
    st.markdown("""<div class='kpi-row'>""" +
        kpi("5 ans", "Période d'analyse", "") +
        kpi("30 min", "Résolution temporelle", "accent") +
        kpi("~87 K", "Observations (train)", "green") +
        kpi("5 pts", "Points géographiques", "orange") +
    """</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h2 style='color:#0f3460;border-bottom:2px solid #e94560;padding-bottom:.4rem'>Objectif</h2>", unsafe_allow_html=True)
        st.markdown("""
Prédire **l'amplitude de la variation future** de la production photovoltaïque normalisée :

$$y_t = |\\text{tch}_{t+1} - \\text{tch}_t|$$

> Chaque pas de temps représente **30 minutes** — on prédit donc la variabilité dans les 30 prochaines minutes.
        """)
        callout("⚡ Enjeu opérationnel : anticiper les rampes critiques pour la gestion du réseau PACA.", "warn")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<h2 style='color:#0f3460;border-bottom:2px solid #e94560;padding-bottom:.4rem'>Démarche</h2>", unsafe_allow_html=True)
        steps = [
            ("Collecte data", "CAMS, RTE"),
            ("Analyse exploratoire", "Variable cible, graphs..."),
            ("Feature Engineering", "Encodages cycliques, lags, stats glissantes, CSI"),
            ("Modélisation", "Baseline naïve à battre, modèles linéaires, LazyPredict, arbres & boosting"),
            ("Modèle final", "Résultats · Interprétabilité · classification des rampes critiques"),
        ]
        for title, desc in steps:
            st.markdown(f"**{title}** — <small style='color:#666'>{desc}</small>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
