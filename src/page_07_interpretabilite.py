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
# PAGE INTERPRÉTABILITÉ
# ─────────────────────────────────────────────────────────────────────────────
def page_interpretabilite():
    slide_header(
        "Interprétabilité du Modèle avec SHAP",
        "ExtraTreesRegressor · SHAP"
    )

    tabs = st.tabs([
        "SHAP Values",
        "Synthèse physique"
    ])

    # Helper to load model & test data
    model = load_model("final_model_etr_train_valid.joblib")
    test_df = load_dataset("region_test.csv")
    train_df = load_dataset("region_train.csv")
    valid_df = load_dataset("region_valid.csv")

    # ── Tab 0 : Feature Importance ──────────────────────────────────────────
    with tabs[0]:
        st.markdown("### Analyse SHAP — Valeurs de Shapley")
        st.markdown("""
Les **valeurs SHAP** mesurent la contribution marginale de chaque variable à chaque prédiction individuelle.
Contrairement à la feature importance globale, SHAP montre **comment** chaque variable influence la prédiction.
        """)

        if model is not None and test_df is not None:
            X_test, y_test = get_xy(test_df)
            try:
                import shap
                with st.spinner("Calcul des valeurs SHAP (échantillon 800 observations)..."):
                    X_shap = X_test.sample(n=min(800, len(X_test)), random_state=42)
                    explainer = shap.TreeExplainer(model)
                    shap_values = explainer.shap_values(X_shap)

                # fig, ax = plt.subplots(figsize=(9, 7))
                # fig.patch.set_facecolor('white')
                # shap.summary_plot(shap_values, X_shap, show=False, max_display=15,
                #                   plot_type="bar", color='#0f3460')
                # plt.title("SHAP — Importance globale (|SHAP| moyen)", fontweight='bold', fontsize=11)
                # plt.tight_layout()
                # st.pyplot(fig)
                # plt.close()

                fig2, ax2 = plt.subplots(figsize=(9, 7))
                fig2.patch.set_facecolor('white')
                shap.summary_plot(shap_values, X_shap, show=False, max_display=15)
                plt.title("SHAP — Beeswarm plot (impact × valeur)", fontweight='bold', fontsize=11)
                plt.tight_layout()
                st.pyplot(fig2)
                plt.close()
            except Exception as e:
                callout(f"SHAP non disponible : {e}. Installez shap pour activer cette section.", "warn")
                _show_shap_static()
        else:
            _show_shap_static()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("#### Résultats SHAP")
        st.markdown("""
        **Variables les plus influente:**

1. **`csi`** — Clear-sky index → très forte influence. Des valeurs élevées tendent à contribuer positivement à la prédiction.
2. **`dtch_solaire_abs_dt`** — Variation absolue récente de la production normalisée → forte influence.
3. **`dghi_abs_dt`** — Variation absolue récente de l’irradiance globale horizontale → forte influence.
4. **`bni`, `bhi`, `dhi`, `ghi`, `clear_sky_ghi`, `clear_sky_bni`** — Niveau d’irradiance disponible → influence modérée.

Le **SHAP plot** montre que `csi` élevé tend à pousser le modèle vers une prédiction plus élevée de la variabilité future. Physiquement, lorsque le rayonnement mesuré est proche du rayonnement théorique par ciel clair, la production solaire est significative ; une perturbation atmosphérique peut alors provoquer une variation plus visible.

Un `dtch_solaire_abs_dt` élevé pousse aussi la prédiction vers des valeurs plus fortes, car une production déjà instable augmente la probabilité d’une nouvelle variation importante.

""")

    # ── Tab 1 : Synthèse physique ────────────────────────────────────────────
    with tabs[1]:
        st.markdown("### Synthèse physique — Ce que le modèle a appris")

        insights = [
            ("☁️", "CSI (Clear Sky Index)", "#0f3460",
             "Variable la plus importante. Mesure l'état atmosphérique. Un CSI qui chute signale l'arrivée de nuages → variabilité probable."),
            ("⚡", "dtch_solaire_abs_dt", "#e94560",
             "Variation absolue récente de la production normalisée. Une production déjà instable prédit une forte variabilité future."),
            ("🔆", "dghi_abs_dt", "#1abc9c",
             "Variation absolue récente de l'irradiance. Un rayonnement solaire fortement variable prédit une forte variabilité de production."),
            # ("🌞", "clear_sky_bni / bni / ghi", "#f39c12",
            #  "Variables d'irradiance : distinguent les périodes où une variation de production est physiquement possible."),
            # ("🕐", "cos_hour / sin_hour / altitude", "#9b59b6",
            #  "Contexte temporel et géométrique : la variabilité ne se manifeste pas de la même façon à l'aube, à midi ou au coucher."),
        ]

        for icon, title, color, desc in insights:
            st.markdown(f"""
<div style='background:#f8f9fd;border-left:4px solid {color};border-radius:8px;padding:1rem 1.5rem;margin:.6rem 0;display:flex;gap:1rem;align-items:flex-start'>
<span style='font-size:1.5rem'>{icon}</span>
<div>
<strong style='color:{color}'>{title}</strong><br>
<span style='color:#444;font-size:.92rem'>{desc}</span>
</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")
        callout("""
<strong>Conclusion de l'interprétabilité :</strong><br>
        Le modèle apprend une relation <strong>physiquement cohérente</strong> — il prédit la variabilité solaire
        principalement à partir des indicateurs de clarté du ciel, des variations récentes de production
        et des variations récentes d'irradiance. Il ne peut prédire que <em>l'intensité</em> du changement
        futur, pas son sens (hausse ou baisse).
        """, "success")


