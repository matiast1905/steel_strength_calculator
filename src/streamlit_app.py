import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Steel Strength Calculator")

st.markdown(
    """
This app allows you to estimate the **Tensile Strength** and **Yield Strength** using the components of the steel as predictors.  
To predict these values It's using a XGBoost machine learning model.  
This app is only for low carbon steels, that's why the allowed range of carbon is bounded to low levels.
"""
)

model = joblib.load("models/xgb_model.joblib")

st.sidebar.header("User Input Features")
carbon = st.sidebar.select_slider("Carbon content (in %)", options=np.arange(0.07, 0.365, 0.005).round(3), value=0.22)
silicon = st.sidebar.select_slider("Silicon content (in %)", options=np.arange(0.10, 0.56, 0.005).round(3), value=0.28)
manganese = st.sidebar.select_slider(
    "Manganese content (in %)", options=np.arange(0.4, 1.51, 0.005).round(3), value=0.95
)
phosphorus = st.sidebar.select_slider(
    "Phosphorus content (in %)", options=np.arange(0.00, 0.031, 0.001).round(3), value=0.015
)
sulphur = st.sidebar.select_slider(
    "Sulphur content (in %)", options=np.arange(0.00, 0.023, 0.001).round(3), value=0.012
)
nickel = st.sidebar.select_slider("Nickel content (in %)", options=np.arange(0.0, 0.65, 0.005).round(3), value=0.3)
chromium = st.sidebar.select_slider("Chromium content (in %)", options=np.arange(0.0, 1.35, 0.005).round(3), value=0.65)
molybdenum = st.sidebar.select_slider(
    "Molybdenum content (in %)", options=np.arange(0.0, 1.4, 0.005).round(3), value=0.7
)
cooper = st.sidebar.select_slider("Cooper content (in %)", options=np.arange(0.0, 0.255, 0.005).round(3), value=0.12)
vanadium = st.sidebar.select_slider(
    "Vanadium content (in %)", options=np.arange(0.0, 0.305, 0.005).round(3), value=0.15
)
aluminum = st.sidebar.select_slider(
    "Aluminum content (in %)", options=np.arange(0.000, 0.051, 0.001).round(3), value=0.025
)
nitrogen = st.sidebar.select_slider(
    "Nitrogen content (in %)", options=np.arange(0.000, 0.0151, 0.0001).round(4), value=0.007
)
niobium_tantalum = st.sidebar.select_slider(
    "Niobium + Tantalum content (in %)", options=np.arange(0.000, 0.002, 0.0005).round(4), value=0.001
)

predictors_df = pd.DataFrame(
    {
        "carbon": carbon,
        "silicon": silicon,
        "manganese": manganese,
        "phosphorus": phosphorus,
        "sulphur": sulphur,
        "nickel": nickel,
        "chromium": chromium,
        "molybdenum": molybdenum,
        "cooper": cooper,
        "vanadium": vanadium,
        "aluminum": aluminum,
        "nitrogen": nitrogen,
        "niobium_tantalum": niobium_tantalum,
    },
    index=[0],
)

temperature_df = pd.DataFrame({"temperature_c": np.arange(20, 665, 20)})

merged_df = pd.merge(predictors_df, temperature_df, how="cross")

prediction_df = pd.DataFrame(model.predict(merged_df), columns=["Yield Strength (MPa)", "Tensile Strength (MPa)"])

final_df = pd.concat([merged_df[["temperature_c"]], prediction_df], axis=1).melt(id_vars="temperature_c")

fig = px.line(
    final_df,
    x="temperature_c",
    y="value",
    color="variable",
    labels={"variable": "Property", "temperature_c": "Temperature [°C]", "value": "Strength [MPa]"},
)
fig.update_layout(yaxis_range=[0, 800])

st.plotly_chart(fig, use_container_width=True)
