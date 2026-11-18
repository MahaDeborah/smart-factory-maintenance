
# Smart Factory Maintenance

[View Live Demo](https://deborah-smart-factory.streamlit.app/)

A Python application that simulates cooling pump operation, detects abnormal sensor readings, and tracks incidents through recovery.

I built this project to practise industrial monitoring, incident tracking, and data visualisation.

## Overview

The application monitors a simulated cooling pump (UTL-002) in a factory's Utilities department.

It tracks four measurements:

- Water flow (L/min)
- Motor temperature (°C)
- Water pressure (bar)
- Vibration (mm/s)

The Streamlit dashboard displays the latest sensor readings, history charts, open incidents, and incident history.

## Features

- Random selection of one to four sensors to develop faults
- Normal, fault, and recovery simulation stages
- Threshold-based warning and critical alerts
- Independent incident tracking for each sensor
- Incident closure after four consecutive normal readings
- Sensor history charts with labelled thresholds
- Recovery progress for open incidents
- Incident history and CSV export

## How It Works

Each simulation generates 30 readings.

| Readings | Stage | Behaviour |
|---|---|---|
| 1–10 | Normal | Sensors fluctuate around normal values |
| 11–20 | Fault | Selected sensors gradually develop abnormal readings |
| 21–30 | Recovery | Affected sensors move back towards normal values |

Each run randomly selects the number of affected sensors and which sensors are affected.

### Incident Tracking

An incident opens when a sensor enters a warning or critical state.

Each incident receives a unique ID within that simulation run.

An incident closes after four consecutive normal readings from the affected sensor.

If another warning or critical reading occurs, the recovery counter resets.

A sensor can therefore show a normal reading while its incident remains open, waiting for recovery confirmation.

Some incidents may still be open when the simulation ends.

## Alert Thresholds

Critical conditions take priority over warning conditions.

| Sensor | Normal | Warning | Critical |
|---|---|---|---|
| Water flow | 90–110 L/min | 70 to below 90, or above 110 L/min | Below 70 L/min |
| Motor temperature | Below 55°C | 55 to below 70°C | 70°C or above |
| Water pressure | 3.5–4.5 bar | 3.0 to below 3.5, or above 4.5 to 5.0 bar | Below 3.0 or above 5.0 bar |
| Vibration | Up to 2.5 mm/s | Above 2.5 to 4.5 mm/s | Above 4.5 mm/s |

These thresholds are demonstration settings and are not validated operating limits for real equipment.

## Technologies Used

- **Python:** Sensor simulation and incident tracking
- **Streamlit:** Dashboard interface
- **Pandas:** Data loading and incident summaries
- **Altair:** Sensor history charts
- **CSV:** Storage of simulated readings and incident records

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/MahaDeborah/smart-factory-maintenance.git
cd smart-factory-maintenance
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

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

Open the local URL shown in your terminal.

Sample CSV files are included, so the dashboard can display saved simulation results immediately.

## Generate a New Simulation

Run:

```bash
python cooling_pump.py
```

Refresh the dashboard afterward to load the new results.

Each run replaces:

- `pump_readings.csv`
- `incident_history.csv`

Previous runs are not retained, and incident numbering restarts with each run.

## Project Structure

| File | Purpose |
|---|---|
| `cooling_pump.py` | Generates readings, classifies conditions, and tracks incidents |
| `dashboard.py` | Displays sensor values, charts, recovery progress, and incident history |
| `pump_readings.csv` | Stores sensor readings and incident states |
| `incident_history.csv` | Stores readings recorded during incidents |
| `.streamlit/config.toml` | Dashboard theme settings |
| `requirements.txt` | Python dependencies |

## Scope and Limitations

- The data is simulated; no physical equipment is connected.
- Fault patterns demonstrate abnormal behaviour rather than modelling actual pump physics.
- Alerts use predefined rules, not machine learning.
- The dashboard displays saved results rather than a live sensor stream.
- The application currently supports one cooling pump.
- Results have not been validated for operational maintenance decisions.

## Future Improvements

- Automated tests for threshold boundaries and recovery logic
- Database storage for multiple simulation runs
- Support for additional machines
- Simulation controls within the dashboard

## Author

**Deborah Maha**

Control in Technical Systems student at LETI University.

Interested in software development, automation, machine learning, and computer vision.

[GitHub Profile](https://github.com/MahaDeborah)
