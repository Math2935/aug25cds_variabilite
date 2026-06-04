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
# PAGE FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────────────────────
def page_feature_engineering():
    slide_header(
        "Feature Engineering",
        "Construction des variables explicatives · Sans fuite temporelle"
    )

    tabs = st.tabs([
        "Encodage temporel",
        "Azimut solaire",
        "Découpage train/valid/test",
        "Lags & Variations",
        "CSI & Ratio TCH/GHI",
        "Agrégation régionale"
    ])

# ── Tab 0 : Encodage temporel ───────────────────────────────────────────
    with tabs[0]:
        st.markdown("### Pourquoi encoder cycliquement ?")
        st.markdown("""
Un encodage numérique classique introduit des **discontinuités artificielles** :
- 23h et 0h sont très proches dans le temps, mais numériquement distants.
- Le 31 décembre et le 1er janvier sont des dates voisines dans le cycle annuel.

L'encodage sinusoïdal **préserve la continuité** de ces cycles.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Heure de la journée**")
            formula("sin_hour(t) = sin(2π·heure(t)/24)<br>cos_hour(t) = cos(2π·heure(t)/24)")
        with col2:
            st.markdown("**Jour de l'année**")
            formula("sin_doy(t) = sin(2π·jour(t)/N_jours)<br>cos_doy(t) = cos(2π·jour(t)/N_jours)")

        st.markdown("---")
        st.markdown("### Visualisation de l'encodage cyclique")

        # Generate synthetic illustration
        theta = np.linspace(0, 2*np.pi, 360)
        t = np.linspace(0, 24, 48)
        sin_h = np.sin(2*np.pi*t/24)
        cos_h = np.cos(2*np.pi*t/24)

        fig, axes = plt.subplots(1, 2, figsize=(14, 4))
        fig.patch.set_facecolor('white')

        # Circle
        # ax = axes[0]
        # scatter_h = np.linspace(0, 24, 48)
        # ax.scatter(np.cos(2*np.pi*scatter_h/24), np.sin(2*np.pi*scatter_h/24),
        #            c=scatter_h, cmap='plasma', s=40, zorder=3, alpha=0.8)
        # ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3)
        # ax.set_aspect('equal')
        # ax.set_title("Cercle unité — heure", fontsize=11, fontweight='bold')
        # ax.set_xlabel(r"$\cos$"); ax.set_ylabel(r"$\sin$")
        # ax.grid(True, alpha=0.3)

        # Continuity
        ax = axes[0]
        ax.plot(t, sin_h, color='#0f3460', label='sin_hour', linewidth=2)
        ax.plot(t, cos_h, color='#e94560', label='cos_hour', linewidth=2)
        ax.set_xlabel("Heure continue"); ax.set_ylabel("Valeur encodée")
        ax.set_title("Continuité horaire", fontsize=11, fontweight='bold')
        ax.legend(); ax.grid(True, alpha=0.3)

        # Midnight continuity
        ax = axes[1]
        t_night = np.linspace(0, 24, 48)
        ax.scatter(np.cos(2*np.pi*t_night/24), np.sin(2*np.pi*t_night/24),
                   color='#e94560', s=40, zorder=3)
        ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3)
        ax.set_aspect('equal')
        ax.set_title("Continuité autour de minuit", fontsize=11, fontweight='bold')
        ax.legend(); ax.grid(True, alpha=0.3)
        ax.text(1.05, -0.01, f"(00h00)", fontsize=8, color='blue')
        ax.text(1.03, 0.13, f"(00h30)", fontsize=8, color='blue')
        ax.text(1.03, -0.16, f"(23h30)", fontsize=8, color='blue')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        callout("✅ Les points autour de minuit (23h30 et 00h00) sont <strong>voisins</strong> sur le cercle — discontinuité éliminée.", "success")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 1 : Azimut solaire ──────────────────────────────────────────────
    with tabs[1]:
        st.markdown("### Encodage cyclique de l'azimut solaire")
        st.markdown("""
L'**azimut solaire** représente la direction horizontale du soleil (0° à 360°).
C'est une variable **circulaire** : 359° est très proche de 1°.

Un encodage numérique brut introduirait une rupture artificielle en fin de journée.
        """)

        formula("azimuth_sin = sin(azimuth_rad)<br>azimuth_cos = cos(azimuth_rad)")

        st.markdown("---")
        # Visual
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        fig.patch.set_facecolor('white')

        az = np.linspace(0, 360, 360)
        az_rad = np.radians(az)

        ax = axes[0]
        ax.plot(az, np.sin(az_rad), color='#0f3460', linewidth=2, label='sin(azimuth)')
        ax.plot(az, np.cos(az_rad), color='#e94560', linewidth=2, label='cos(azimuth)')
        ax.set_xlabel("Azimut (degrés)"); ax.set_ylabel("Valeur encodée")
        ax.set_title("Encodage sin/cos de l'azimut", fontsize=11, fontweight='bold')
        ax.legend(); ax.grid(True, alpha=0.3)

        ax = axes[1]
        theta = np.linspace(0, 2*np.pi, 360)
        ax.scatter(np.cos(az_rad), np.sin(az_rad), c=az, cmap='twilight', s=10, alpha=0.7)
        ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3)
        ax.set_aspect('equal')
        ax.set_title("Projection sur le cercle unité", fontsize=11, fontweight='bold')
        ax.set_xlabel("cos"); ax.set_ylabel("sin"); ax.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        callout("La colonne <code>azimuth</code> brute est <strong>supprimée</strong> et remplacée par <code>azimuth_sin</code> et <code>azimuth_cos</code> pour chaque point.", "info")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2 : Découpage ───────────────────────────────────────────────────
    with tabs[2]:
        st.markdown("### Découpage temporel strict — anti-fuite")
        st.markdown("""
Le découpage est figé **avant** toute construction de variable dérivée.
Les modèles de séries temporelles doivent être évalués sur des **périodes futures**.
        """)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
<div style='background:linear-gradient(135deg,#0f3460,#1a5276);color:white;border-radius:12px;padding:1.5rem;text-align:center'>
<div style='font-size:1.8rem;font-weight:700'>Train</div>
<div style='font-size:1.2rem;margin:.4rem 0'>2020 → 2023</div>
<div style='opacity:.8;font-size:.85rem'>~70 000 obs<br>Entraînement des modèles</div>
</div>
""", unsafe_allow_html=True)
        with col2:
            st.markdown("""
<div style='background:linear-gradient(135deg,#e94560,#c0392b);color:white;border-radius:12px;padding:1.5rem;text-align:center'>
<div style='font-size:1.8rem;font-weight:700'>Validation</div>
<div style='font-size:1.2rem;margin:.4rem 0'>2024</div>
<div style='opacity:.8;font-size:.85rem'>~17 000 obs<br>Sélection des hyperparamètres</div>
</div>
""", unsafe_allow_html=True)
        with col3:
            st.markdown("""
<div style='background:linear-gradient(135deg,#1abc9c,#16a085);color:white;border-radius:12px;padding:1.5rem;text-align:center'>
<div style='font-size:1.8rem;font-weight:700'>Test</div>
<div style='font-size:1.2rem;margin:.4rem 0'>2025</div>
<div style='opacity:.8;font-size:.85rem'>Données jamais vues<br>Évaluation finale uniquement</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")
        # Timeline visualization
        fig, ax = plt.subplots(figsize=(12, 2.5))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        bars = [
            (2020, 4, '#0f3460', 'TRAIN (2020–2023)'),
            (2024, 1, '#e94560', 'VALID (2024)'),
            (2025, 1, '#1abc9c', 'TEST (2025)'),
        ]
        for start, width, color, label in bars:
            ax.barh(0, width, left=start, height=0.5, color=color, label=label, alpha=0.9)
            ax.text(start + width/2, 0, label, ha='center', va='center',
                    color='white', fontweight='bold', fontsize=9)
        ax.set_xlim(2019.5, 2026.5)
        ax.set_ylim(-0.5, 0.5)
        ax.set_xlabel("Année")
        ax.set_yticks([])
        ax.set_title("Découpage chronologique des données", fontweight='bold', fontsize=11)
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        callout("📌 <strong>Folds de validation croisée temporelle</strong> : 4 folds manuels couvrant 2021→2024 — l'ordre chronologique est toujours respecté.", "info")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 3 : Lags & Variations ───────────────────────────────────────────
    with tabs[3]:
        callout("⚠️ <strong>Règle anti-fuite</strong> : toutes les variables explicatives utilisent uniquement l'information disponible à l'instant <em>t</em> ou avant.", "warn")
        st.markdown("### Mémoire du système : lags, variations, statistiques glissantes")
        st.markdown("""
Pour prédire une variation à court terme, il ne suffit pas de connaître l'état instantané.
Il faut décrire la **dynamique récente** du système.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Variables de retard (lags)")
            formula("var_lag_1 = var(t-1)  ← 30 min avant<br>var_lag_2 = var(t-2)  ← 1h avant<br>var_lag_3 = var(t-3)  ← 1h30 avant")

        with col2:
            st.markdown("#### Variables de variation")
            formula("dvar_dt      = var(t) - var(t-1)  [signée]<br>dvar_abs_dt  = |dvar_dt|          [absolue]<br>dvar_dt_lag_1/2/3               [retardées]")

        st.markdown("---")
        st.markdown("#### Statistiques glissantes sur une fenêtre de 2h (4 pas)")

        col1, col2 = st.columns(2)
        with col1:
            formula("var_roll_mean_4    = moyenne glissante<br>var_roll_std_4     = écart-type glissant")
        with col2:
            formula("dvar_roll_mean_4   = moyenne des variations<br>dvar_roll_std_4    = volatilité récente<br>dvar_abs_roll_mean = intensité moyenne")

        st.markdown("---")
        st.markdown("#### Variables ciblées par ces dérivées")

        vars_list = [
            ("GHI", "Irradiance globale horizontale — variable d'irradiance principale"),
            ("CSI", "Clear Sky Index — état atmosphérique normalisé"),
            ("TCH solaire", "Taux de charge solaire — production normalisée"),
            ("Ratio TCH/GHI", "Cohérence production/irradiance — indicateur opérationnel"),
        ]
        for var, desc in vars_list:
            st.markdown(f"- **`{var}`** — {desc}")

        callout("✅ Toutes ces variables respectent la règle anti-fuite : elles utilisent uniquement des informations disponibles à <em>t</em> ou avant.", "success")
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Tab 4 : CSI & Ratio ─────────────────────────────────────────────────
        with tabs[4]:
            st.markdown("### Indicateurs atmosphériques complémentaires")

            tab_a, tab_b = st.tabs(["☁️ Clear Sky Index (CSI)", "📉 Ratio TCH / GHI"])

            with tab_a:
                st.markdown("#### Clear Sky Index — Mesure de l'atténuation atmosphérique")
                st.markdown("""
    Le **CSI** compare l'irradiance réellement observée à l'irradiance théorique sous ciel clair.
                """)
                formula("CSI(t) = GHI(t) / GHI_clear_sky(t)")

                col1, col2, col3 = st.columns(3)
                col1.markdown("""
    <div style='background:#eaf4ff;border-radius:10px;padding:1rem;text-align:center;border:1px solid #bee3f8'>
    <b>CSI ≈ 1</b><br><small>Ciel clair<br>Conditions idéales</small>
    </div>""", unsafe_allow_html=True)
                col2.markdown("""
    <div style='background:#fff9e6;border-radius:10px;padding:1rem;text-align:center;border:1px solid #fbd38d'>
    <b>CSI 0.5–0.8</b><br><small>Partiellement nuageux<br>Atténuation modérée</small>
    </div>""", unsafe_allow_html=True)
                col3.markdown("""
    <div style='background:#fff5f5;border-radius:10px;padding:1rem;text-align:center;border:1px solid #fed7d7'>
    <b>CSI ≈ 0</b><br><small>Très nuageux ou nuit<br>Faible production</small>
    </div>""", unsafe_allow_html=True)

                callout(
                    "⚠️ Quand GHI_clear_sky < 10 W/m², le CSI est fixé à 0 pour éviter les divisions instables (lever/coucher du soleil, nuit).",
                    "warn")

            with tab_b:
                st.markdown("#### Ratio TCH/GHI — Cohérence production/irradiance")
                st.markdown("""
    Ce ratio mesure si la production photovoltaïque observée est cohérente avec l'irradiance disponible.
                """)
                formula("Ratio(t) = TCH_solaire(t) / GHI(t)")

                st.markdown("""
    **Interprétation :**
    - Ratio **normal** → production cohérente avec l'irradiance
    - Ratio **anormalement faible** (GHI fort, TCH faible) → possible curtailment, panne partielle ou limitation réseau
    - Ce ratio est un **indicateur candidate** — sa pertinence est validée en modélisation

    *Quand GHI < 10 W/m², le ratio est fixé à 0 pour éviter les instabilités numériques.*
                """)

            st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 5 : Agrégation régionale ────────────────────────────────────────
    with tabs[5]:
        st.markdown("### Agrégation régionale — 5 points représentatifs PACA")
        st.markdown("""
Les données proviennent de **5 points géographiques représentatifs** de la région PACA,
pondérés par leur puissance photovoltaïque installée.
        """)
        st.latex(r"\text{var\_region}(t) = \sum_i \text{poids\_i} \times \text{var\_commune\_i(t)}")

        st.markdown("---")
        st.markdown("**Pourquoi agréger ?**")
        st.markdown("""
- Réduire la dimensionnalité (5 × N colonnes → N colonnes)
- Obtenir une vision régionale cohérente de la production PV
- Les pondérations reflètent la capacité installée réelle
- Plus robuste aux effets locaux (orages, masques…)
            """)

