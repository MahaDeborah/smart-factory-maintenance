
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart FactoryMaintenance",
    page_icon ="logo.png",
    layout="wide"
)
st.markdown("""
<style>
    .stApp {
        background-color: #071B3A;
        color: #FFFFFF;
    }

    h1 {
        color: #FF65AD;
    }
        [data-testid="stMetricLabel"] {
        color: #FF65AD;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)
logo_column, title_column = st.columns([1, 5])
with logo_column:
    st.image("logo.png", width=120)
with title_column:
    st.title("Smart Factory Maintenance")
    st.write("Cooling Pump Monitoring — UTL-002")

readings= pd.read_csv("pump_readings.csv") 
latest_reading = readings.iloc[-1]

st.metric(
    label="Water Flow",
    value=f"{latest_reading['Water Flow (L/min)']} L/min"
)