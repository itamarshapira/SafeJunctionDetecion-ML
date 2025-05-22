import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import joblib



import streamlit as st
from datetime import datetime

st.title("🚦 Smart Junction Detection")
st.write("Welcome! This is your intersection risk assistant.")
st.subheader("Driver Info")

# מין הנהג
sex = st.selectbox("Sex", options=["Male", "Female"])
sex_value = 0 if sex == "Male" else 1  # גבר = 0, אישה = 1

# גיל → קידוד לקבוצת גיל לפי df_for_model
age = st.number_input("Age", min_value=15, max_value=100, value=30)

def map_age_to_group(age):
    if 15 <= age <= 19:
        return 4
    elif 20 <= age <= 24:
        return 5
    elif 25 <= age <= 29:
        return 6
    elif 30 <= age <= 34:
        return 7
    elif 35 <= age <= 39:
        return 8
    elif 40 <= age <= 44:
        return 9
    elif 45 <= age <= 49:
        return 10
    elif 50 <= age <= 54:
        return 11
    elif 55 <= age <= 59:
        return 12
    elif 60 <= age <= 64:
        return 13
    elif 65 <= age <= 69:
        return 14
    elif 70 <= age <= 74:
        return 15
    elif 75 <= age <= 79:
        return 16
    elif 80 <= age <= 84:
        return 17
    else:
        return 18  # גיל 85+

age_group_value = map_age_to_group(age)

# שנת הוצאת רישיון + חישוב ותק
shnat_hozaa = st.number_input("Year of License Issuance", min_value=1950, max_value=datetime.now().year, step=1, value=2010)
veteran_driver_years = datetime.now().year - shnat_hozaa

# סוג רכב → מיפוי לפי קטגוריות
vehicle_type = st.selectbox("Vehicle Type", options=["Private", "Taxi", "Commercial/Truck", "Two-wheeler"])

vehicle_0 = 1 if vehicle_type in ["Private", "Taxi"] else 0
vehicle_1 = 1 if vehicle_type == "Two-wheeler" else 0
vehicle_2 = 1 if vehicle_type == "Commercial/Truck" else 0

# הצגת סיכום
st.write("### Current Input Summary")
st.write({
    "SEX": sex_value,
    "KVUZA_GIL": age_group_value,
    "veteran_driver_years": veteran_driver_years,
    "vehicle_0": vehicle_0,
    "vehicle_1": vehicle_1,
    "vehicle_2": vehicle_2
})

#*  DB STATIC:

st.subheader("Intersection Location")

# הזנת קואורדינטות
input_x = st.number_input("Enter X coordinate", format="%.6f")
input_y = st.number_input("Enter Y coordinate", format="%.6f")

# טעינת בסיס הנתונים הסטטי
@st.cache_data
def load_static_data():
    return pd.read_csv("../data_base/df_static.csv")

df_static = load_static_data()

# חישוב מרחק מכל נקודה בצומת
df_static["distance"] = np.sqrt((df_static["X"] - input_x)**2 + (df_static["Y"] - input_y)**2)

# מציאת הצומת הקרובה ביותר
nearest_row = df_static.sort_values("distance").iloc[0]

# הצגת המאפיינים הסטטיים
st.write("### Nearest Intersection Data")
st.write(nearest_row.drop("distance"))

#* DYMANIC:

now = datetime.now()

# שעה
hour = now.hour
hour_rad = 2 * np.pi * hour / 24
hour_sin = np.sin(hour_rad)
hour_cos = np.cos(hour_rad)

# חודש
month = now.month
month_rad = 2 * np.pi * month / 12
month_sin = np.sin(month_rad)
month_cos = np.cos(month_rad)

# יום בשבוע
weekday = now.weekday()  # 0=Monday ... 6=Sunday
weekday_rad = 2 * np.pi * weekday / 7
weekday_sin = np.sin(weekday_rad)
weekday_cos = np.cos(weekday_rad)

# תואם ללוח העברי – ראשון עד חמישי הם ימי חול
SUG_YOM_Weekday = 1 if weekday in [6, 0, 1, 2, 3] else 0 # API GOV for HOLIDY COUD INSERT


# לילה
is_night = 1 if hour < 6 or hour >= 20 else 0


#* COMBAIND

# ----- יצירת שורת DataFrame -----

# שלב 1: שילוב הדינמי + הסטטי
combined = nearest_row.drop(["X", "Y", "ZOMET_IRONI", "SEMEL_YISHUV", "pk_teuna_fikt", "distance"]).to_dict()

