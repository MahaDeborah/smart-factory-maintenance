from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


# Find files beside dashboard.py.
BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "logo.png"
READINGS_PATH = BASE_DIR / "pump_readings.csv"
HISTORY_PATH = BASE_DIR / "incident_history.csv"


st.set_page_config(
    page_title="Smart Factory Maintenance",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "⚙️",
    layout="wide",
)


# Dashboard colours and sensor cards.
st.markdown("""
<style>
    .stApp {
        background-color: #0B1220;
        color: #F1F5F9;
    }

    h1, h2, h3 {
        color: #F1F5F9;
    }

    [data-testid="stMetricLabel"] {
        color: #94A3B8;
    }

    [data-testid="stMetricValue"] {
        color: #F1F5F9;
    }

    [data-testid="stMetric"] {
        background-color: #172235;
        border: 1px solid #334155;
        border-left: 4px solid #22D3EE;
        border-radius: 12px;
        padding: 20px;
    }

    .incident-card {
        background-color: #172235;
        border: 1px solid #334155;
        border-left: 4px solid #F59E0B;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
    }

    .incident-label {
        color: #F59E0B;
        font-size: 14px;
        font-weight: 600;
    }

    .incident-sensor {
        color: #F1F5F9;
        font-size: 28px;
        font-weight: 600;
        margin: 10px 0;
    }

    .incident-recovery {
        color: #CBD5E1;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)


# Header.
logo_column, title_column = st.columns([1, 5])

with logo_column:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=120)

with title_column:
    st.title("Smart Factory Maintenance")
    st.write("Cooling Pump Monitoring — UTL-002")


# Load the saved simulation readings.
if not READINGS_PATH.exists():
    st.info("Run python cooling_pump.py first to generate readings.")
    st.stop()

try:
    readings = pd.read_csv(READINGS_PATH)
except pd.errors.EmptyDataError:
    st.info("The readings file is empty. Run the simulator again.")
    st.stop()

if readings.empty:
    st.info("No readings available. Run the simulator again.")
    st.stop()

latest_reading = readings.iloc[-1]

st.caption(
    f"Simulated data · Last saved reading: {latest_reading['Timestamp']}"
)


# Four latest sensor values.
flow_col, temp_col, pressure_col, vibration_col = st.columns(4)

with flow_col:
    st.metric(
        label="Water Flow",
        value=f"{latest_reading['Water Flow (L/min)']:g} L/min",
    )

with temp_col:
    st.metric(
        label="Temperature",
        value=f"{latest_reading['Motor Temperature (°C)']:g} °C",
    )

with pressure_col:
    st.metric(
        label="Pressure",
        value=f"{latest_reading['Water Pressure (bar)']:.2f} bar",
    )

with vibration_col:
    st.metric(
        label="Vibration",
        value=f"{latest_reading['Vibration (mm/s)']:.2f} mm/s",
    )

st.write("")


# Shared chart instructions.
def show_sensor_chart(column_name, axis_title):
    chart = (
        alt.Chart(readings)
        .mark_line(color="#22D3EE", strokeWidth=2)
        .encode(
            x=alt.X(
                "Reading:Q",
                title="Reading",
                axis=alt.Axis(format="d", tickMinStep=1),
            ),
            y=alt.Y(
                field=column_name,
                type="quantitative",
                title=axis_title,
                scale=alt.Scale(zero=False),
            ),
        )
        .properties(height=320, background="#0B1220")
        .configure_axis(
            labelColor="#CBD5E1",
            titleColor="#CBD5E1",
            gridColor="#334155",
            domainColor="#334155",
        )
        .configure_view(stroke=None)
    )

    # No .interactive(): dragging and zooming stay disabled.
    st.altair_chart(chart, use_container_width=True)


chart_col, incidents_col = st.columns([2, 1])


# Sensor-history tabs.
with chart_col:
    st.subheader("Sensor history")

    flow_tab, temp_tab, pressure_tab, vibration_tab = st.tabs(
        ["Flow", "Temperature", "Pressure", "Vibration"]
    )

    with flow_tab:
        show_sensor_chart("Water Flow (L/min)", "Flow (L/min)")

    with temp_tab:
        show_sensor_chart("Motor Temperature (°C)", "Temperature (°C)")

    with pressure_tab:
        show_sensor_chart("Water Pressure (bar)", "Pressure (bar)")

    with vibration_tab:
        show_sensor_chart("Vibration (mm/s)", "Vibration (mm/s)")


# Active incidents from the latest saved reading.
with incidents_col:
    st.subheader("Active incidents")
    active_count = 0

    for sensor in ["Flow", "Pressure", "Temperature", "Vibration"]:
        open_column = f"{sensor} Incident Open"
        recovery_column = f"{sensor} Recovery Count"

        if open_column not in readings.columns or recovery_column not in readings.columns:
            st.error(
                f"Missing incident columns for {sensor}. "
                "Run the updated cooling_pump.py."
            )
            st.stop()

        is_open = latest_reading[open_column]

        if str(is_open).strip().lower() == "true":
            active_count += 1
            recovery = int(latest_reading[recovery_column])

            st.markdown(f"""
<div class="incident-card">
    <div class="incident-label">OPEN INCIDENT</div>
    <div class="incident-sensor">{sensor}</div>
    <div class="incident-recovery">
        Recovery: {recovery}/4 normal readings
    </div>
</div>
""", unsafe_allow_html=True)

    if active_count == 0:
        st.success("No active incidents")


# Full incident-reading history.
with st.expander("Incident history"):
    st.caption(
        "Each row is one reading during an incident, "
        "including its recovery readings."
    )

    if not HISTORY_PATH.exists():
        st.info("Run the simulator to create the incident history file.")
    else:
        try:
            history = pd.read_csv(HISTORY_PATH)

            if history.empty:
                st.write("No incidents recorded in this run.")
            else:
                st.dataframe(
                    history,
                    use_container_width=True,
                    hide_index=True,
                )

        except pd.errors.EmptyDataError:
            st.write("The incident history file is empty.")


st.caption(
    "This dashboard shows a saved simulation. "
    "After running cooling_pump.py, refresh this page."
)