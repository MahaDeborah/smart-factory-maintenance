from pathlib import Path
from html import escape

import altair as alt
import pandas as pd
import streamlit as st


# Files beside this dashboard.
BASE_DIR = Path(__file__).resolve().parent
READINGS_PATH = BASE_DIR / "pump_readings.csv"
HISTORY_PATH = BASE_DIR / "incident_history.csv"

GREEN = "#047857"
BLUE = "#1D4ED8"
RED = "#991B1B"

SENSORS = {
    "Flow": {
        "column": "Water Flow (L/min)",
        "status": "Flow Status",
        "unit": "L/min",
        "thresholds": [
            (70, "Critical below 70", RED),
            (90, "Warning below 90", BLUE),
            (110, "Warning above 110", BLUE),
        ],
    },
    "Temperature": {
        "column": "Motor Temperature (°C)",
        "status": "Temperature Status",
        "unit": "°C",
        "thresholds": [
            (55, "Warning at 55 and above", BLUE),
            (70, "Critical at 70 and above", RED),
        ],
    },
    "Pressure": {
        "column": "Water Pressure (bar)",
        "status": "Pressure Status",
        "unit": "bar",
        "thresholds": [
            (3.0, "Critical below 3.0", RED),
            (3.5, "Warning below 3.5", BLUE),
            (4.5, "Warning above 4.5", BLUE),
            (5.0, "Critical above 5.0", RED),
        ],
    },
    "Vibration": {
        "column": "Vibration (mm/s)",
        "status": "Vibration Status",
        "unit": "mm/s",
        "thresholds": [
            (2.5, "Warning above 2.5", BLUE),
            (4.5, "Critical above 4.5", RED),
        ],
    },
}


st.set_page_config(
    page_title="Smart Factory Maintenance",
    layout="wide",
)

