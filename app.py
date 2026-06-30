import joblib
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

st.set_page_config(page_title="City Explorer — Tel Aviv Flickr", layout="wide")
st.title("City Explorer — Tel Aviv Flickr Dataset")

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    photos = pd.read_csv("flickr_clean.csv")
    preds  = pd.read_csv("predictions.csv")   # uid, label, predicted, prob_local
    feats  = pd.read_csv("features.csv")
    photos = photos.merge(preds[["uid", "label", "predicted", "prob_local"]], on="uid", how="inner")
    return photos, preds, feats

@st.cache_resource
def load_model():
    return joblib.load("model.joblib")

try:
    photos, preds, feats = load_data()
    model = load_model()
except FileNotFoundError as e:
    st.error(f"Missing file: {e} — run city_explorer.ipynb first.")
    st.stop()

FEATURE_COLS = [c for c in feats.columns if c not in ["uid", "label"]]
importances  = pd.Series(model.feature_importances_, index=FEATURE_COLS).sort_values()

# ── Sidebar filters ────────────────────────────────────────────────────────────
st.sidebar.header("About")
st.sidebar.markdown("""
**City Explorer** analyzes geotagged Flickr photos from Tel Aviv to classify users as
**tourists** (activity span < 1 year) or **locals** (≥ 1 year) using a Random Forest classifier.

---
**Process**
1. Clean raw Flickr CSV → `flickr_clean.csv`
2. Engineer 14 behavioral/spatial features per user (≥ 5 photos)
3. Train RF on 80/20 stratified split (`class_weight="balanced"`)
4. Persist model + predictions → `model.joblib`, `predictions.csv`

---
**Feature families**

🔢 **Volume** — n_photos, n_active_days, photos_per_active_day

📍 **Spatial** — n_distinct_cells, radius_of_gyration, bbox_area, bbox_diag, std_lon, std_lat

🔁 **Revisit** — mean_photos_per_cell, location_entropy

🕐 **Temporal** — weekend_ratio, hour_std, n_distinct_months

---
**Important notes**
- Activity span is the **label definition only** — it is never a feature (no leakage)
- Only users with ≥ 5 photos are classified (988 of 2 152 total users)
- Class imbalance (~64 % tourist / 36 % local) is handled via `class_weight="balanced"`
""")

st.sidebar.divider()
st.sidebar.header("Filters")

group_opts = st.sidebar.multiselect(
    "Predicted group", ["Tourist", "Local"], default=["Tourist", "Local"]
)
label_map      = {"Tourist": 0, "Local": 1}
selected_labels = [label_map[g] for g in group_opts]

year_min, year_max = int(photos["year"].min()), int(photos["year"].max())
year_range = st.sidebar.slider("Year range", year_min, year_max, (year_min, year_max))

filtered = photos[
    photos["predicted"].isin(selected_labels) &
    photos["year"].between(year_range[0], year_range[1])
].copy()
filtered["color"]       = filtered["predicted"].map({0: [255, 165, 0, 160], 1: [91, 33, 130, 160]})
filtered["group"]       = filtered["predicted"].map({0: "Tourist", 1: "Local"})
filtered["group_label"] = filtered["group"]

# ── Dataset Overview ───────────────────────────────────────────────────────────
st.subheader("Dataset Overview")
d1, d2, d3, d4, d5 = st.columns(5)
d1.metric("Total photos",    f"{len(photos):,}")
d2.metric("Classified users", f"{preds['uid'].nunique():,}")
d3.metric("Tourists (true)", f"{(preds['label'] == 0).sum():,}")
d4.metric("Locals (true)",   f"{(preds['label'] == 1).sum():,}")
d5.metric("Date range",      f"{photos['year'].min()}–{photos['year'].max()}")

# ── KPIs (filtered) ────────────────────────────────────────────────────────────
st.subheader("Current selection")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Photos",               f"{len(filtered):,}")
c2.metric("Unique users",         f"{filtered['uid'].nunique():,}")
c3.metric("Tourists (predicted)", f"{(filtered['predicted'] == 0).sum():,}")
c4.metric("Locals (predicted)",   f"{(filtered['predicted'] == 1).sum():,}")

# ── Map ────────────────────────────────────────────────────────────────────────
st.subheader("Photo locations — predicted group")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered[["lon", "lat", "color", "uid", "group", "year"]],
    get_position=["lon", "lat"],
    get_fill_color="color",
    get_radius=40,
    pickable=True,
)
view_state = pdk.ViewState(
    latitude=filtered["lat"].mean()  if len(filtered) else 32.08,
    longitude=filtered["lon"].mean() if len(filtered) else 34.78,
    zoom=12,
    pitch=0,
)
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "uid: {uid}\ngroup: {group}\nyear: {year}"},
))

# ── Model Performance ──────────────────────────────────────────────────────────
st.subheader("Model Performance")

y_true = preds["label"].values
y_pred = preds["predicted"].values
report = classification_report(y_true, y_pred, target_names=["Tourist", "Local"], output_dict=True)

