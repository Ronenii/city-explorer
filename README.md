# city-explorer

## Assignment Overview

**Final Project: Examining Urban Behavior via Agent-Based Modeling using Machine Learning Methods**

This project analyzes human movement and behavior in urban environments using a Flickr photo dataset of Tel Aviv.

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

## Methodology

1. **Agent-Based Modeling (ABM):** Create synthetic agents representing tourists and locals
2. **Environment Rules:** Define rules governing the city grid environment
3. **Agent Rules:** Define behavioral rules for each agent type based on observed data patterns

## Key Assumptions

- **User Classification:** Activity span < 1 year → tourist; ≥ 1 year → local
- **Time Normalization:** All agents move within the simulation during the span of a single day
- **Spatial Model:** Users move around a city grid
