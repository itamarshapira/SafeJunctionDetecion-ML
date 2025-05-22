# 🚦 Smart Junction Risk Detection

**Machine Learning meets Real-Time Safety Alerts**  
A final-year project that combines data science, machine learning, and geospatial data to detect dangerous intersections for drivers based on personal, temporal, and environmental conditions.

---

## 📊 Project Summary

This project is structured in four parts:

1. **A. ML Pipeline** – From raw accident records to risk prediction
2. **B. Insights & Visual Analysis** – Data exploration and interpretability
3. **C. Model Reuse** – Save & reuse the trained model in production
4. **D. App** – Real-time prediction with interactive map

---

## 🧠 Problem Definition

Urban intersections are prone to high accident rates.  
Our goal is to predict how dangerous a specific intersection is **for a specific driver**, based on accident history and contextual factors such as:

- Time and day
- Weather
- Driver demographics
- Road characteristics

---

## 🎯 Risk Score Definition

Since the raw dataset does not contain a 'danger' label, we created a custom score:

### ✅ `Base_Risk_Score`

Inspired by CBS methodology:

> Weighted sum of accident types:
>
> ```
> 6 × fatal + 3 × severe + 1 × light
> ```

This creates a continuous risk score that we later **normalized** and converted into:

- Regression target
- Or binary class (high-risk vs. not)

---

## 🔄 ML Workflow (6 Steps)

1. **Import & Merge** accident datasets
2. **Clean + Normalize** features
3. **Aggregate** at intersection level
4. **Feature Engineering** – encode time, road, and driver inputs
5. **Modeling** – trained `RandomForestClassifier`
6. **Evaluation** – accuracy, ROC, and manual examples

Threshold tuned to `0.39` for improved F1 on high-risk class.

---

## 🖥️ App: Streamlit Interface

Our Streamlit app receives real-time user input and performs:

- Age, gender, license year → converts to ML features
- User inputs X/Y → closest intersection loaded
- Dynamic features (hour, weekday, month, night)
- Predicts if junction is dangerous
- Displays map and details

---

### 🗺️ Map View

- Uses `folium` and `streamlit-folium`
- Converts ITM coordinates to GPS (WGS84)
- Interactive marker with popup ("Safe" or "Dangerous")

---

## 🧱 Tech Stack

| Component           | Tool                        |
| ------------------- | --------------------------- |
| UI                  | Streamlit                   |
| ML Model            | Scikit-learn (RandomForest) |
| Coordinates         | pyproj                      |
| Map Rendering       | Folium                      |
| Geodata             | df_static.csv               |
| Deployment (Future) | React + Flask               |

---

## 🌐 Planned Features

- [ ] Real-time GPS location instead of manual X/Y
- [ ] Weather integration (OpenWeather API)
- [ ] Route safety alerts during trip (Google Directions API)
- [ ] User login & usage history
- [ ] Upgrade to full stack (React + FastAPI)

---

## 📁 Project Structure

```
final_project/
├── smart_junction_app/
│   └── app.py                # Streamlit app
├── data_base/
│   └── df_static.csv         # Processed intersection data
├── model/
│   └── rf_balanced.pkl       # Trained model
├── SafeJunctionDetection.ipynb  # Notebook with full pipeline
├── README.md
```

---

## 👥 Authors

- Itamar Shapira & Ofir Rodity
- Sapir College – B.Sc Computer Science
- Final Year Project – 2025
