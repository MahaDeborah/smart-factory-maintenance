# Smart Factory Maintenance 

 [View live demo](https://deborah-smart-factory.streamlit.app/)

The demo displays saved simulated sensor readings.
A python operator that simulates cooling pump operation, detects abnormal sensor readings, and tract incidents through recovery.

I built this project to practise industrial monitoring, incident tracking and data visualisation.

#Overview

The application monitors a simulated cooling pump, **UTL-002** in a factory's utilities department 
-Water flow - L/min
-Motor temperature -c
-Water pressure - bar
-Vibration-mm/s

The streamlit dashboard displays the latest values, sensory history charts, open incident, and incident history

##Features

-Random selection of one to four sensors to develop faults 
-Normal, faults and recovery simulation stages 
-Threshold based warning and critical alerts 
-Independent incident tracking for each sensor 
-Incident closure after four consecutive normal reading
-Charts with labelled thresholds and distinct colours and shapes
- Recovery progress for open incidents
- Incident summaries to access to individual reading
- CSV export of reading and incident history

 ##How it works 

 | Reading | Stage | Behaviour|
 |---|---|---|
 |1-10| Normal | Sensors fluctuate around normal values |
 |11-20| Fault | Selected sensors gradually develop abnormal readings|
 |21-30| Recovery| Affected sensors move back towards normal values|

 Each run randomly selects the number of affected sensors and which sensors are affected.

 ##Incident tracking 

 An incident opens when a sensor enter warning or critical state. Each incident receives a unique ID within that run.

 An incident closes after **four consecutive normal readings** from its sensor. A warning or critical reading resets the the recovery counter.
 
 A sensor can therefore show a normal reading while its incident remains open awaiting recovery confirmation. Some incidents may still be open while the simulation ends.

 The dashborad shows:
 -**Currently open incidents:** incidents still open at the latest saved reading.
 -**Incident history:** both open and closed incident recorded during the run 

 ## Alert thresholds

Critical conditions take priority over warning conditions.

| Sensor | Normal | Warning | Critical |
|---|---|---|---|
| Water flow | 90–110 L/min | 70 to below 90, or above 110 L/min | Below 70 L/min |
| Motor temperature | Below 55°C | 55 to below 70°C | 70°C or above |
| Water pressure | 3.5–4.5 bar | 3.0 to below 3.5, or above 4.5 to 5.0 bar | Below 3.0 or above 5.0 bar |
| Vibration | Up to 2.5 mm/s | Above 2.5 to 4.5 mm/s | Above 4.5 mm/s |

These thresholds are demonstration settings, not validated operating limits for real equipment.

## Technology
-**Python:** simulation and incident logic
-**Streamlit:** dashboard
-**Pandas:** data loading and incident summaries
-**Altair:** sensor history charts 
-**CSV:** saved readings and incident records
 
 ##Run locally
 
 #### Smart Factory Maintenance

A Python application that simulates cooling-pump operation, detects abnormal sensor readings, and tracks incidents through recovery.

I built this project to practise industrial monitoring, incident tracking, and data visualisation.

## Overview

The application monitors a simulated cooling pump, **UTL-002**, in a factory’s Utilities department.

It tracks four measurements:

- Water flow — L/min
- Motor temperature — °C
- Water pressure — bar
- Vibration — mm/s

The Streamlit dashboard displays the latest values, sensor-history charts, open incidents, and incident history from the saved simulation.

## Features

- Random selection of one to four sensors to develop faults
- Normal, fault, and recovery simulation stages
- Threshold-based warning and critical alerts
- Independent incident tracking for each sensor
- Incident closure after four consecutive normal readings
- Charts with labelled thresholds and distinct status colours and shapes
- Recovery progress for open incidents
- Incident summaries with access to individual readings
- CSV export of readings and incident history

## How it works

Each simulation generates **30 readings**:

| Readings | Stage | Behaviour |
|---|---|---|
| 1–10 | Normal | Sensors fluctuate around normal values |
| 11–20 | Fault | Selected sensors gradually develop abnormal readings |
| 21–30 | Recovery | Affected sensors move back toward normal values |

Each run randomly selects both the number of affected sensors and which sensors are affected.

### Incident tracking

An incident opens when a sensor enters a warning or critical state. Each incident receives a unique ID within that run.

An incident closes after **four consecutive normal readings** from its sensor. A warning or critical reading resets the recovery counter.

A sensor can therefore show a normal value while its incident remains open, awaiting recovery confirmation. Some incidents may still be open when the simulation ends.

The dashboard shows:

- **Currently open incidents:** incidents still open at the latest saved reading.
- **Incident history:** both open and closed incidents recorded during the run.

## Alert thresholds

Critical conditions take priority over warning conditions.

| Sensor | Normal | Warning | Critical |
|---|---|---|---|
| Water flow | 90–110 L/min | 70 to below 90, or above 110 L/min | Below 70 L/min |
| Motor temperature | Below 55°C | 55 to below 70°C | 70°C or above |
| Water pressure | 3.5–4.5 bar | 3.0 to below 3.5, or above 4.5 to 5.0 bar | Below 3.0 or above 5.0 bar |
| Vibration | Up to 2.5 mm/s | Above 2.5 to 4.5 mm/s | Above 4.5 mm/s |

These thresholds are demonstration settings, not validated operating limits for real equipment.

## Technology

- **Python:** simulation and incident logic
- **Streamlit:** dashboard
- **pandas:** data loading and incident summaries
- **Altair:** sensor-history charts
- **CSV:** saved readings and incident records

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/MahaDeborah/smart-factory-maintenance.git
cd smart-factory-maintenance
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the dashboard

```bash
python -m streamlit run dashboard.py
```

Open the local URL shown in the terminal.

Sample CSV files are included, so the dashboard can display a saved simulation immediately.

## Generate a new simulation

Run:

```bash
python cooling_pump.py
```

Refresh the dashboard afterward to load the new results.

Each run replaces:

- `pump_readings.csv`
- `incident_history.csv`

Previous runs are not retained. Incident numbering restarts with each run.

## Project files

| File | Purpose |
|---|---|
| `cooling_pump.py` | Generates readings, classifies conditions, and tracks incidents |
| `dashboard.py` | Displays sensor values, charts,
recovery progress, and history |
| `pump_readings.csv` | Sensor readings and incident states from the saved run |
| `incident_history.csv` | Readings recorded during incidents |
| `.streamlit/config.toml` | Dashboard theme settings |
| `requirements.txt` | Python dependencies |

## Scope and limitations

-The data is limited no physical equipment is connected
-Fault patterns demonstrate abnormal behaviour rather than model pump physics
-Alerts use predefined rules, not machine learning.
-The dashboard displays saved results rather than a live sensor stream
-The application currently supports one cooling pump.
-Results have not been validated for operational maintenance desicions.

##Future improvements

-Automated test for threshold boundaries and recovery logic 
-Database storage for multiple simulation runs 
-support for additional machines
-Simulation controls within the dashboard


##**Author**

 **Maha Deborah**
 
 Control in Technical Systems Student at LETI, interested in industrial software, machine learning and computer vision.
 [GitHub profile](https://github.com/MahaDeborah)

