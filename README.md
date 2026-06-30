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
2. Learn and compare behavioral patterns between the two groups

### Part 2 — Unsupervised Learning & Agent-Based Simulation
1. **Synthetic Agents:** Add simulative agents to the city grid with defined parameters:
   - Quantity, starting point, walking rules, and environment rules
2. **POI Discovery:** Apply unsupervised clustering to identify Points of Interest where agents congregate
   - **K-Means** clustering
   - **DBSCAN** clustering
3. **Parameter Tuning:** Vary algorithm parameters and examine how results differ; analyze emergent agent behavior
4. **Validation:** Compare synthetic agent movements against real (Flickr) agent movements — is there a meaningful relationship?

## Key Assumptions

- **User Classification:** Activity span < 1 year → tourist; ≥ 1 year → local
- **Time Normalization:** All agents move within the simulation during the span of a single day
- **Spatial Model:** Users move around a city grid