# שלב 2: הוספת משתנים דינמיים
combined.update({
    "KVUZA_GIL": age_group_value,
    "veteran_driver_years": veteran_driver_years,
    "SEX": sex_value,
    "vehicle_0": vehicle_0,
    "vehicle_1": vehicle_1,
    "vehicle_2": vehicle_2,
    "hour_sin": hour_sin,
    "hour_cos": hour_cos,
    "HODESH_TEUNA_sin": month_sin,
    "HODESH_TEUNA_cos": month_cos,
    "YOM_BASHAVUA_sin": weekday_sin,
    "YOM_BASHAVUA_cos": weekday_cos,
    "SUG_YOM_Weekday": SUG_YOM_Weekday,
    "is_night": is_night,
    "is_not_clear_weather": 0,  # נוכל להחליף בהמשך
    "is_slippery_road": 0       # נוכל לשאוב ממזג אוויר
})

# שלב 3: יצירת DataFrame עם שורה אחת
predict_df = pd.DataFrame([combined])

# ----- טעינת המודל וביצוע חיזוי -----
model = joblib.load("../model/rf_balanced.pkl")

# סדר את העמודות לפי הסדר שהמודל מצפה לו
correct_order = [
    'MEHIRUT_MUTERET', 'ROHAV', 'RAMZOR',
    'KVUZA_GIL', 'veteran_driver_years',
    'HODESH_TEUNA_sin', 'HODESH_TEUNA_cos',
    'SUG_YOM_Weekday', 'is_night',
    'YOM_BASHAVUA_sin', 'YOM_BASHAVUA_cos',
    '_MultiLaneOneWay', '_SingleLaneOneWay',
    '_TwoWay_Separated', '_TwoWay_Unseparated',
    'is_signage_problem', 'is_not_clear_weather',
    'is_slippery_road', 'SEX',
    'vehicle_0', 'vehicle_1', 'vehicle_2',
    'hour_sin', 'hour_cos'
]

# סדר את העמודות לפי הסדר
predict_df = predict_df[correct_order]
#print('sdfsdf',predict_df)

st.write("### 🔍 Full Input to Model")
st.dataframe(predict_df.T, use_container_width=True)


probability = model.predict_proba(predict_df)[0][1]
prediction = int(probability >= 0.39)

# ----- תצוגה -----
st.subheader("Prediction Result")
st.metric("Predicted Risk Probability", f"{probability:.2%}")
st.write("Risk Level:", "⚠️ High Risk" if prediction == 1 else "✅ Low Risk")
 
#* MAP:
# === המרה מ-ITM (רשת ישראל החדשה) ל-WGS84 (קו רוחב/קו אורך) ===
from pyproj import Transformer
import folium
from streamlit_folium import st_folium

# פונקציה שמבצעת המרה
def convert_itm_to_wgs84(x, y):
    """
    Converts Israeli TMGrid coordinates (ITM) to WGS84 (latitude, longitude).
    Uses EPSG codes: 2039 (ITM) → 4326 (WGS84).
    """
    transformer = Transformer.from_crs("EPSG:2039", "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lat, lon

# המרת הקואורדינטות של הצומת
lat, lon = convert_itm_to_wgs84(nearest_row["X"], nearest_row["Y"])

# Create a map centered on the detected intersection coordinates
m = folium.Map(location=[lat, lon], zoom_start=16)



# === TOP BANNER SECTION (STATIC + AUTO-DISMISS) ===

# Import Element from branca to insert custom HTML into the map
from branca.element import Element

# Define HTML and inline CSS for a top banner that appears above the map
# The banner will auto-hide after 3 seconds using JavaScript
banner_html = f"""
<div id="alert-banner" style="
    position: fixed;
    top: 0px;
    left: 50%;
    transform: translateX(-50%);
    background-color: {'#ff4d4d' if prediction == 1 else '#90ee90'};
    color: black;
    padding: 12px 30px;
    border-radius: 0 0 12px 12px;
    font-weight: bold;
    font-size: 18px;
    z-index: 9999;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    transition: opacity 1s ease-out;
">
    {'⚠️ Dangerous Intersection – Drive Carefully!' if prediction == 1 else '✅ Safe Intersection – Continue Driving'}
</div>

<script>
    // JavaScript to fade out the banner after 3 seconds
    setTimeout(function() {{
        var banner = document.getElementById('alert-banner');
        if (banner) {{
            banner.style.opacity = '0';
        }}
    }}, 3000);
</script>
"""

# Inject the banner HTML into the map's root element
m.get_root().html.add_child(Element(banner_html))

# === MAP MARKER SECTION ===

# Choose marker color and popup text based on prediction result
if prediction == 1:
    color = "red"
    icon_text = "⚠️ High Risk – Drive Carefully!"
else:
    color = "green"
    icon_text = "✅ Low Risk – Safe"

# Add a visible marker to the map to indicate the intersection location
# Includes popup message and color-coded icon
folium.Marker(
    [lat, lon],
    popup=icon_text,
    icon=folium.Icon(color=color, icon="info-sign")
).add_to(m)


# הצגת המפה ב-Streamlit
st.write("### 🗺️ Intersection Location on Map")
st_folium(m, width=700, height=500)