m1, m2, m3 = st.columns(3)
m1.metric("Accuracy",   f"{report['accuracy']:.1%}")
m2.metric("Tourist F1", f"{report['Tourist']['f1-score']:.3f}")
m3.metric("Local F1",   f"{report['Local']['f1-score']:.3f}")

col_cm, col_fi = st.columns(2)

with col_cm:
    fig, ax = plt.subplots(figsize=(4, 3.5))
    ConfusionMatrixDisplay(
        confusion_matrix(y_true, y_pred),
        display_labels=["Tourist", "Local"],
    ).plot(ax=ax, colorbar=False, cmap="Purples")
    ax.set_title("Confusion Matrix")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col_fi:
    fig, ax = plt.subplots(figsize=(5, 3.5))
    importances.plot(kind="barh", ax=ax, color="#5b2182")
    ax.axvline(1 / len(FEATURE_COLS), color="gray", linestyle="--", lw=1, label="uniform baseline")
    ax.set(title="Feature Importances", xlabel="Mean decrease in impurity")
    ax.legend(fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ── Photos per year ────────────────────────────────────────────────────────────
st.subheader("Photos per year")
yearly = filtered.groupby(["year", "group_label"]).size().unstack(fill_value=0)
st.bar_chart(yearly)

# ── Research Findings ──────────────────────────────────────────────────────────
st.subheader("Research Findings")

FINDINGS = [
    (
        "Q1 — What are the more popular regions?",
        "Activity concentrates along the **beachfront** and **city centre** (Dizengoff, Old Jaffa). "
        "The coastal strip and central boulevard consistently attract the highest photo density across all years.",
    ),
    (
        "Q2 — Are popular regions different for tourists vs locals?",
        "**Tourists** cluster tightly on the coast and landmark sites (beach promenade, Old Jaffa port, Dizengoff Square). "
        "**Locals** spread further inland across residential neighborhoods, revealing areas that tourists rarely reach. "
        "The spatial separation is visible on the map — filter by group to compare.",
    ),
    (
        "Q3 — What are the similarities/differences within each group?",
        "Locals have a **~58% larger median radius of gyration** (0.0183° vs 0.0116°) and visit "
        "**twice as many distinct 1 km grid cells** (median 8 vs 4). "
        "Tourists are spatially homogeneous — their movements converge on the same hotspots. "
        "Within each group, high-activity users exhibit the greatest spatial spread.",
    ),
    (
        "Q4 — What are the behavioral differences between groups?",
        "The strongest contrasts are **n_active_days** (median 12 for locals vs 3 for tourists), "
        "**n_distinct_cells**, and **radius_of_gyration** — all captured in the top features by importance. "
        "Weekend photo ratio is similar across both groups (~0.20–0.25), showing that day-of-week "
        "is not a meaningful differentiator. Volume and spatial range are the dominant signals.",
    ),
]
for title, text in FINDINGS:
    with st.expander(title, expanded=True):
        st.markdown(text)

# ── Feature Comparison ─────────────────────────────────────────────────────────
st.subheader("Tourist vs Local — Feature Comparison")

tourist_feats = feats[feats["label"] == 0][FEATURE_COLS]
local_feats   = feats[feats["label"] == 1][FEATURE_COLS]

comparison = pd.DataFrame({
    "Tourist (median)": tourist_feats.median().round(4),
    "Local (median)":   local_feats.median().round(4),
})
comparison["Local / Tourist ratio"] = (
    comparison["Local (median)"] / comparison["Tourist (median)"].replace(0, float("nan"))
).round(2)
st.dataframe(comparison, use_container_width=True)

# Box plots: top 6 features by importance
top_features = importances.nlargest(6).index.tolist()
fig, axes = plt.subplots(2, 3, figsize=(12, 6))
for ax, feat in zip(axes.flat, top_features):
    data_t = feats[feats["label"] == 0][feat].dropna()
    data_l = feats[feats["label"] == 1][feat].dropna()
    bp = ax.boxplot(
        [data_t, data_l],
        tick_labels=["Tourist", "Local"],
        patch_artist=True,
        notch=False,
        showfliers=False,
    )
    bp["boxes"][0].set_facecolor("darkorange"); bp["boxes"][0].set_alpha(0.7)
    bp["boxes"][1].set_facecolor("#5b2182");    bp["boxes"][1].set_alpha(0.7)
    for med in bp["medians"]:
        med.set_color("black"); med.set_linewidth(2)
    ax.set_title(feat, fontsize=9)
    ax.tick_params(axis="x", labelsize=8)
plt.suptitle("Feature distributions: Tourist vs Local (top 6 by importance, outliers hidden)", fontsize=10)
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ── Raw data ───────────────────────────────────────────────────────────────────
with st.expander("Show raw data"):
    st.dataframe(
        filtered.drop(columns=["color", "group", "group_label"], errors="ignore")
        .reset_index(drop=True)
    )
