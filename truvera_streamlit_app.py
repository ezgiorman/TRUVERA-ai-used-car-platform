import os
import math
import pickle
from pathlib import Path
import base64

import numpy as np
import pandas as pd
import streamlit as st

# ============================================================
# TRUVERA - Tesla Style Streamlit App
# ============================================================

st.set_page_config(
    page_title="Truvera | AI Used Car Intelligence",
    page_icon=":car:",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_base64_image(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


BASE_DIR = Path(__file__).resolve().parent
car_img = get_base64_image(BASE_DIR / "assets" / "car.jpg")

# ------------------------------------------------------------
# CSS - Tesla inspired dark premium UI
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 20% 10%, rgba(255,255,255,0.08), transparent 28%),
            radial-gradient(circle at 80% 20%, rgba(140,140,140,0.12), transparent 32%),
            linear-gradient(135deg, #050505 0%, #0b0d10 45%, #111318 100%);
        color: #f5f5f5;
    }

    section[data-testid="stSidebar"] {
        background: rgba(15, 17, 21, 0.95);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #f2f2f2 !important;
    }

    .main .block-container {
        padding-top: 1.4rem;
        padding-bottom: 3rem;
        max-width: 1320px;
    }

    .hero {
    position: relative;
    overflow: hidden;
    border-radius: 34px;
    min-height: 420px;
    padding: 48px;
    background:
        linear-gradient(90deg, rgba(0,0,0,0.96) 0%, rgba(0,0,0,0.78) 45%, rgba(0,0,0,0.18) 100%),
        url("data:image/jpg;base64,__CAR_IMAGE__");
    background-size: cover;
    background-position: center right;
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 28px 80px rgba(0,0,0,0.55);
}

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: #c7c7c7;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 13px;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: 22px;
    }

    .hero h1 {
        font-size: clamp(44px, 5vw, 76px);
        line-height: .92;
        letter-spacing: -0.06em;
        margin: 0;
        color: #ffffff;
        font-weight: 800;
        max-width: 760px;
    }

    .hero p {
        margin-top: 24px;
        font-size: 18px;
        line-height: 1.7;
        color: rgba(255,255,255,0.76);
        max-width: 610px;
    }

    .hero-actions {
        display: flex;
        gap: 14px;
        margin-top: 34px;
        flex-wrap: wrap;
    }

    .pill {
        padding: 13px 22px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 14px;
        border: 1px solid rgba(255,255,255,0.16);
    }

    .pill.primary {
        background: #f5f5f5;
        color: #050505;
    }

    .pill.secondary {
        background: rgba(255,255,255,0.08);
        color: #fff;
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.11), rgba(255,255,255,0.055));
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 28px;
        padding: 26px;
        min-height: 164px;
        box-shadow: 0 22px 50px rgba(0,0,0,0.28);
    }

    .metric-card .label {
        color: rgba(255,255,255,0.62);
        font-size: 13px;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .metric-card .value {
        color: #fff;
        font-size: 36px;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-bottom: 8px;
    }

    .metric-card .sub {
        color: rgba(255,255,255,0.62);
        font-size: 14px;
    }

    .panel {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 30px;
        padding: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.24);
    }

    .section-title {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #fff;
        margin: 16px 0 8px 0;
    }

    .section-subtitle {
        color: rgba(255,255,255,0.62);
        font-size: 15px;
        margin-bottom: 20px;
    }

    .gauge-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        min-height: 260px;
    }

    .gauge {
        width: 220px;
        height: 220px;
        border-radius: 50%;
        display: grid;
        place-items: center;
        background:
            radial-gradient(circle closest-side, #111318 76%, transparent 77% 100%),
            conic-gradient(#ffffff calc(var(--score) * 1%), rgba(255,255,255,0.13) 0);
        box-shadow: 0 0 60px rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.08);
    }

    .gauge-inner {
        text-align: center;
    }

    .gauge-score {
        font-size: 48px;
        font-weight: 800;
        color: #fff;
        letter-spacing: -0.06em;
    }

    .gauge-label {
        color: rgba(255,255,255,0.58);
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: .12em;
    }

    .verdict {
        padding: 16px 18px;
        border-radius: 18px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        color: #fff;
        font-weight: 700;
        margin-top: 18px;
        text-align: center;
    }

    .tiny-note {
        color: rgba(255,255,255,0.56);
        font-size: 13px;
        line-height: 1.6;
    }

    .stButton > button {
    width: 100%;
    border-radius: 999px;
    min-height: 54px;
    border: none;
    background: #000000;
    color: #ffffff !important;
    font-weight: 800;
    font-size: 15px;
    box-shadow: 0 14px 40px rgba(255,255,255,0.08);
}

    .stButton > button:hover {
    background: #111111;
    color: #ffffff !important;
    transform: translateY(-1px);
}

    input, textarea, select {
        color: #ffffff !important;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] > div {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        color: #fff !important;
        border-radius: 16px !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        color: #fff !important;
        -webkit-text-fill-color: #fff !important;
    }

    div[data-baseweb="select"] span {
        color: #fff !important;
    }

    label, .stMarkdown, .stText, p, span {
        color: rgba(255,255,255,0.86);
    }

    .footer {
        color: rgba(255,255,255,0.42);
        text-align: center;
        padding: 28px 0 10px;
        font-size: 13px;
    }

    hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 24px 0;
    }
    </style>
    """.replace("__CAR_IMAGE__", car_img),
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
ARTIFACT_DIR = Path("artifacts")


def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


@st.cache_resource(show_spinner=False)
def load_artifacts():
    """Load model artifacts if available. Falls back to demo mode."""
    artifacts = {"available": False}
    try:
        # Flexible artifact names
        model_paths = [
            ARTIFACT_DIR / "model.pkl",
            ARTIFACT_DIR / "xgb_model.pkl",
            ARTIFACT_DIR / "xgb_price_model.joblib",
            ARTIFACT_DIR / "price_model.pkl",
        ]
        feature_paths = [
            ARTIFACT_DIR / "feature_cols.pkl",
            ARTIFACT_DIR / "feature_cols.joblib",
            ARTIFACT_DIR / "FEATURE_COLS.pkl",
            ARTIFACT_DIR / "features.pkl",
        ]

        model_path = next((p for p in model_paths if p.exists()), None)
        feature_path = next((p for p in feature_paths if p.exists()), None)

        if model_path and feature_path:
            artifacts["model"] = load_pickle(model_path)
            artifacts["feature_cols"] = load_pickle(feature_path)
            artifacts["available"] = True

        # Optional tfidf/vectorizer support
        for name in ["tfidf.pkl", "vectorizer.pkl", "tfidf_vectorizer.pkl"]:
            p = ARTIFACT_DIR / name
            if p.exists():
                artifacts["tfidf"] = load_pickle(p)
                break

    except Exception as exc:
        artifacts["error"] = str(exc)
        artifacts["available"] = False
    return artifacts


def normalize_text(text: str) -> str:
    return " ".join(str(text or "").lower().split())


HONEST_TERMS = [
    "clean title", "runs great", "runs good", "service records", "one owner",
    "new tires", "new brakes", "new battery", "cold ac", "well maintained",
    "minor dent", "small dent", "no accidents", "garage kept", "clean interior",
    "recently serviced", "oil changed", "timing belt", "water pump", "carfax"
]

SUSPICIOUS_TERMS = [
    "bad credit", "no credit", "guaranteed approval", "approved today",
    "down payment", "weekly payment", "monthly payment", "payments start",
    "zero down", "buy here pay here", "rent to own", "call now",
    "apply now", "everyone approved", "repo", "repos", "fixed income"
]


def trust_score_from_description(description: str):
    text = normalize_text(description)
    words = text.split()
    word_count = len(words)
    honest_hits = sum(term in text for term in HONEST_TERMS)
    suspicious_hits = sum(term in text for term in SUSPICIOUS_TERMS)
    caps_ratio = 0.0
    raw = str(description or "")
    letters = [c for c in raw if c.isalpha()]
    if letters:
        caps_ratio = sum(c.isupper() for c in letters) / len(letters)

    score = 72
    score += min(honest_hits * 5, 18)
    score -= min(suspicious_hits * 10, 36)

    if word_count < 20:
        score -= 12
    elif word_count > 80:
        score += 5

    if caps_ratio > 0.35:
        score -= 8

    score = int(max(0, min(100, score)))
    if score >= 78:
        label = "High Trust"
    elif score >= 55:
        label = "Moderate Trust"
    else:
        label = "Low Trust"
    return score, label, honest_hits, suspicious_hits


def demo_price_prediction(year, manufacturer, model_name, condition, fuel, odometer, title_status, transmission, car_type, state):
    """A deterministic demo estimator used if artifacts are missing."""
    base = 23000
    age = max(0, 2026 - int(year))
    base -= age * 850
    base -= (float(odometer) / 1000) * 48

    premium = {"bmw", "mercedes-benz", "audi", "lexus", "tesla", "porsche", "cadillac", "acura", "infiniti"}
    reliable = {"toyota", "honda", "subaru", "mazda"}
    trucks = {"truck", "pickup", "offroad"}

    if str(manufacturer).lower() in premium:
        base += 8500
    if str(manufacturer).lower() in reliable:
        base += 1800
    if str(car_type).lower() in trucks:
        base += 5500
    if str(car_type).lower() in {"suv", "wagon"}:
        base += 2500
    if str(fuel).lower() in {"diesel", "electric"}:
        base += 2500
    if str(transmission).lower() == "manual":
        base -= 600
    if str(title_status).lower() not in {"clean", "unknown"}:
        base -= 5000

    cond_adj = {
        "new": 5000, "like new": 3200, "excellent": 2200,
        "good": 600, "fair": -1800, "salvage": -6500, "unknown": 0
    }
    base += cond_adj.get(str(condition).lower(), 0)

    return max(500, int(base))


def predict_price_with_artifacts(artifacts, row):
    if not artifacts.get("available"):
        return None
    try:
        feature_cols = artifacts["feature_cols"]
        model = artifacts["model"]
        X = pd.DataFrame([row])
        for col in feature_cols:
            if col not in X.columns:
                X[col] = 0
        X = X[feature_cols]
        pred = model.predict(X)[0]
        # If trained on log1p target, many notebooks store log preds. Heuristic:
        if pred < 20:
            pred = np.expm1(pred)
        return int(max(0, pred))
    except Exception:
        return None


def fairness_score(listing_price, predicted_price, trust_score):
    if predicted_price <= 0:
        return 50, "Unknown"
    diff_pct = (listing_price - predicted_price) / predicted_price
    price_component = max(0, 100 - abs(diff_pct) * 140)
    score = int(round(price_component * 0.72 + trust_score * 0.28))
    if diff_pct <= -0.12:
        verdict = "Potential Deal"
    elif diff_pct >= 0.12:
        verdict = "Overpriced"
    else:
        verdict = "Fairly Priced"
    return max(0, min(100, score)), verdict


def money(x):
    return f"${x:,.0f}"

# ------------------------------------------------------------
# Data / defaults
# ------------------------------------------------------------
artifacts = load_artifacts()

BRAND_MODEL_MAP = {
    "toyota": ["camry", "corolla", "prius", "rav4", "highlander", "tacoma", "tundra", "4runner", "sienna", "avalon"],
    "honda": ["civic", "accord", "cr-v", "pilot", "odyssey", "fit", "ridgeline", "hr-v", "insight", "element"],
    "ford": ["f-150", "escape", "explorer", "fusion", "mustang", "focus", "edge", "expedition", "ranger", "taurus"],
    "chevrolet": ["silverado", "malibu", "impala", "camaro", "equinox", "tahoe", "suburban", "traverse", "cruze", "colorado"],
    "bmw": ["3 series", "5 series", "x3", "x5", "x1", "x6", "7 series", "m3", "m5", "z4"],
    "mercedes-benz": ["c-class", "e-class", "s-class", "glc", "gle", "gla", "gls", "cla", "sl", "sprinter"],
    "audi": ["a3", "a4", "a5", "a6", "a7", "q3", "q5", "q7", "q8", "tt"],
    "lexus": ["is", "es", "gs", "ls", "rx", "nx", "gx", "lx", "ct", "ux"],
    "tesla": ["model 3", "model s", "model x", "model y", "roadster"],
    "nissan": ["altima", "sentra", "maxima", "rogue", "pathfinder", "murano", "frontier", "titan", "versa", "370z"],
    "jeep": ["wrangler", "grand cherokee", "cherokee", "compass", "renegade", "gladiator", "patriot", "liberty"],
    "subaru": ["outback", "forester", "impreza", "legacy", "crosstrek", "wrx", "brz", "ascent"],
    "mazda": ["mazda3", "mazda6", "cx-3", "cx-5", "cx-9", "mx-5 miata", "rx-8"],
    "hyundai": ["elantra", "sonata", "tucson", "santa fe", "accent", "kona", "veloster", "palisade"],
    "kia": ["optima", "sorento", "sportage", "soul", "forte", "rio", "telluride", "sedona", "stinger"],
    "ram": ["1500", "2500", "3500", "promaster", "promaster city"],
    "gmc": ["sierra", "yukon", "terrain", "acadia", "canyon", "savana"],
    "dodge": ["charger", "challenger", "durango", "journey", "grand caravan", "dart", "ram 1500"],
    "volkswagen": ["jetta", "passat", "golf", "tiguan", "atlas", "beetle", "taos", "arteon"],
    "cadillac": ["escalade", "cts", "ats", "xt5", "xt4", "xt6", "srx", "ct5", "ct6"],
}
manufacturers = list(BRAND_MODEL_MAP.keys())
conditions = ["excellent", "good", "fair", "like new", "new", "salvage", "Unknown"]
fuels = ["gas", "diesel", "hybrid", "electric", "other", "Unknown"]
title_statuses = ["clean", "rebuilt", "salvage", "lien", "missing", "parts only", "Unknown"]
transmissions = ["automatic", "manual", "other", "Unknown"]
types = ["sedan", "SUV", "truck", "pickup", "coupe", "hatchback", "wagon", "van", "convertible", "mini-van", "other", "Unknown"]
states = ["ca", "tx", "fl", "ny", "oh", "wa", "az", "co", "ga", "mi", "pa", "nc", "or", "il", "Unknown"]

# ------------------------------------------------------------
# Sidebar inputs
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("### Vehicle Inputs")
    year = st.slider("Model Year", 2000, 2022, 2016)
    manufacturer = st.selectbox("Manufacturer", manufacturers, index=0)
    model_options = BRAND_MODEL_MAP.get(manufacturer, ["other"])
    model_name = st.selectbox("Model", model_options, index=0)
    odometer = st.number_input("Odometer / Mileage", min_value=11, max_value=300000, value=85000, step=1000)
    listing_price = st.number_input("Listing Price", min_value=500, max_value=80000, value=15900, step=500)

    st.markdown("---")
    condition = st.selectbox("Condition", conditions, index=1)
    fuel = st.selectbox("Fuel", fuels, index=0)
    title_status = st.selectbox("Title Status", title_statuses, index=0)
    transmission = st.selectbox("Transmission", transmissions, index=0)
    car_type = st.selectbox("Vehicle Type", types, index=0)
    state = st.selectbox("State", states, index=1)

    st.markdown("---")
    description = st.text_area(
        "Listing Description",
        value="Clean title, runs great, cold AC, recently serviced, new tires. Minor scratches only. Serious buyers can test drive.",
        height=170,
    )
    run = st.button("Analyze Listing")

# ------------------------------------------------------------
# Hero
# ------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Truvera AI - Used Car Intelligence</div>
        <h1>Know the real value before you buy.</h1>
        <p>Estimate fair market price, evaluate listing trust, and reveal whether a used car listing is a smart deal or an overpriced risk.</p>
        <div class="hero-actions">
            <div class="pill primary">Fair Price Engine</div>
            <div class="pill secondary">Trust Score NLP</div>
            <div class="pill secondary">Market Fairness</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.write("")

# ------------------------------------------------------------
# Prediction / Results only after button click
# ------------------------------------------------------------
if run:
    row = {
        "year": year,
        "manufacturer": manufacturer,
        "model": model_name,
        "condition": condition,
        "fuel": fuel,
        "odometer": odometer,
        "title_status": title_status,
        "transmission": transmission,
        "type": car_type,
        "state": state,
    }
    
    predicted = predict_price_with_artifacts(artifacts, row)
    if predicted is None:
        predicted = demo_price_prediction(year, manufacturer, model_name, condition, fuel, odometer, title_status, transmission, car_type, state)
        mode_text = "Demo estimator active"
    else:
        mode_text = "Model artifacts loaded"
    
    trust_score, trust_label, honest_hits, suspicious_hits = trust_score_from_description(description)
    fair_score, verdict = fairness_score(listing_price, predicted, trust_score)
    delta = listing_price - predicted
    delta_pct = (delta / predicted) * 100 if predicted else 0
    
    # ------------------------------------------------------------
    # Result cards
    # ------------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">Predicted Fair Price</div>
            <div class="value">{money(predicted)}</div>
            <div class="sub">{mode_text}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">Listing Price</div>
            <div class="value">{money(listing_price)}</div>
            <div class="sub">Difference: {money(delta)} - {delta_pct:+.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">Trust Score</div>
            <div class="value">{trust_score}/100</div>
            <div class="sub">{trust_label}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">Fairness Score</div>
            <div class="value">{fair_score}/100</div>
            <div class="sub">{verdict}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    left, right = st.columns([1.1, 0.9], gap="large")
    
    with left:
        st.markdown("""
        <div class="panel">
            <div class="section-title">Market Intelligence</div>
            <div class="section-subtitle">Truvera compares the listing price against the estimated fair value and blends it with description trust signals.</div>
        """, unsafe_allow_html=True)
    
        status_line = ""
        if verdict == "Potential Deal":
            status_line = "This listing appears below the estimated market value. Review trust score before assuming it is a bargain."
        elif verdict == "Overpriced":
            status_line = "This listing appears above the estimated market value. Negotiation may be needed."
        else:
            status_line = "This listing is close to the estimated fair market range."
    
        st.markdown(f"""
            <div class="verdict">{verdict}: {status_line}</div>
            <hr>
            <div class="tiny-note">
                Honest signals detected: <b>{honest_hits}</b><br>
                Suspicious signals detected: <b>{suspicious_hits}</b><br>
                Description length: <b>{len(str(description).split())}</b> words
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with right:
        st.markdown(f"""
        <div class="panel gauge-wrap">
            <div class="gauge" style="--score:{fair_score};">
                <div class="gauge-inner">
                    <div class="gauge-score">{fair_score}</div>
                    <div class="gauge-label">Fairness</div>
                </div>
            </div>
            <div class="verdict">{manufacturer.title()} {model_name.title()} - {year}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
else:
    st.markdown("""
    <div class="panel" style="text-align:center; padding:42px;">
        <div class="section-title">Ready for analysis</div>
        <div class="section-subtitle">Choose the vehicle details from the sidebar, write or paste the listing description, then click <b>Analyze Listing</b>.</div>
        <div class="verdict">Results will appear here after analysis.</div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("How Truvera thinks", expanded=False):
    st.markdown(
        """
        **Fair Price Engine** estimates market value using structured vehicle attributes such as year, mileage, manufacturer, model, fuel, transmission, type, title status, and state.  
        **Trust Score** analyzes the listing description for honest signals and suspicious sales language.  
        **Fairness Score** combines price deviation and trust score into a single buyer-friendly rating.
        """
    )

st.markdown("<div class='footer'>Truvera - AI-powered used car fairness and trust scoring platform</div>", unsafe_allow_html=True)



