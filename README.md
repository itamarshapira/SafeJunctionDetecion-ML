# 🚦 Smart Junction Risk Detection

**Final Year Project – Sapir College (2025)**  
A full machine learning pipeline combined with an interactive web app for detecting dangerous intersections based on driver context, environment, and historical data.

---

## 🧭 Project Overview

Urban intersections are critical points where accidents frequently occur.  
Our goal was to build a machine learning model that can **predict whether a given intersection is high-risk**, for a specific driver and context (time, weather, road conditions).

This project was supervised by **Dr. Amir Kolman** and followed a structured end-to-end ML methodology.

---

## 1️⃣ Problem Definition

The original datasets did not include any explicit “risk” labels.  
We defined a risk score per intersection based on accident severity, to allow supervised learning. This involved:

- Aggregating accident records by intersection
- Creating a **Base Risk Score** using HALMAS-inspired weights:
  > `6 × Fatal + 3 × Severe + 1 × Light`
- Normalizing these scores and converting them into binary labels: `High Risk` vs `Low Risk`

---

## 2️⃣ Data Collection & Preparation

We combined multiple CSVs of 2023 accident records from the **Israeli Central Bureau of Statistics** and **Israeli Police**.  
After merging on `pk_teuna_fikt`, we retained only official police-verified rows (i.e. not survey data).

- Final dataset contained **over 40,000 rows** and **60+ features**
- We filtered only intersections with valid GPS (X/Y) and sufficient accident history
- Handled missing values by dropping noisy or empty columns

---

## 3️⃣ Feature Engineering

We engineered features from 3 domains:

**A. Time**

- `hour`, `weekday`, `month` were transformed into **cyclical features** using sin/cos encoding to preserve distance (e.g. 23 ↔ 0)

**B. Driver Context**

- Age grouped into HALMAS categories (15–85+)
- Experience calculated from license year
- Vehicle type encoded into 3 binary columns (private, commercial, two-wheeler)

**C. Road & Environment**

- Binary flags: road lighting, signage problems, weather clarity, slippery conditions
- One-hot encoded road structure types

> ✅ Engineering handled many challenges like non-numeric data, inconsistent columns, and missing values.

---

## 4️⃣ Modeling & Training

We trained multiple models, ultimately selecting:

- `RandomForestClassifier` from scikit-learn
- Target: binary risk classification (high vs low)

> We manually tuned the classification threshold to `0.39` for better **recall on high-risk** cases  
> (a standard 0.5 threshold underperformed due to class imbalance)

We validated results using:

- Accuracy and F1-score
- Confusion matrix
- ROC AUC and threshold tuning curves
- Manual real-world scenarios (X/Y samples)

---

## 5️⃣ App Deployment

We deployed the model inside a real-time web app built with **Streamlit**, where users can:

1. Input driver details
2. Enter intersection coordinates
3. Automatically get context (time, weekday, hour)
4. View prediction and **live map**

> The app uses `folium` to render a dynamic map with markers:  
> ✅ Green = Safe  ⚠️ Red = Dangerous

Coordinates are converted from **ITM** to **WGS84** for map display using `pyproj`.

---

## 🧱 Tech Summary

| Layer             | Tools                      |
| ----------------- | -------------------------- |
| ML Modeling       | scikit-learn               |
| Data Wrangling    | pandas, numpy              |
| UI + Map          | Streamlit + folium         |
| Coordinate System | pyproj (ITM → WGS84)       |
| Dataset Size      | 40,000+ rows, 60+ features |

---

## 🛣️ Future Plans

- [ ] Full-stack React + Flask integration
- [ ] Google Maps route + risk overlay
- [ ] Real-time driver GPS + voice alerts
- [ ] Weather API integration
- [ ] Save prediction history per user

---