st.markdown(
    """
<style>
    .stApp {
        background-color: #FFFFFF;
        color: #1F2937;
        font-family: "Segoe UI", Arial, sans-serif;
    }

    .stApp h1, .stApp h2, .stApp h3,
    .stApp p, .stApp label,
    [data-testid="stMetric"] {
        font-family: "Segoe UI", Arial, sans-serif;
    }

    .stApp h1 {
        color: #1F2937;
        font-size: 30px;
        font-weight: 600;
    }

    .stApp h2, .stApp h3 {
        color: #1F2937;
        font-size: 21px;
        font-weight: 600;
    }

    [data-testid="stMetric"] {
        background-color: #F0FDF4;
        border: 1px solid #D1FAE5;
        border-left: 3px solid #047857;
        border-radius: 8px;
        padding: 18px;
    }

    [data-testid="stMetricLabel"] {
        color: #475569;
    }

    [data-testid="stMetricValue"] {
        color: #1F2937;
        font-size: 30px;
        font-weight: 500;
    }

    .incident-card {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-left: 4px solid;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
    }

    .incident-label {
        font-size: 12px;
        font-weight: 600;
    }

    .incident-sensor {
        color: #1F2937;
        font-size: 23px;
        font-weight: 600;
        margin: 10px 0;
    }

    .incident-detail {
        color: #475569;
        font-size: 15px;
        margin-top: 10px;
        line-height: 1.5;
    }

    .recovery-track {
        display: flex;
        gap: 6px;
        margin-top: 16px;
    }

    .recovery-segment {
        flex: 1;
        height: 8px;
        border-radius: 3px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Load the saved readings.
st.title("Smart Factory Maintenance")
st.write("Cooling pump · UTL-002 · Utilities")

if not READINGS_PATH.exists():
    st.info("Run python cooling_pump.py to generate readings.")
    st.stop()

try:
    readings = pd.read_csv(READINGS_PATH)
except pd.errors.EmptyDataError:
    st.info("The readings file is empty. Run the simulator again.")
    st.stop()

if readings.empty:
    st.info("No readings available. Run the simulator again.")
    st.stop()

required_columns = {"Reading", "Timestamp"}

for sensor, settings in SENSORS.items():
    required_columns.update([
        settings["column"],
        settings["status"],
        f"{sensor} Incident Open",
        f"{sensor} Recovery Count",
    ])

missing = required_columns - set(readings.columns)

if missing:
    st.error("Missing CSV columns: " + ", ".join(sorted(missing)))
    st.info("Run the updated cooling_pump.py.")
    st.stop()

readings = readings.sort_values("Reading").reset_index(drop=True)
latest_reading = readings.iloc[-1]

st.caption(
    "Saved simulation · Last generated: "
    f"{latest_reading['Timestamp']}"
)


# Latest values, without repeated normal-range captions.
metric_columns = st.columns(4)

for column, (sensor, settings) in zip(
    metric_columns, SENSORS.items()
):
    with column:
        value = float(latest_reading[settings["column"]])

        st.metric(
            label=sensor,
            value=f"{value:g} {settings['unit']}",
        )

st.write("")


def show_sensor_chart(sensor):
    settings = SENSORS[sensor]

    data = readings[
        ["Reading", settings["column"], settings["status"]]
    ].copy()
    data.columns = ["Reading", "Value", "Status"]

    data["Status"] = data["Status"].replace({
        "CHECK HIGH FLOW": "WARNING",
    })

    limits = [item[0] for item in settings["thresholds"]]
    lowest = min(float(data["Value"].min()), min(limits))
    highest = max(float(data["Value"].max()), max(limits))
    padding = max((highest - lowest) * 0.12, 0.1)

    y_scale = alt.Scale(
        domain=[lowest - padding, highest + padding],
        zero=False,
        nice=False,
    )

    base = alt.Chart(data).encode(
        x=alt.X(
            "Reading:Q",
            title="Reading",
            axis=alt.Axis(
                format="d",
                tickMinStep=1,
                tickCount=7,
                labelOverlap=True,
            ),
        ),
        y=alt.Y(
            "Value:Q",
            title=f"{sensor} ({settings['unit']})",
            scale=y_scale,
        ),
    )

    line = base.mark_line(
        color=GREEN,
        strokeWidth=2,
    )

    points = base.mark_point(
        filled=True,
        size=70,
        opacity=1,
    ).encode(
        color=alt.Color(
            "Status:N",
            scale=alt.Scale(
                domain=["NORMAL", "WARNING", "CRITICAL"],
                range=[GREEN, BLUE, RED],
            ),
            legend=alt.Legend(
                title=None,
                orient="bottom",
            ),
        ),
        shape=alt.Shape(
            "Status:N",
            scale=alt.Scale(
                domain=["NORMAL", "WARNING", "CRITICAL"],
                range=["circle", "triangle-up", "diamond"],
            ),
            legend=alt.Legend(
                title=None,
                orient="bottom",
            ),
        ),
        tooltip=[
            alt.Tooltip("Reading:Q", title="Reading", format="d"),
            alt.Tooltip(
                "Value:Q",
                title=f"{sensor} ({settings['unit']})",
                format=".2f",
            ),
            alt.Tooltip("Status:N", title="Status"),
        ],
    )

    layers = []

    for value, label, colour in settings["thresholds"]:
        threshold_data = pd.DataFrame({
            "Limit": [value],
            "Label": [label],
        })

        rule = (
            alt.Chart(threshold_data)
            .mark_rule(
                color=colour,
                strokeDash=[2, 3] if colour == RED else [8, 4],
                strokeWidth=1.5,
            )
            .encode(
                y=alt.Y("Limit:Q", scale=y_scale),
            )
        )

        label_chart = (
            alt.Chart(threshold_data)
            .mark_text(
                align="left",
                baseline="bottom",
                dy=-5,
                color=colour,
                fontSize=11,
            )
            .encode(
                x=alt.value(8),
                y=alt.Y("Limit:Q", scale=y_scale),
                text="Label:N",
            )
        )

        layers.extend([rule, label_chart])

    chart = (
        alt.layer(*layers, line, points)
        .properties(height=350, background="#FFFFFF")
        .configure(font="Segoe UI")
        .configure_axis(
            domain=True,
            domainColor="#475569",
            domainWidth=1.5,
            ticks=True,
            tickColor="#475569",
            tickSize=5,
            labelColor="#475569",
            titleColor="#475569",
            gridColor="#E5E7EB",
            labelFontSize=12,
            titleFontSize=12,
            titleFontWeight="normal",
            labelPadding=6,
            titlePadding=12,
        )
        .configure_legend(
            labelColor="#475569",
            labelFontSize=12,
        )
        .configure_view(
            stroke="#CBD5E1",
            strokeWidth=1,
        )
    )

    # No interactive(): the graph cannot be dragged or zoomed.
    st.altair_chart(chart, use_container_width=True)


# Graph and currently open incidents.
chart_column, incidents_column = st.columns([2, 1])

with chart_column:
    st.subheader("Sensor history")
    st.caption(
        "Blue dashed lines: warning limits · "
        "Red dotted lines: critical limits"
    )

    tabs = st.tabs(list(SENSORS))

    for tab, sensor in zip(tabs, SENSORS):
        with tab:
            show_sensor_chart(sensor)


with incidents_column:
    st.subheader("Currently open incidents")
    st.caption(
        f"At reading {int(latest_reading['Reading'])}. "
        "Closed incidents appear in history below."
    )

    active_count = 0

    for sensor, settings in SENSORS.items():
        is_open = (
            str(latest_reading[f"{sensor} Incident Open"])
            .strip()
            .lower()
            == "true"
        )

        if not is_open:
            continue

        active_count += 1

        recovery = int(
            latest_reading[f"{sensor} Recovery Count"]
        )
        status = str(latest_reading[settings["status"]])
        value = float(latest_reading[settings["column"]])

        if status == "CRITICAL":
            accent = RED
            label = "CRITICAL"
            explanation = (
                "The latest reading is beyond a critical limit."
            )
        elif status == "NORMAL":
            accent = BLUE
            label = "RECOVERING"
            remaining = max(0, 4 - recovery)
            noun = "reading" if remaining == 1 else "readings"

            explanation = (
                f"{sensor} is normal again. Needs {remaining} more "
                f"consecutive normal {noun} to close."
            )
        else:
            accent = BLUE
            label = "WARNING"
            explanation = (
                "The latest reading is outside the normal range. "
                "Recovery counting starts when it returns to normal."
            )

        segments = ""

        for index in range(4):
            colour = GREEN if index < recovery else "#E5E7EB"

            segments += (
                '<span class="recovery-segment" '
                f'style="background-color: {colour};"></span>'
            )

        st.markdown(
            f"""
<div class="incident-card" style="border-left-color: {accent};">
    <div class="incident-label" style="color: {accent};">
        {label}
    </div>
    <div class="incident-sensor">{escape(sensor)}</div>
    <div class="incident-detail">
        {value:g} {escape(settings["unit"])}
    </div>
    <div class="incident-detail">{escape(explanation)}</div>
    <div class="recovery-track">{segments}</div>
    <div class="incident-detail">
        Recovery confirmation: {recovery} of 4 normal readings
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    if active_count == 0:
        st.success("No currently open incidents.")


# One summary row per incident, with individual readings available.
with st.expander("Incident history"):
    if not HISTORY_PATH.exists():
        st.info("Run the simulator to create incident history.")
    else:
        try:
            history = pd.read_csv(HISTORY_PATH)
        except pd.errors.EmptyDataError:
            history = pd.DataFrame()

        if history.empty:
            st.write("No incidents recorded in this run.")
        else:
            history_columns = {
                "Incident ID",
                "Sensor",
                "Reading",
                "Timestamp",
                "Status",
            }

            if not history_columns.issubset(history.columns):
                st.error(
                    "The history file has missing columns. "
                    "Run the updated simulator."
                )
            else:
                history = history.sort_values("Reading")
                summary_rows = []

                for (incident_id, sensor), group in history.groupby(
                    ["Incident ID", "Sensor"],
                    sort=False,
                ):
                    group = group.sort_values("Reading")

                    # The simulator closes an incident after four
                    # consecutive NORMAL readings and logs the fourth.
                    closed = (
                        len(group) >= 4
                        and group["Status"].tail(4).eq("NORMAL").all()
                    )

                    last_status = str(group.iloc[-1]["Status"])

                    if closed:
                        state = "Closed"
                    elif last_status == "NORMAL":
                        state = "Recovering"
                    elif last_status == "CRITICAL":
                        state = "Critical"
                    else:
                        state = "Warning"

                    summary_rows.append({
                        "Incident ID": incident_id,
                        "Sensor": str(sensor).title(),
                        "First reading": int(group["Reading"].min()),
                        "Last recorded reading": int(
                            group["Reading"].max()
                        ),
                        "Recorded readings": len(group),
                        "State": state,
                    })

                summary = pd.DataFrame(summary_rows)

                sensor_colours = {
                    "Flow": "#365F81",
                    "Pressure": "#28675F",
                    "Temperature": "#596574",
                    "Vibration": "#344563",
                }

                def style_sensor(column):
                    return [
                        "background-color: #F3F4F6; "
                        f"color: {sensor_colours.get(value, '#374151')}; "
                        "font-weight: 600;"
                        for value in column
                    ]

                def style_state(column):
                    colours = {
                        "Closed": GREEN,
                        "Recovering": BLUE,
                        "Warning": BLUE,
                        "Critical": RED,
                    }

                    return [
                        f"color: {colours.get(value, '#374151')}; "
                        "font-weight: 600;"
                        for value in column
                    ]

                styled_summary = (
                    summary.style
                    .apply(style_sensor, subset=["Sensor"])
                    .apply(style_state, subset=["State"])
                )

                st.caption(
                    "One row per incident from the saved simulation."
                )

                st.dataframe(
                    styled_summary,
                    use_container_width=True,
                    hide_index=True,
                )

                selected_id = st.selectbox(
                    "View readings for an incident",
                    summary["Incident ID"].unique(),
                )

                details = history[
                    history["Incident ID"] == selected_id
                ]

                st.dataframe(
                    details,
                    use_container_width=True,
                    hide_index=True,
                )


st.caption(
    "Saved simulation data. After running cooling_pump.py, "
    "refresh this page to load the new readings."
)