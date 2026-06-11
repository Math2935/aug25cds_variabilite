import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import plotly.graph_objects as go
#from utils import load_dataset, load_model, get_xy

from utils import slide_header, section, kpi, formula, callout
from utils import load_dataset, load_model, check_data_available, check_model_available, get_xy

# ─────────────────────────────────────────────────────────────────────────────
# PAGE MODÉLISATION
# ─────────────────────────────────────────────────────────────────────────────
def page_modelisation():
    slide_header(
        "Modélisation",
        "Du modèle naïf au meilleur modèle — Démarche progressive"
    )

    tabs = st.tabs([
        "Métriques & Baseline",
        "Modèles linéaires",
        "LazyPredict (2020-2023)",
        "Optimisation (2020-2024)",
        "Résultats sur 2025",
    ])

    # ── Tab 0 : Métriques & Baseline ────────────────────────────────────────
    with tabs[0]:
        st.markdown("### Métriques d'évaluation")

        col1, col2 = st.columns(2)
        with col1:
            metrics_data = {
                "Métrique": ["MAE", "NMAE", "RMSE", "R²", "Gap train/val"],
                # "Description": [
                #     "Erreur absolue moyenne — métrique principale",
                #     "MAE normalisée en % — interprétation intuitive",
                #     "Pénalise les grandes erreurs",
                #     "Part de variance expliquée",
                #     "Indicateur de surapprentissage"
                # ],
                "Rôle": ["Principal", "Secondaire", "Secondaire", "Secondaire", "Régularité"]
            }
            df_metrics = pd.DataFrame(metrics_data)

            def color_principal(val):
                if "Principal" in str(val):
                    return "color: red; font-weight: bold;"
                elif "Régularité" in str(val):
                    return "color: orange; font-weight: bold;"
                return "color: green; font-weight: bold;"

            st.dataframe(
                df_metrics.style.applymap(color_principal, subset=["Rôle"]),
                use_container_width=True,
                hide_index=True
            )

        with col2:
            st.markdown(r"$\displaystyle \mathrm{MAE}=\frac{1}{n}\sum_{i=1}^{n}|y_i-\hat{y}_i|$")
            st.markdown(r"$\displaystyle\mathrm{NMAE} = 100 \times \frac{\mathrm{MAE}}{\mathrm{mean}(|y_{\mathrm{true}}|)}$")
            st.markdown(r"$\displaystyle\mathrm{RMSE} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}$")

        st.markdown("---")
        st.markdown("### Modèle naïf de référence (Baseline)")
        st.markdown("""
La **baseline** prédit que la variabilité future sera proche de la dernière variation observée :
        """)
        st.markdown(r"""
        $$
        \hat{y}_{t+1} \approx \left|\Delta TCH_t\right|
        \qquad \longleftarrow \textbf{\textcolor{green}{variation récente de la production solaire}}
        $$
        """)

        callout("📌 Tout modèle plus sophistiqué doit surpasser cette baseline pour justifier sa complexité.", "warn")


    # ── Tab 1 : Modèles linéaires ────────────────────────────────────────────
    with (tabs[1]):
        st.markdown("### Pourquoi commencer par des modèles linéaires ?")
        st.markdown("""
        En première approximation, on peut s'appuyer sur un **modèle physique simplifié** du photovoltaïque :
        la puissance produite est approximativement proportionnelle à l'irradiance solaire reçue.

        Cette relation conduit naturellement à l'hypothèse que les variations de production sont liées aux variations d'irradiance.
        """)
        st.latex(r"P_t \approx \beta \cdot GHI_t  \longrightarrow  |\Delta P_t| \approx \beta \cdot  |\Delta GHI_t|")

