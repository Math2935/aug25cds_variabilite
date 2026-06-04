import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import os

current_path = Path().resolve()
base = ''
if current_path.name != 'aug25cds_variabilite':
    base = '../'
DATA_DIR = Path(base+"data")
MODELS_DIR = Path(base+"data/models")

@st.cache_data(show_spinner=False)
def load_dataset(name):
    """Load a CSV from the data/ directory."""
    path = DATA_DIR / name
    if not path.exists():
        return None
    return pd.read_csv(path, index_col="datetime_utc", parse_dates=True)

@st.cache_resource(show_spinner=False)
def load_model(name):
    """Load a joblib model from the models/ directory."""
    try:
        import joblib
        path = MODELS_DIR / name
        if not path.exists():
            return None
        return joblib.load(path)
    except Exception:
        return None

def check_data_available():
    """Return dict with availability status."""
    files = {
        "region_train.csv": "Train",
        "region_valid.csv": "Validation",
        "region_test.csv":  "Test",
    }
    status = {}
    for f, label in files.items():
        status[label] = (DATA_DIR / f).exists()
    return status

def check_model_available():
    """Return dict with model availability."""
    models = {
        "final_model_etr_train_valid.joblib": "ExtraTreesRegressor (final)",
    }
    status = {}
    for f, label in models.items():
        status[label] = (MODELS_DIR / f).exists()
    return status

def get_xy(df):
    X = df.drop(columns=["target"], errors="ignore")
    y = df["target"] if "target" in df.columns else None
    return X, y

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def slide_header(title, subtitle=""):
    st.markdown(f"""
    <div class="slide-header">
        <h1>{title}</h1>
        {"<p>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)

def section(title="", content_fn=None):
    if title:
        st.markdown(f"<div class='slide-section'><h2>{title}</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='slide-section'>", unsafe_allow_html=True)
    if content_fn:
        content_fn()
    st.markdown("</div>", unsafe_allow_html=True)

def kpi(value, label, variant=""):
    cls = f"kpi-card {variant}"
    return f"<div class='{cls}'><div class='kpi-value'>{value}</div><div class='kpi-label'>{label}</div></div>"

def formula(text):
    st.markdown(f"<div class='formula-box'>{text}</div>", unsafe_allow_html=True)

def callout(text, kind="info"):
    css = {"info": "callout-info", "warn": "callout", "success": "callout-success"}.get(kind, "callout-info")
    st.markdown(f"<div class='{css}'>{text}</div>", unsafe_allow_html=True)

def step_badge(n, text):
    st.markdown(f"<p><span class='step-badge'>{n}</span> {text}</p>", unsafe_allow_html=True)


def load_first_available_dataset(*names):
    """Charge le premier CSV disponible parmi une liste de noms."""
    for name in names:
        try:
            df = load_dataset(name)
            if df is not None and not df.empty:
                return df, name
        except Exception:
            pass
    return None, None

def existing_cols(df, cols):
    """Retourne seulement les colonnes présentes dans un DataFrame."""
    if df is None:
        return []
    return [c for c in cols if c in df.columns]

def make_demo_region_profile(n=96):
    """Profil didactique cohérent avec les variables des notebooks: GHI, clear_sky_ghi, CSI, TCH et target."""
    idx = pd.date_range("2024-06-21", periods=n, freq="30min")
    h = idx.hour + idx.minute / 60
    clear = np.maximum(0, np.sin(np.pi * (h - 5.5) / 15.0)) * 900
    cloud = 1 - 0.45 * np.exp(-((h - 10.5) / 1.3) ** 2) - 0.35 * np.exp(-((h - 15.0) / 1.0) ** 2)
    cloud = np.clip(cloud, 0.15, 1)
    ghi = clear * cloud
    csi = np.where(clear > 10, ghi / clear, 0)
    tch = np.clip(ghi / 1000 * 100, 0, None)
    df = pd.DataFrame({
        "clear_sky_ghi": clear,
        "ghi": ghi,
        "csi": csi,
        "tch_solaire": tch,
    }, index=idx)
    df["dghi_abs_dt"] = df["ghi"].diff().abs().fillna(0)
    df["dtch_solaire_abs_dt"] = df["tch_solaire"].diff().abs().fillna(0)
    df["target"] = df["tch_solaire"].shift(-1).sub(df["tch_solaire"]).abs().fillna(0)
    return df
