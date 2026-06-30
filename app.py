import pandas as pd
import streamlit as st
import pydeck as pdk

st.set_page_config(page_title="City Explorer — Tel Aviv Flickr", layout="wide")
st.title("City Explorer — Tel Aviv Flickr Dataset")

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("flickr_clean.csv")
    df["date"] = pd.to_datetime(df[["year", "month", "day"]])
    # Classify tourist vs local per user
    span = df.groupby("uid")["date"].agg(lambda x: (x.max() - x.min()).days)
    df["user_type"] = df["uid"].map(lambda u: "local" if span[u] >= 365 else "tourist")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("flickr_clean.csv not found — run the 01_data_cleaning notebook first.")
    st.stop()

# ── Sidebar filters ────────────────────────────────────────────────────────────
st.sidebar.header("Filters")

user_types = st.sidebar.multiselect(
    "User type", ["tourist", "local"], default=["tourist", "local"]
)

year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider("Year range", year_min, year_max, (year_min, year_max))

df_filtered = df[
    df["user_type"].isin(user_types) &
    df["year"].between(year_range[0], year_range[1])
]

# ── KPIs ───────────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Photos", f"{len(df_filtered):,}")
col2.metric("Unique users", f"{df_filtered['uid'].nunique():,}")
col3.metric("Tourists", f"{(df_filtered['user_type'] == 'tourist').sum():,}")
col4.metric("Locals", f"{(df_filtered['user_type'] == 'local').sum():,}")

# ── Map ────────────────────────────────────────────────────────────────────────
st.subheader("Photo locations")

COLOR_MAP = {"tourist": [255, 100, 50, 160], "local": [50, 150, 255, 160]}
df_filtered = df_filtered.copy()
df_filtered["color"] = df_filtered["user_type"].map(COLOR_MAP)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtered[["lon", "lat", "color", "uid", "user_type", "year"]],
    get_position=["lon", "lat"],
    get_fill_color="color",
    get_radius=40,
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=df_filtered["lat"].mean(),
    longitude=df_filtered["lon"].mean(),
    zoom=12,
    pitch=0,
)

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "uid: {uid}\ntype: {user_type}\nyear: {year}"},
    )
)

# ── Photos per year ────────────────────────────────────────────────────────────
st.subheader("Photos per year")
yearly = df_filtered.groupby(["year", "user_type"]).size().unstack(fill_value=0)
st.bar_chart(yearly)

# ── Raw table ──────────────────────────────────────────────────────────────────
with st.expander("Show raw data"):
    st.dataframe(df_filtered.drop(columns=["color", "date"]).reset_index(drop=True))
