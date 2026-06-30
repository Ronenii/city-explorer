# Implementation Plan

Live tracker for the city-explorer project. Work proceeds in **reviewable batches** —
each item is implemented, briefed, and committed only after review.

## Part 1 — Supervised Learning (Tourist vs Local Classifier)

Classify Flickr users as tourists or locals and learn what behavioral/spatial signature
distinguishes them. Label is defined by activity span (<1 year = tourist), so the model
is trained on **behavioral/spatial features only** — no span-derived features (avoids leakage).

**Locked decisions:**
- Features: behavioral/spatial only (no activity span, no first/last dates)
- User filter: ≥5 photos (~1025 users: 668 tourist / 357 local)
- Model: `RandomForestClassifier`, `class_weight="balanced"` (~65/35 imbalance)
- The **entire project (Part 1 + Part 2)** lives in one notebook: `city_explorer.ipynb`

**Steps:**
- [x] 0. Save this plan + set up env (install `requirements.txt` into `.venv`, verify imports)
- [x] 1. Cleaning section — single documented cell; output `flickr_clean.csv`
- [x] 2. EDA — photos over time, spatial scatter, photos-per-user dist, label balance
- [x] 3. Labeling — per-user span → label; filter ≥5 photos; per-user label table
- [x] 4. Feature engineering (no leakage) — volume, spatial, revisit, temporal features
- [x] 5. Model training — stratified split, `RandomForestClassifier(class_weight="balanced")`
- [x] 6. Evaluation — accuracy, P/R/F1, confusion matrix, CV, feature importances
- [x] 6.5 Analysis — answer the 4 research questions with plots in the notebook
- [x] 7. Persist artifacts — save model (joblib) + per-user feature/label table (CSV)
- [x] 8. Streamlit Part 1 results — display model metrics, confusion matrix,
       feature importances, and per-user predicted tourist/local on the map
       (extends `app.py`, reads the saved model + feature table from step 7)

## Part 2 — Unsupervised Learning & Agent-Based Simulation

_To be planned after Part 1 is complete._