#         st.markdown("---")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.markdown("#### Modèles testés")
#             models_lin = [
#                 ("Régression simple", "1 variable : |ΔGHI|", "Sans intercept"),
#                 ("Régression multivariée", "Toutes les variables", "Référence linéaire complète"),
#                 ("Ridge (L2)", "Régularisation L2", "Réduit les coefficients → colinéarité"),
#                 ("Lasso (L1)", "Régularisation L1", "Sélection de variables"),
#             ]
#             for name, desc, note in models_lin:
#                 st.markdown(f"- **{name}** — {desc} · *{note}*")
#
#         with col2:
#             st.markdown("#### Pourquoi Ridge et Lasso ?")
#             st.markdown("""
# Le jeu de données contient de **nombreuses variables corrélées** :
# - Variables retardées (lags 1, 2, 3)
# - Statistiques glissantes corrélées entre elles
# - Variables météo corrélées (GHI, BHI, DHI…)
#
# **Ridge** : stabilise les coefficients sans en éliminer
# **Lasso** : peut mettre des coefficients à 0 → sélection implicite
#             """)

        callout("La standardisation est obligatoire avant la régularisation — on utilise un Pipeline sklearn (StandardScaler + modèle).", "info")

        # Results table with known values
        # st.markdown("---")
        st.markdown("### Résultats sur validation 2024")

        results = pd.DataFrame([
            {"Modèle": "Naïf (baseline)", "MAE": "0.90", "NMAE (%)": "~38%", "R2": "0.76", "Gap_MAE": "0.05"},
            {"Modèle": "Régression linéaire simple", "MAE": "1.08", "NMAE (%)": "~45%", "R2": "0.62",
             "Gap_MAE": "0.05"},
            {"Modèle": "Régression linéaire multi", "MAE": "0.64", "NMAE (%)": "~27%", "R2": "0.88", "Gap_MAE": "0.02"},
            {"Modèle": "Ridge (optimal α)", "MAE": "0.63", "NMAE (%)": "~26%", "R2": "0.88", "Gap_MAE": "0.03"},
            {"Modèle": "Lasso (optimal α)", "MAE": "0.63", "NMAE (%)": "~26%", "R2": "0.88", "Gap_MAE": "0.03"},
        ])

        # Convert MAE to numeric
        results["MAE"] = results["MAE"].astype(float)

        # Sort from best to worst
        results_sorted = (
            results
            .sort_values("MAE", ascending=True)
            .reset_index(drop=True)
            .set_index("Modèle")
        )

        col1, col2 = st.columns([1, 1.5])

        with col1:

            def highlight_best_three(row):
                row_position = results_sorted.index.get_loc(row.name)
                styles = [""] * len(row)

                if row_position < 3:
                    mae_col_position = results_sorted.columns.get_loc("MAE")
                    styles[mae_col_position] = (
                        "background-color: #ffe5e5; "
                        "color: #c00000; "
                        "font-weight: bold;"
                    )

                return styles

            st.dataframe(
                results_sorted
                .style
                .apply(highlight_best_three, axis=1)
                .format({"MAE": "{:.2f}"}),
                use_container_width=True
            )

        with col2:

            fig, ax = plt.subplots(figsize=(5, 2.5))
            fig.patch.set_facecolor("white")

            colors_results = [
                "#e94560" if i < 3 else "#adb5bd"
                for i in range(len(results_sorted))
            ]

            ax.barh(
                results_sorted.index[::-1],
                results_sorted["MAE"][::-1],
                color=colors_results[::-1],
                alpha=0.85,
                edgecolor="white"
            )

            ax.set_xlabel("MAE validation")
            ax.set_title("Classement des modèles linéaires — MAE", fontweight="bold", fontsize=11)
            ax.grid(axis="x", alpha=0.3)
            ax.spines[["top", "right"]].set_visible(False)

            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        # st.dataframe(results, use_container_width=True, hide_index=True)

    # ── Tab 2 : LazyPredict ──────────────────────────────────────────────────
    with tabs[2]:
        st.markdown("### LazyPredict — Sélection exploratoire rapide")
