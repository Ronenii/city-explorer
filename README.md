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
1. Classify users as tourists or locals based on activity span
2. Engineer per-user features (location diversity, visit frequency, temporal spread, etc.)
3. Train a **Random Forest** classifier using **scikit-learn**
4. Evaluate with accuracy, F1-score, and confusion matrix; analyze feature importances

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
