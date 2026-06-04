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
# PAGE RAMPES CRITIQUES
# ─────────────────────────────────────────────────────────────────────────────
def page_rampes():
    slide_header(
        "Détection des Rampes Critiques",
        "Événements extrêmes au seuil Q90 · Classification binaire"
    )

    tabs = st.tabs([
        "Principe",
        "Résultats Q90",
        "Ajustement du seuil"
    ])

    model = load_model("final_model_etr_train_valid.joblib")
    test_df = load_dataset("region_test.csv")
    train_df = load_dataset("region_train.csv")
    valid_df = load_dataset("region_valid.csv")

    # Compute predictions
    X_test, y_test_val = get_xy(test_df)
    y_pred_test = model.predict(X_test)
    y_dev = pd.concat([train_df['target'], valid_df['target']])
    seuil_q90 = y_dev.quantile(0.90)


    # ── Tab 0 : Principe ────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown("### De la régression à la classification d'événements extrêmes")
        st.markdown("""
En plus des métriques classiques de régression (MAE, R²), on évalue la capacité du modèle
à **détecter les rampes critiques** — les fortes variations de production.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Définition")
            formula("Seuil Q90 = 90e percentile(target sur train+valid)<br><br>Événement critique : target ≥ Q90<br>Alerte modèle  : prédiction ≥ Q90")
            callout("Le seuil Q90 est calculé <strong>uniquement sur train+valid</strong> — jamais sur le test (anti-fuite).", "warn")
        with col2:
            st.markdown("#### Pourquoi le recall ?")
            st.markdown("""
Dans une application de gestion de réseau :
- **Faux négatif** = rampe critique non détectée → **coûteux opérationnellement**
- **Faux positif** = fausse alerte → acceptable

Le **recall** est la métrique prioritaire : minimiser les rampes manquées.
            """)

    # ── Tab 1 : Résultats Q90 ────────────────────────────────────────────────
    with tabs[1]:
        st.markdown(f"### Résultats au seuil Q90 = {seuil_q90:.2f}")

        from sklearn.metrics import recall_score, precision_score, f1_score, confusion_matrix
        y_true_evt = (y_test_val >= seuil_q90).astype(int)
        y_pred_evt = (y_pred_test >= seuil_q90).astype(int)

        recall = recall_score(y_true_evt, y_pred_evt)
        precision = precision_score(y_true_evt, y_pred_evt)
        f1 = f1_score(y_true_evt, y_pred_evt)

        st.markdown(f"""<div class='kpi-row'>
                        {kpi(f"{recall:.1%}", "Recall Q90", "green")}
                        {kpi(f"{precision:.1%}", "Précision Q90", "")}
                        {kpi(f"{f1:.3f}", "F1-Score Q90", "orange")}
                        {kpi(f"{int(y_true_evt.sum())}", "Rampes réelles", "accent")}
                        </div>""", unsafe_allow_html=True)

        # st.markdown("### Matrice de confusion — Seuil Q90")

        from sklearn.metrics import confusion_matrix
        y_true_evt = (y_test_val >= seuil_q90).astype(int)
        y_pred_evt = (y_pred_test >= seuil_q90).astype(int)
        cm = confusion_matrix(y_true_evt, y_pred_evt)

        fig, ax = plt.subplots(figsize=(5, 3.5))
        fig.patch.set_facecolor('white')
        labels = [['VN\n(Correct non-critique)', 'FP\n(Fausse alerte)'],
                  ['FN\n(Rampe manquée)', 'VP\n(Rampe détectée)']]

        sns.heatmap(cm, annot=False, fmt='d', cmap='Blues', cbar=False,
                    xticklabels=['Prédit: Non critique', 'Prédit: Critique'],
                    yticklabels=['Réel: Non critique', 'Réel: Critique'],
                    ax=ax, linewidths=2, linecolor='white')
        for i in range(2):
            for j in range(2):
                color = 'white' if cm[i, j] > cm.max() * 0.5 else '#333'
                ax.text(j + 0.5, i + 0.3, f"{cm[i, j]:,}", ha='center', va='center',
                        fontsize=16, fontweight='bold', color=color)
                ax.text(j + 0.5, i + 0.65, labels[i][j], ha='center', va='center',
                        fontsize=8, color='white' if cm[i, j] > cm.max() * 0.5 else '#666')
        ax.set_title("Matrice de confusion", fontweight='bold', fontsize=11, pad=12)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
        - **VN**: situations normales correctement identifiées
        - **FP**: fausses alertes
        - **FN**: rampes critiques **manquées** ← cas les plus coûteux
        - **VP**: rampes critiques correctement détectées ✅
                    """)
        with col2:
            callout(
                "Les <strong>faux négatifs (FN)</strong> sont les cas les plus problématiques dans une application de gestion de réseau électrique.",
                "warn")

        st.markdown("""
                **Interprétation :**
                - Le modèle détecte correctement **984 rampes critiques** sur 1284 présentes
                - Il manque **300 événements** critiques (≈ 23.4% non détectés)
                - Il produit **217 fausses alertes** sur 16 227 situations non critiques
                - Quand il prédit une rampe, il a raison dans **81.9%** des cas
                            """)

    # ── Tab 2 : Ajustement du seuil ──────────────────────────────────────────
    with tabs[2]:
        st.markdown("### Ajustement du seuil de décision")
        st.markdown("""
En abaissant le **seuil appliqué aux prédictions** (distinct du seuil Q90 sur les vraies valeurs),
on peut augmenter le recall au prix d'une précision plus faible.
        """)

        from sklearn.metrics import recall_score, precision_score, f1_score
        y_true_evt = (y_test_val >= seuil_q90).astype(int)

        seuils_range = np.linspace(y_pred_test.min(), y_pred_test.max(), 80)
        rows = []
        for s in seuils_range:
            yp = (y_pred_test >= s).astype(int)
            rows.append({
                'seuil': s,
                'recall': recall_score(y_true_evt, yp),
                'precision': precision_score(y_true_evt, yp),
                'f1': f1_score(y_true_evt, yp),
                'n_alertes': int(yp.sum())
            })
        seuils_df = pd.DataFrame(rows)

        seuil_85 = seuils_df.loc[
            seuils_df["recall"].sub(0.85).abs().idxmin(),
            "seuil"
        ]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=seuils_df["seuil"],
            y=seuils_df["recall"],
            mode="lines",
            name="Recall",
            line=dict(color="#1abc9c", width=3)
        ))

        fig.add_trace(go.Scatter(
            x=seuils_df["seuil"],
            y=seuils_df["precision"],
            mode="lines",
            name="Précision",
            line=dict(color="#0f3460", width=3)
        ))

        fig.add_trace(go.Scatter(
            x=seuils_df["seuil"],
            y=seuils_df["f1"],
            mode="lines",
            name="F1-Score",
            line=dict(color="#e94560", width=3, dash="dash")
        ))

        fig.add_trace(go.Scatter(
            x=[seuil_85, seuil_85],
            y=[0, 1],
            mode="lines+text",
            name="Recall ≥ 85%",
            line=dict(color="#f39c12", width=3, dash="dot"),
            text=["", "Recall ≥ 85%"],
            textposition="top center",
            textfont=dict(color="#f39c12", size=12),
            cliponaxis=False
        ))

        fig.add_trace(go.Scatter(
            x=[seuil_q90, seuil_q90],
            y=[0, 1],
            mode="lines+text",
            name="seuil_Q90",
            line=dict(color="#e94560", width=3, dash="dot"),
            text=["", "seuil_Q90"],
            textposition="top center",
            textfont=dict(color="#e94560", size=12),
            cliponaxis=False
        ))

        fig.update_layout(
            title="Précision, Recall, F1 en fonction du seuil de décision",
            xaxis_title="Seuil de décision (prédictions)",
            yaxis_title="Score",
            height=460,
            hovermode="x unified",
            legend=dict(
                orientation="v",
                # y=1.08,
                # x=0
            ),
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.15)")
        fig.update_yaxes(range=[0, 1], showgrid=True, gridcolor="rgba(0,0,0,0.15)")

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Résultats avec seuil optimisé (Recall ≥ 85%)")
        st.markdown("""<div class='kpi-row'>""" +
            kpi("85.5%", "Recall optimisé", "green") +
            kpi("67.7%", "Précision optimisée", "orange") +
            kpi("0.756", "F1-Score optimisé", "") +
            kpi("523", "Fausses alertes", "accent") +
        """</div>""", unsafe_allow_html=True)

        st.markdown(f"### Résultats au seuil Q90")

        # from sklearn.metrics import recall_score, precision_score, f1_score, confusion_matrix
        # y_true_evt = (y_test_val >= seuil_q90).astype(int)
        # y_pred_evt = (y_pred_test >= seuil_q90).astype(int)
        #
        # recall = recall_score(y_true_evt, y_pred_evt)
        # precision = precision_score(y_true_evt, y_pred_evt)
        # f1 = f1_score(y_true_evt, y_pred_evt)

        st.markdown(f"""<div class='kpi-row'>
                                {kpi(f"{recall:.1%}", "Recall Q90", "green")}
                                {kpi(f"{precision:.1%}", "Précision Q90", "orange")}
                                {kpi(f"{f1:.3f}", "F1-Score Q90", "")}
                                {kpi("217", "Fausses alertes", "accent")}
                                </div>""", unsafe_allow_html=True)
        callout("""
<strong>Compromis opérationnel :</strong><br>
• Seuil Q90 (8.04): Recall 76.6%, Précision 81.9% → moins de fausses alertes<br>
• Seuil optimisé (7.37): Recall 85.5%, Précision 67.7% → moins de rampes manquées<br>
Le choix dépend du coût relatif entre une rampe manquée et une fausse alerte.
        """, "warn")
        st.markdown("</div>", unsafe_allow_html=True)

