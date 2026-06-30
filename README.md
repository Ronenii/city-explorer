# city-explorer

## Assignment Overview

**Final Project: Examining Urban Behavior via Agent-Based Modeling using Machine Learning Methods**

This project analyzes human movement and behavior in urban environments using a Flickr photo dataset of Tel Aviv.

**Part 1** focuses on **supervised machine learning** — classifying users as tourists or locals and learning behavioral patterns from labeled data.

## Dataset

- **Source:** Flickr user images geotagged in Tel Aviv
- **File:** `flickr_output_TelAviv100.xlsx - flickr_output_100.csv`

## User Classification

Users are classified based on their photo activity span:

- **Tourist:** A user who took photos over a span of **less than one year**
- **Local:** A user who took photos over a span of **one year or more**

## Research Goals

- Study and compare the spatial behavior of tourists vs. locals
- Analyze movement patterns relative to Points of Interest (POIs) across the city
- Build synthetic agents to simulate and model urban movement behavior

**Part 2** focuses on **unsupervised machine learning** — simulating synthetic agents on the city grid and discovering POIs through clustering.

## Methodology

### Part 1 — Supervised Learning
1. **Data cleaning** — drop nulls, validate dates/coordinates, land-check against Natural Earth polygons, remove duplicates; output `flickr_clean.csv`
2. **EDA** — photos per year, spatial scatter, users-by-photo-count distribution, tourist/local label balance
3. **Labeling** — activity span < 365 days → tourist (0); ≥ 365 days → local (1); label derived inside feature engineering to avoid a separate aggregation pass
4. **Feature engineering** — 14 per-user behavioral/spatial features with no label leakage (span is never a feature); families: Volume, Spatial, Revisit, Temporal rhythm; output `features.csv`
5. **Model training** — 80/20 stratified split, `RandomForestClassifier(n_estimators=200, class_weight="balanced")`

#### Feature Definitions (Step 4)

Features are grouped into four families. No span-derived columns are included (no leakage).

**Volume** — how much the user photographs

| Feature | Description |
|---|---|
| `n_photos` | Total photos taken |
| `n_active_days` | Distinct calendar days with at least one photo |
| `photos_per_active_day` | Average photos per active day (`n_photos / n_active_days`) |

**Spatial** — where the user photographs

| Feature | Description |
|---|---|
| `std_lon` | Standard deviation of photo longitudes (east-west spread) |
| `std_lat` | Standard deviation of photo latitudes (north-south spread) |
| `n_distinct_cells` | Distinct ~1 km grid cells visited (`round(lon,2)_round(lat,2)`) |
| `bbox_area` | Area of the bounding box around all photo locations (degrees²) |
| `bbox_diag` | Diagonal of the bounding box (degrees) |
| `radius_of_gyration` | RMS distance from the user's centroid: `√mean((lon−lon̄)²+(lat−lat̄)²)` |

**Revisit** — how the user concentrates or distributes effort across locations

| Feature | Description |
|---|---|
| `mean_photos_per_cell` | Average photos per distinct cell (revisit intensity) |
| `location_entropy` | Shannon entropy of cell visit frequencies — high = uniform spread, low = concentrated at few spots |

**Temporal rhythm** — when the user photographs

| Feature | Description |
|---|---|
| `weekend_ratio` | Fraction of photos taken on Saturday or Sunday |
| `hour_std` | Standard deviation of hour-of-day across all photos (spread of shooting times) |
| `n_distinct_months` | Distinct calendar months with at least one photo (breadth of visit period) |
6. **Evaluation** — classification report, confusion matrix, 5-fold CV F1, feature importances
7. **Analysis** — four research questions answered with plots (see below)
8. **Persist artifacts** — `model.joblib` + `predictions.csv` for use in the dashboard

#### Research Questions (Step 6.5)

| # | Question | Key finding |
|---|---|---|
| 1 | What are the more popular regions? | Activity concentrates along the beachfront and city centre (Dizengoff, Old Jaffa) |
| 2 | Are popular regions different for tourists vs locals? | Tourists cluster tightly on the coast and landmarks; locals spread inland across residential areas |
| 3 | What are the similarities/differences within each group? | Locals have a ~58% larger median radius of gyration (0.0183° vs 0.0116°) and visit twice as many distinct grid cells (8 vs 4); tourists are more spatially homogeneous |
| 4 | What are the behavioral differences between groups? | Strongest contrasts: `n_active_days` (12 vs 3), `n_distinct_cells`, `radius_of_gyration`; weekend ratio is similar (~0.20–0.25) |

### Part 2 — Unsupervised Learning & Agent-Based Simulation
1. **Synthetic Agents:** Implement agent-based simulation using **Mesa**
   - Parameters: agent quantity, starting position, walking rules, environment rules
   - Each agent represents a tourist or local moving on the city grid
2. **POI Discovery:** Apply unsupervised clustering via **scikit-learn** to identify Points of Interest where agents congregate
   - **K-Means** clustering
   - **DBSCAN** clustering
3. **Parameter Tuning:** Vary algorithm parameters and examine how results differ; analyze emergent agent behavior
4. **Validation:** Compare synthetic agent movements against real (Flickr) agent movements — is there a meaningful relationship?

## Tools & Libraries

| Category | Libraries |
|---|---|
| Data handling | `pandas`, `numpy` |
| Geospatial | `geopandas`, `shapely`, `pyproj`, `fiona`, `geodatasets` |
| Machine Learning | `scikit-learn` (Random Forest, KMeans, DBSCAN) |
| Agent-Based Modeling | `mesa` |
| Visualization | `matplotlib`, `seaborn`, `pydeck` |
| Dashboard | `streamlit` |
| Notebooks | `jupyterlab` |
| File I/O | `openpyxl` |

## Key Assumptions

- **User Classification:** Activity span < 1 year → tourist; ≥ 1 year → local
- **Time Normalization:** All agents move within the simulation during the span of a single day
- **Spatial Model:** Users move around a city grid