#         st.markdown("""
# **LazyPredict** entraîne automatiquement plusieurs dizaines de modèles sklearn sur les données,
# pour identifier rapidement les **familles de modèles prometteuses** avant l'optimisation fine.
#         """)
#         st.markdown("#### Objectif de cette étape")
#         st.markdown("""
# **Avant LazyPredict :** on ne sait pas encore quelle famille choisir entre: Modèles linéaires / Arbres de décision simples /
# Random Forests / Extra Trees / Gradient Boosting (LGBM, XGBoost, HistGB) / SVR / K-Nearest Neighbors ...
#         """)
#         # st.markdown("---")
#         st.markdown("#### Découpage interne utilisé pour LazyPredict")
#         st.markdown("""
#                 Pour LazyPredict, on garde la logique chronologique: les modèles sont entraînés sur **2020–2022**, puis comparés sur **2023**.
#                 """)
#         # Les années **2024** et **2025** ne sont pas utilisées dans cette étape :
#         # 2024 reste pour la validation globale et 2025 pour le test final.
#         callout("⚠️ LazyPredict est utilisé sur les données d'entraînement uniquement — le test reste indépendant.","warn")
        fig, ax = plt.subplots(figsize=(15, 2.8))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        bars = [
            (2020, 3, "#0f3460", "TRAIN LazyPredict\n2020–2022"),
            (2023, 1, "#e94560", "VALIDATION interne\n2023"),
            (2024, 1, "#adb5bd", "VALID globale\n2024\n(non utilisée ici)"),
            (2025, 1, "#d0d0d0", "TEST final\n2025\njamais utilisé"),
        ]

        for start, width, color, label in bars:
            ax.barh(0, width, left=start, height=0.5, color=color, alpha=0.9)
            ax.text(
                start + width / 2,
                0,
                label,
                ha="center",
                va="center",
                color="white" if start <= 2023 else "#333333",
                fontweight="bold",
                fontsize=12
            )

        ax.set_xlim(2019.8, 2026.2)
        ax.set_ylim(-0.5, 0.5)
        ax.set_xlabel("Année")
        ax.set_yticks([])
        ax.set_title(
            "Découpage chronologique spécifique à LazyPredict",
            fontweight="bold",
            fontsize=16
        )
        ax.grid(axis="x", alpha=0.3)
        ax.spines[["top", "right", "left"]].set_visible(False)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Résumé statique des familles de modèles testées dans le notebook
        lazy_results = pd.DataFrame({
            "Modèle": [
                "ExtraTreesRegressor", "RandomForestRegressor", "LGBMRegressor",
                "HistGradientBoosting", "XGBRegressor", "GradientBoosting",
                "KNeighborsRegressor"
            ],
            "MAE": [0.465, 0.475, 0.493, 0.496, 0.509, 0.546, 0.549],
            "R²": [0.916, 0.913, 0.913, 0.911, 0.904, 0.903, 0.896]
        })

        lazy_results.index += 1

        col_t, col_p = st.columns([1, 2])

        with col_t:
            st.dataframe(lazy_results.set_index("Modèle"), use_container_width=True)

        with col_p:
            fig, ax = plt.subplots(figsize=(6, 3.5))
            fig.patch.set_facecolor("white")

            colors_lazy = ['#e94560' if i < 5 else '#adb5bd' for i in range(len(lazy_results))]

            ax.barh(
                lazy_results["Modèle"][::-1],
                lazy_results["MAE"][::-1],
                color=colors_lazy[::-1],
                alpha=0.85,
                edgecolor="white"
            )

            ax.set_xlabel("MAE validation interne 2023")
            ax.set_title("Classement LazyPredict — MAE validation interne", fontweight="bold", fontsize=11)
            ax.grid(axis="x", alpha=0.3)
            ax.set_xlim(0.40, 0.55)
            ax.spines[["top", "right"]].set_visible(False)

            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        st.markdown("""
        **Après LazyPredict :**
        - Les **modèles d'ensemble basés sur les arbres** dominent clairement
        - ExtraTrees, Random Forest, LGBM HistGradient et XGBoost ressortent systématiquement
                    """)

    # ── Tab 3 : Recherche des Hyperparamètres ────────────────────────────────────────────
    with tabs[3]:
        st.markdown("### Recherche des Hyperparamètres")
        # st.markdown("""
        #         Les 5 modèles retenus après LazyPredict sont optimisés avec **Optuna**.
        #
        #         Contrairement à LazyPredict, où **2023 servait de validation interne**, cette étape utilise
        #         **2024 comme année de validation** pour la recherche des hyperparamètres.
        #         """)

        fig, ax = plt.subplots(figsize=(15, 2.8))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        bars = [
            (2020, 5, "#0f3460", "Validation Croisée (Folds temporels)\n2020–2024\n"),
            (2025, 1, "#adb5bd", "TEST final\n2025\n(non utilisée ici)"),
        ]

        for start, width, color, label in bars:
            ax.barh(0, width, left=start, height=0.5, color=color, alpha=0.9)
            ax.text(
                start + width / 2,
                0,
                label,
                ha="center",
                va="center",
                color="white" if start <= 2024 else "#333333",
                fontweight="bold",
                fontsize=16
            )

        ax.set_xlim(2019.8, 2026.2)
        ax.set_ylim(-0.5, 0.5)
        ax.set_xlabel("Année")
        ax.set_yticks([])
        ax.set_title(
            "Découpage chronologique pour l’optimisation des hyperparamètres",
            fontweight="bold",
            fontsize=16
        )
        ax.grid(axis="x", alpha=0.3)
        ax.spines[["top", "right", "left"]].set_visible(False)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.markdown("### Synthèse des performances — Validation 2024")
        st.latex(r"\text{score} = MAE + RMSE + \frac{GAP}{MAE}")
        # Results table
        # results_df = pd.DataFrame([
        #     {"Modèle": "HistGradientBoosting", "MAE_valid": 0.473, "RMSE_valid": 1.016, "R2_valid": 0.90, "Gap_MAE": 0.03},
        #     {"Modèle": "ExtraTrees", "MAE_valid": 0.491, "RMSE_valid": 1.01, "R2_valid": 0.902, "Gap_MAE": 0.02},
        #     {"Modèle": "XGBoost", "MAE_valid": 0.50, "RMSE_valid": 1.01, "R2_valid": 0.90, "Gap_MAE": 0.02},
        #     {"Modèle": "LGBM", "MAE_valid": 0.49, "RMSE_valid": 1.00, "R2_valid": 0.90, "Gap_MAE": 0.04},
        #     {"Modèle": "Keras MLP", "MAE_valid": 0.49, "RMSE_valid": 1.03, "R2_valid": 0.90, "Gap_MAE": 0.02},
        #     {"Modèle": "RandomForest", "MAE_valid": 0.51, "RMSE_valid": 1.03, "R2_valid": 0.90, "Gap_MAE": 0.02},
        #     {"Modèle": "Régression linéaire multivariée", "MAE_valid": 0.64, "RMSE_valid": 1.13, "R2_valid": 0.88,
        #      "Gap_MAE": 0.02},
        #     {"Modèle": "Ridge", "MAE_valid": 0.63, "RMSE_valid": 1.13, "R2_valid": 0.88, "Gap_MAE": 0.03},
        #     {"Modèle": "Lasso", "MAE_valid": 0.63, "RMSE_valid": 1.12, "R2_valid": 0.88, "Gap_MAE": 0.03},
        #     {"Modèle": "Naïf", "MAE_valid": 0.90, "RMSE_valid": 1.59, "R2_valid": 0.76, "Gap_MAE": 0.05},
        #     {"Modèle": "Régression linéaire simple", "MAE_valid": 1.08, "RMSE_valid": 1.98, "R2_valid": 0.62,
        #      "Gap_MAE": 0.05},
        # ])
        results_df = pd.DataFrame([
            {"Modèle": "HistGradientBoosting", "MAE_valid": 0.473, "RMSE_valid": 1.016, "R2_valid": 0.90,
             "Gap_MAE": 0.03},
            {"Modèle": "ExtraTrees", "MAE_valid": 0.491, "RMSE_valid": 1.01, "R2_valid": 0.902, "Gap_MAE": 0.02},
            {"Modèle": "XGBoost", "MAE_valid": 0.50, "RMSE_valid": 1.01, "R2_valid": 0.90, "Gap_MAE": 0.02},
            {"Modèle": "LGBM", "MAE_valid": 0.49, "RMSE_valid": 1.00, "R2_valid": 0.90, "Gap_MAE": 0.04},
            # {"Modèle": "Keras MLP", "MAE_valid": 0.49, "RMSE_valid": 1.03, "R2_valid": 0.90, "Gap_MAE": 0.02},
            {"Modèle": "RandomForest", "MAE_valid": 0.51, "RMSE_valid": 1.03, "R2_valid": 0.90, "Gap_MAE": 0.02},
            # {"Modèle": "Régression linéaire multivariée", "MAE_valid": 0.64, "RMSE_valid": 1.13, "R2_valid": 0.88,
            #  "Gap_MAE": 0.02},
            # {"Modèle": "Ridge", "MAE_valid": 0.63, "RMSE_valid": 1.13, "R2_valid": 0.88, "Gap_MAE": 0.03},
            # {"Modèle": "Lasso", "MAE_valid": 0.63, "RMSE_valid": 1.12, "R2_valid": 0.88, "Gap_MAE": 0.03},
            # {"Modèle": "Naïf", "MAE_valid": 0.90, "RMSE_valid": 1.59, "R2_valid": 0.76, "Gap_MAE": 0.05},
            # {"Modèle": "Régression linéaire simple", "MAE_valid": 1.08, "RMSE_valid": 1.98, "R2_valid": 0.62,
            #  "Gap_MAE": 0.05},
        ])
        results_df["score"] = results_df.apply(
            lambda row: row["MAE_valid"] + row["RMSE_valid"] + max(0, row["Gap_MAE"]) / (row["MAE_valid"]),
            axis=1
        )
        results_df = results_df.sort_values("score")

        def highlight_best_score(row):
            if row["score"] == results_df["score"].min():
                return ["background-color: #e94560; color: white; font-weight: bold"] * len(row)
            return [""] * len(row)

        results_df["score"] = results_df.apply(
            lambda row: row["MAE_valid"] + row["RMSE_valid"] + max(0, row["Gap_MAE"]) / row["MAE_valid"],
            axis=1
        )

        # Trier par score croissant : meilleur modèle en premier
        results_df = results_df.sort_values("score", ascending=True).reset_index(drop=True)

        col_t, col_p = st.columns([1.2, 2])

        with col_t:
            def highlight_best_one(row):
                if row.name == 0:
                    return [
                        "background-color: #ffe5e5; color: #c00000; font-weight: bold;"
                    ] * len(row)
                return [""] * len(row)

            st.dataframe(
                results_df
                .style
                .apply(highlight_best_one, axis=1)
                .format({
                    "MAE_valid": "{:.3f}",
                    "RMSE_valid": "{:.3f}",
                    "R2_valid": "{:.3f}",
                    "Gap_MAE": "{:.3f}",
                    "score": "{:.3f}"
                }),
                use_container_width=True,
                hide_index=True
            )

        with col_p:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            fig.patch.set_facecolor("white")

            colors_score = [
                "#e94560" if i == 0 else "#adb5bd"
                for i in range(len(results_df))
            ]

            bars = ax.barh(
                results_df["Modèle"],
                results_df["score"],
                color=colors_score,
                alpha=0.9,
                edgecolor="white"
            )

            ax.invert_yaxis()  # meilleur modèle en haut

            ax.set_xlabel("Score")
            ax.set_title("Classement des modèles — Score croissant", fontweight="bold", fontsize=11)
            ax.grid(axis="x", alpha=0.3)
            ax.spines[["top", "right"]].set_visible(False)

            # Ajouter label pour le meilleur modèle
            best_model = results_df.iloc[0]["Modèle"]

            for bar, model in zip(bars, results_df["Modèle"]):
                if model == best_model:
                    ax.text(
                        bar.get_width() + 0.01,
                        bar.get_y() + bar.get_height() / 2,
                        "Modèle sélectionné",
                        va="center",
                        fontsize=9,
                        fontweight="bold",
                        color="#e94560"
                    )

            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        # st.dataframe(
        #     results_df.style
        #     .apply(highlight_best_score, axis=1)
        #     .format(precision=4),
        #     use_container_width=True,
        #     hide_index=True
        # )
        #
        # fig, axes = plt.subplots(1, 2, figsize=(13, 5))
        # fig.patch.set_facecolor("white")
        #
        # # MAE bar
        # ax = axes[0]
        #
        # colors_bar = [
        #     "#e94560" if m == "ExtraTrees" else "#0f3460"
        #     for m in results_df["Modèle"]
        # ]
        #
        # edges_bar = [
        #     "#e94560" if m == "ExtraTrees" else "white"
        #     for m in results_df["Modèle"]
        # ]
        #
        # linewidths = [
        #     2.5 if m == "ExtraTrees" else 0.8
        #     for m in results_df["Modèle"]
        # ]
        #
        # bars = ax.barh(
        #     results_df["Modèle"],
        #     results_df["MAE_valid"],
        #     color=colors_bar,
        #     alpha=0.9,
        #     edgecolor=edges_bar,
        #     linewidth=linewidths
        # )
        #
        # ax.set_xlabel("MAE validation")
        # ax.set_title("Classement par MAE — Validation 2024", fontweight="bold", fontsize=11)
        # ax.grid(axis="x", alpha=0.3)
        # ax.spines[["top", "right"]].set_visible(False)
        #
        # # Add label for ExtraTrees
        # for bar, model in zip(bars, results_df["Modèle"]):
        #     if model == "ExtraTrees":
        #         ax.text(
        #             bar.get_width() + 0.01,
        #             bar.get_y() + bar.get_height() / 2,
        #             "Modèle sélectionné",
        #             va="center",
        #             fontsize=9,
        #             fontweight="bold",
        #             color="#e94560"
        #         )
        #
        # # Gap scatter
        # ax = axes[1]
        #
        # for _, row in results_df.iterrows():
        #     is_final = row["Modèle"] == "ExtraTrees"
        #
        #     ax.scatter(
        #         row["MAE_valid"],
        #         row["Gap_MAE"],
        #         s=220 if is_final else 80,
        #         color="#e94560" if is_final else "#0f3460",
        #         edgecolor="black" if is_final else "white",
        #         linewidth=1.2 if is_final else 0.5,
        #         zorder=5 if is_final else 3,
        #         alpha=1.0 if is_final else 0.75
        #     )
        #
        #     ax.annotate(
        #         row["Modèle"],
        #         (row["MAE_valid"], row["Gap_MAE"]),
        #         xytext=(8, 5) if is_final else (5, 3),
        #         textcoords="offset points",
        #         fontsize=9 if is_final else 7.5,
        #         fontweight="bold" if is_final else "normal",
        #         color="#e94560" if is_final else "#333333"
        #     )
        #
        # ax.set_xlabel("MAE validation")
        # ax.set_ylabel("Gap MAE valid−train")
        # ax.set_title("MAE validation vs Gap de surapprentissage", fontweight="bold", fontsize=11)
        # ax.grid(True, alpha=0.3)
        # ax.spines[["top", "right"]].set_visible(False)
        #
        # plt.tight_layout()
        # st.pyplot(fig)
        # plt.close()

        st.markdown("#### Stratégie Optuna — Validation croisée temporelle")
        st.markdown("""
        **Pour chaque essai Optuna :**
        1. Optuna propose un jeu d'hyperparamètres
        2. Évaluation sur les 4 folds temporels
        3. Score = MAE moyenne sur les folds
        4. Optuna ajuste la direction de recherche
        5. Meilleurs paramètres → entraînement final sur train complet
                    """)
    # # ── Tab 5 : Évaluation sur Test ───────────────────────────────────
    # with tabs[4]:
    #     fig, ax = plt.subplots(figsize=(15, 2.8))
    #     fig.patch.set_facecolor("white")
    #     ax.set_facecolor("white")
    #
    #     bars = [
    #         (2020, 5, "#0f3460", "Entraînement du modèle final ExtraTreesRegressor\n2020–2024\n"),
    #         (2025, 1, "#e94560", "Test final\n2025\n"),
    #     ]
    #
    #     for start, width, color, label in bars:
    #         ax.barh(0, width, left=start, height=0.5, color=color, alpha=0.9)
    #         ax.text(
    #             start + width / 2,
    #             0,
    #             label,
    #             ha="center",
    #             va="center",
    #             color="white",
    #             fontweight="bold",
    #             fontsize=16
    #         )
    #
    #     ax.set_xlim(2019.8, 2026.2)
    #     ax.set_ylim(-0.5, 0.5)
    #     ax.set_xlabel("Année")
    #     ax.set_yticks([])
    #     ax.set_title(
    #         "Découpage chronologique pour l’optimisation des hyperparamètres",
    #         fontweight="bold",
    #         fontsize=16
    #     )
    #     ax.grid(axis="x", alpha=0.3)
    #     ax.spines[["top", "right", "left"]].set_visible(False)
    #
    #     plt.tight_layout()
    #     st.pyplot(fig)
    #     plt.close()
    #
    #     st.markdown("#### Résultats finaux sur le jeu de test (2025)")
    #
    #     test_df = load_dataset("region_test.csv")
    #     model = load_model("final_model_etr_train_valid.joblib")
    #
    #     X_val, y_val = get_xy(test_df)
    #     X_val_aligned = X_val[[c for c in X_val.columns if c in X_val.columns]]
    #     y_pred = model.predict(X_val_aligned)
    #     from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    #     mae = mean_absolute_error(y_val, y_pred)
    #     r2 = r2_score(y_val, y_pred)
    #     rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    #
    #     st.markdown(f"""<div class='kpi-row'>
    #             {kpi(f"{mae:.4f}", "MAE Test")}
    #             {kpi(f"{rmse:.4f}", "RMSE Test", "orange")}
    #             {kpi(f"{r2:.4f}", "R² Test", "green")}
    #             {kpi("~0", "Gap MAE test/train", "accent")}
    #             </div>""", unsafe_allow_html=True)
    #     callout(
    #         "✅ Le gap MAE test/train est quasi nul — le modèle <strong>généralise bien</strong> sur des données futures jamais vues.",
    #         "success")
    #
    #     fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    #     fig.patch.set_facecolor('white')
    #
    #     # Scatter
    #     ax = axes[0]
    #     ax.scatter(y_val, y_pred, alpha=0.5, s=8, color='#0f3460')
    #     min_val = min(y_val.min(), y_pred.min())
    #     max_val = max(y_val.max(), y_pred.max())
    #     ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=1.5, label='Prédiction parfaite')
    #     ax.set_xlabel("Réel")
    #     ax.set_ylabel("Prédit")
    #     ax.set_title("Réel vs Prédit — ExtraTrees (Test 2025)", fontweight='bold', fontsize=10)
    #     ax.legend()
    #     ax.grid(True, alpha=0.3)
    #     ax.spines[['top', 'right']].set_visible(False)
    #
    #     # Time series
    #     ax = axes[1]
    #     july_mask = (y_val.index.month == 7)
    #     y_july = y_val[july_mask]
    #     y_pred_july = y_pred[july_mask]
    #
    #     ax.plot(y_july.index[150:450], y_july.values[150:450], color='#0f3460', linewidth=1, label='Réel', alpha=0.8)
    #     ax.plot(y_july.index[150:450], y_pred_july[150:450], color='#e94560', linewidth=1, label='Prédit', alpha=0.7)
    #     ax.set_xlabel("Date")
    #     ax.set_ylabel("|ΔTCH|")
    #     ax.set_title("Série temporelle — Juillet 2025", fontweight='bold', fontsize=10)
    #     ax.legend()
    #     ax.grid(True, alpha=0.3)
    #     ax.spines[['top', 'right']].set_visible(False)
    #     ax.tick_params(axis='x', rotation=30)
    #
    #     plt.tight_layout()
    #     st.pyplot(fig)
    #     plt.close()
    # ── Tab 5 : Évaluation sur Test ───────────────────────────────────
    with tabs[4]:

        st.markdown("### Évaluation finale du modèle")

        # Timeline simple
        fig, ax = plt.subplots(figsize=(12, 1.8))
        fig.patch.set_facecolor("white")

        ax.barh(0, 5, left=2020, height=0.5, color="#0f3460", alpha=0.9)
        ax.barh(0, 1, left=2025, height=0.5, color="#e94560", alpha=0.9)

        ax.text(
            2022.5, 0,
            "Entraînement final\n2020–2024",
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=13
        )

        ax.text(
            2025.5, 0,
            "Test final\n2025",
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=13
        )

        ax.set_xlim(2019.8, 2026.2)
        ax.set_yticks([])
        ax.set_xlabel("Année")
        ax.set_title(
            "Découpage chronologique pour l’évaluation finale",
            fontweight="bold",
            fontsize=14
        )
        ax.grid(axis="x", alpha=0.3)
        ax.spines[["top", "right", "left"]].set_visible(False)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Chargement des données et du modèle
        test_df = load_dataset("region_test.csv")
        model = load_model("final_model_etr_train_valid.joblib")

        X_test, y_test = get_xy(test_df)
        y_pred = model.predict(X_test)

        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        st.markdown("#### Résultats finaux sur le jeu de test 2025")

        st.markdown(f"""
        <div class='kpi-row'>
            {kpi(f"{mae:.4f}", "MAE Test")}
            {kpi(f"{rmse:.4f}", "RMSE Test", "orange")}
            {kpi(f"{r2:.4f}", "R² Test", "green")}
            {kpi("≈ 0", "Gap test/train", "accent")}
        </div>
        """, unsafe_allow_html=True)

        callout(
            "✅ Les résultats montrent que le modèle garde de bonnes performances sur l’année 2025, qui n’a jamais été utilisée pendant l’entraînement.",
            "success"
        )

        # Graphique simple réel vs prédit
        st.markdown("#### Exemple de comparaison entre valeurs réelles et prédites")
        july_mask = (y_test.index.month == 7)
        y_july = y_test[july_mask]
        y_pred_july = y_pred[july_mask]

        fig, ax = plt.subplots(figsize=(8, 3))
        fig.patch.set_facecolor("white")

        ax.plot(y_july.index[450:850], y_july[450:850],
            # y_test.index[:n_show],
            # y_test.values[:n_show],
            label="Réel",
            linewidth=1.5,
            color="#0f3460"
        )

        ax.plot(y_july.index[450:850], y_pred_july[450:850],
            # y_test.index[:n_show],
            # y_pred[:n_show],
            label="Prédit",
            linewidth=1.5,
            color="#e94560",
            alpha=0.8
        )

        ax.set_xlabel("Date")
        ax.set_ylabel("Variabilité solaire")
        # ax.set_title("Comparaison Réel vs Prédit — Test 2025", fontweight="bold", fontsize=12)

        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(axis="x", rotation=30)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
