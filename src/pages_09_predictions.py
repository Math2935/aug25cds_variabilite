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
# PAGE PRÉDICTION EN LIGNE
# ─────────────────────────────────────────────────────────────────────────────
def page_prediction():
    """
    Page de prédiction en ligne adaptée du pasted text.
    Elle permet de choisir un instant t, de charger le modèle sauvegardé,
    d'obtenir la variabilité prédite à t+1 et l'alerte associée.
    """
    slide_header(
        "Prédiction en ligne",
        "Simulation opérationnelle : choisir un instant t, charger le modèle sauvegardé, obtenir la variabilité prédite à t+1 et l'alerte associée."
    )

    # -------------------------------------------------------------------------
    # Chargement des données et du modèle
    # -------------------------------------------------------------------------
    q_event = 0.90

    train = load_dataset("region_train.csv")
    valid = load_dataset("region_valid.csv")
    test = load_dataset("region_test.csv")
    model = load_model("final_model_etr_train_valid.joblib")

    csv_ok = test is not None
    model_ok = model is not None

    if not csv_ok or not model_ok:
        callout(
            "L'application reste tolérante : vous pouvez déposer les CSV dans <code>data/</code> "
            "et le modèle <code>.joblib</code> dans <code>models/</code>, ou charger un CSV manuellement ci-dessous.",
            "warn"
        )

    uploaded_csv = st.file_uploader(
        "Ou charger un CSV de prédiction contenant les mêmes features que l'entraînement",
        type=["csv"]
    )

    # -------------------------------------------------------------------------
    # Préparation des données de prédiction
    # -------------------------------------------------------------------------
    if uploaded_csv is not None:
        try:
            live_df = pd.read_csv(uploaded_csv, index_col="datetime_utc", parse_dates=True).sort_index()
        except Exception:
            # Fallback si la colonne datetime_utc n'existe pas dans le CSV uploadé
            live_df = pd.read_csv(uploaded_csv, index_col=0, parse_dates=True).sort_index()

        if "target" in live_df.columns:
            y_live = live_df["target"]
            X_live = live_df.drop(columns=["target"])
        else:
            y_live = None
            X_live = live_df

    elif csv_ok:
        live_df = test.copy()
        X_live, y_live = get_xy(live_df)
    else:
        st.warning("Chargez un CSV ou déposez `region_test.csv` dans `data/`.")
        st.stop()

    # -------------------------------------------------------------------------
    # Seuil d'alerte
    # -------------------------------------------------------------------------
    if train is not None and valid is not None and "target" in train.columns and "target" in valid.columns:
        seuil = pd.concat([train["target"], valid["target"]]).sort_index().quantile(q_event)
    elif y_live is not None:
        seuil = y_live.quantile(q_event)

    # -------------------------------------------------------------------------
    # Sélection d'un instant
    # -------------------------------------------------------------------------
    st.markdown("## 1. Sélection d'un instant")

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_date = st.date_input(
            "Date",
            value=X_live.index[0].date(),
            min_value=X_live.index.min().date(),
            max_value=X_live.index.max().date(),
            width=300
        )

    with col2:
        day_mask = X_live.index.date == selected_date
        times_available = X_live.index[day_mask]

        if len(times_available) == 0:
            st.warning("Pas de données ce jour-là.")
            st.stop()

        selected_time = st.selectbox(
            "Heure UTC",
            [t.strftime("%H:%M") for t in times_available]
        )

    matching = times_available[times_available.strftime("%H:%M") == selected_time]

    if len(matching) == 0:
        st.warning("Timestamp introuvable.")
        st.stop()

    selected_ts = matching[0]

    X_one = X_live.loc[[selected_ts]]
    pred_one = float(np.clip(model.predict(X_one)[0], 0, None))
    critical = pred_one >= 7.37

    c1, c2, c3 = st.columns(3)

    c1.metric("Variabilité prédite", f"{pred_one:.5f}")
    # c2.metric(f"Seuil Q{int(q_event * 100)}", f"{seuil:.2f}")
    c2.metric("Seuil", "7.37")
    c3.metric("Décision", "⚠️ Alerte" if critical else "✅ Normal")

    real = float(y_live.loc[selected_ts])
    st.metric(
        "Variabilité réelle observée",
        f"{real:.5f}",
        delta=f"erreur abs. {abs(real - pred_one):.5f}"
    )

    if critical:
        # st.markdown(
        #     "<div class='warn'><b>⚠️ <strong>ALERTE RAMPE CRITIQUE</strong>.</b> "
        #     f"Variabilité prédite {pred_one:.3f} ≥ seuil Q{int(q_event * 100)} ({seuil:.3f}). "
        #     "Le modèle prévoit une variation solaire importante au prochain pas de temps.</div>"
        #     , unsafe_allow_html=True
        # )
        st.markdown(
            "<div class='warn'><b>⚠️ <strong>ALERTE RAMPE CRITIQUE</strong>.</b> "
            f"Variabilité prédite {pred_one:.3f} ≥ seuil (7.37). "
            "Le modèle prévoit une variation solaire importante au prochain pas de temps.</div>"
            , unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div class='ok'><b>✅ Situation normale.</b> "
            "La variabilité prédite reste sous le seuil critique.</div>"
            , unsafe_allow_html=True
        )

    # -------------------------------------------------------------------------
    # Contexte temporel
    # -------------------------------------------------------------------------
    st.markdown("## 2. Contexte temporel")

    try:
        preds_live = np.clip(model.predict(X_live), 0, None)
    except Exception as e:
        st.error(f"Erreur lors de la prédiction globale : {e}")
        st.stop()

    window = st.slider(
        "Fenêtre autour de l'instant sélectionné (heures)",
        12,
        48,
        12
    )

    start = selected_ts - pd.Timedelta(hours=window)
    end = selected_ts

    mask = (X_live.index >= start) & (X_live.index <= end)

    ctx = pd.DataFrame(
        {"Prédit": preds_live[mask]},
        index=X_live.index[mask]
    )

    if y_live is not None:
        ctx["Réel"] = y_live.loc[ctx.index]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ctx.index,
            y=ctx["Prédit"],
            mode="lines",
            name="Prédit"
        )
    )

    if "Réel" in ctx.columns:
        fig.add_trace(
            go.Scatter(
                x=ctx.index,
                y=ctx["Réel"],
                mode="lines",
                name="Réel"
            )
        )

    fig.add_hline(
        y=7.37,
        line_dash="dash",
        # annotation_text=f"Q{int(q_event * 100)}"
    )

    # Ligne verticale corrigée pour éviter l'erreur Timestamp + Plotly
    fig.add_shape(
        type="line",
        x0=selected_ts,
        x1=selected_ts,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(dash="dot", width=2)
    )

    fig.add_annotation(
        x=selected_ts,
        y=1,
        xref="x",
        yref="paper",
        text="instant choisi",
        showarrow=False,
        yshift=12
    )

    fig.update_layout(
        height=460,
        title="Contexte réel/prédit autour de l'instant choisi",
        xaxis_title="Date / Heure UTC",
        yaxis_title="Variabilité solaire",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Voir les variables d'entrée à l'instant t"):
        st.dataframe(
            X_one.T.rename(columns={selected_ts: "valeur"}),
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)


