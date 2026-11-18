import random
import csv
from datetime import datetime
from pathlib import Path


# 1. SET UP THE MACHINE
BASE_DIR = Path(__file__).resolve().parent

machine_id = "UTL-002"
machine_name = "cooling pump"
department = "Utilities"

print("SMART FACTORY MAINTENANCE")
print("Machine ID:", machine_id)
print("Machine Name:", machine_name)
print("Department:", department)

water_flow = 100
motor_temperature = 45
water_pressure = 4.0
vibration = 1.5

incidents = {
    "flow": {"open": False, "normal_count": 0, "id": None},
    "pressure": {"open": False, "normal_count": 0, "id": None},
    "temperature": {"open": False, "normal_count": 0, "id": None},
    "vibration": {"open": False, "normal_count": 0, "id": None},
}

readings_data = []
incident_history = []
incident_count = 0


# 2. RANDOMLY SELECT BETWEEN ONE AND FOUR SENSORS
sensor_names = ["flow", "pressure", "temperature", "vibration"]

fault_count = random.randint(1, 4)
fault_sensors = random.sample(sensor_names, fault_count)

print("Sensors selected for faults:", ", ".join(fault_sensors))


# 3. GENERATE READINGS AND CHECK THEIR STATUSES
for reading in range(1, 31):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if reading <= 10:
        stage = "NORMAL"
    elif reading <= 20:
        stage = "FAULT"
    else:
        stage = "RECOVERY"

    if stage == "NORMAL":
        water_flow = random.randint(98, 102)
        motor_temperature = random.randint(44, 46)
        water_pressure = random.uniform(3.9, 4.1)
        vibration = random.uniform(1.3, 1.7)

    elif stage == "FAULT":
        if "flow" in fault_sensors:
            water_flow = max(0, water_flow - random.randint(3, 6))
        else:
            water_flow = random.randint(98, 102)

        if "temperature" in fault_sensors:
            motor_temperature += random.randint(2, 4)
        else:
            motor_temperature = random.randint(44, 46)

        if "pressure" in fault_sensors:
            water_pressure += random.uniform(0.1, 0.2)
        else:
            water_pressure = random.uniform(3.9, 4.1)

        if "vibration" in fault_sensors:
            vibration += random.uniform(0.3, 0.5)
        else:
            vibration = random.uniform(1.3, 1.7)

    else:  # RECOVERY
        if "flow" in fault_sensors:
            water_flow = min(
                100, water_flow + random.randint(4, 7)
            )
        else:
            water_flow = random.randint(98, 102)

        if "temperature" in fault_sensors:
            motor_temperature = max(
                45, motor_temperature - random.randint(3, 5)
            )
        else:
            motor_temperature = random.randint(44, 46)

        if "pressure" in fault_sensors:
            water_pressure = max(
                4.0, water_pressure - random.uniform(0.15, 0.25)
            )
        else:
            water_pressure = random.uniform(3.9, 4.1)

        if "vibration" in fault_sensors:
            vibration = max(
                1.5, vibration - random.uniform(0.4, 0.6)
            )
        else:
            vibration = random.uniform(1.3, 1.7)

    water_pressure = round(water_pressure, 2)
    vibration = round(vibration, 2)

    # Decide the status of each sensor.
    if water_flow < 70:
        status = "CRITICAL"
    elif water_flow < 90 or water_flow > 110:
        status = "WARNING"
    else:
        status = "NORMAL"

    if motor_temperature >= 70:
        temperature_status = "CRITICAL"
    elif motor_temperature >= 55:
        temperature_status = "WARNING"
    else:
        temperature_status = "NORMAL"

    if water_pressure < 3.0 or water_pressure > 5.0:
        pressure_status = "CRITICAL"
    elif water_pressure < 3.5 or water_pressure > 4.5:
        pressure_status = "WARNING"
    else:
        pressure_status = "NORMAL"

    if vibration > 4.5:
        vibration_status = "CRITICAL"
    elif vibration > 2.5:
        vibration_status = "WARNING"
    else:
        vibration_status = "NORMAL"

    sensor_status = {
        "flow": status,
        "pressure": pressure_status,
        "temperature": temperature_status,
        "vibration": vibration_status,
    }

    if "CRITICAL" in sensor_status.values():
        machine_status = "CRITICAL"
    elif "WARNING" in sensor_status.values():
        machine_status = "WARNING"
    else:
        machine_status = "NORMAL"

    print("\nReading:", reading, "| Stage:", stage)

    # 4. TRACK EACH SENSOR'S INCIDENT SEPARATELY
    for sensor, sensor_stat in sensor_status.items():
        incident = incidents[sensor]
        was_open = incident["open"]

        if sensor_stat in ("WARNING", "CRITICAL"):
            incident["normal_count"] = 0

            if not incident["open"]:
                incident["open"] = True
                incident_count += 1
                incident["id"] = f"INC-{incident_count:03d}"

                print(
                    "NEW INCIDENT:", incident["id"],
                    "| Sensor:", sensor,
                )

        elif sensor_stat == "NORMAL":
            if incident["open"]:
                incident["normal_count"] += 1

                print(
                    sensor,
                    "recovery:",
                    incident["normal_count"],
                    "/4",
                )

                if incident["normal_count"] == 4:
                    incident["open"] = False

                    print(
                        "INCIDENT CLOSED:", incident["id"],
                        "| Sensor:", sensor,
                    )

                    incident["normal_count"] = 0

        # Include the final recovery reading in the history.
        if incident["open"] or was_open:
            incident_history.append({
                "Incident ID": incident["id"],
                "Sensor": sensor,
                "Reading": reading,
                "Timestamp": timestamp,
                "Status": sensor_stat,
            })

    print("Water flow:", water_flow, "L/min | Status:", status)
    print(
        "Motor temperature:", motor_temperature,
        "°C | Status:", temperature_status,
    )
    print(
        "Water pressure:", water_pressure,
        "bar | Status:", pressure_status,
    )
    print(
        "Vibration:", vibration,
        "mm/s | Status:", vibration_status,
    )
    print("Overall machine condition:", machine_status)

    readings_data.append({
        "Reading": reading,
        "Timestamp": timestamp,
        "Stage": stage,
        "Water Flow (L/min)": water_flow,
        "Flow Status": status,
        "Motor Temperature (°C)": motor_temperature,
        "Temperature Status": temperature_status,
        "Water Pressure (bar)": water_pressure,
        "Pressure Status": pressure_status,
        "Vibration (mm/s)": vibration,
        "Vibration Status": vibration_status,
        "Machine Status": machine_status,
        "Flow Incident Open": incidents["flow"]["open"],
        "Flow Recovery Count": incidents["flow"]["normal_count"],
        "Pressure Incident Open": incidents["pressure"]["open"],
        "Pressure Recovery Count": incidents["pressure"]["normal_count"],
        "Temperature Incident Open": incidents["temperature"]["open"],
        "Temperature Recovery Count": incidents["temperature"]["normal_count"],
        "Vibration Incident Open": incidents["vibration"]["open"],
        "Vibration Recovery Count": incidents["vibration"]["normal_count"],
    })


# 5. SAVE AFTER ALL 30 READINGS ARE FINISHED
with open(
    BASE_DIR / "pump_readings.csv",
    "w",
    newline="",
    encoding="utf-8",
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=readings_data[0].keys(),
    )
    writer.writeheader()
    writer.writerows(readings_data)

with open(
    BASE_DIR / "incident_history.csv",
    "w",
    newline="",
    encoding="utf-8",
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "Incident ID",
            "Sensor",
            "Reading",
            "Timestamp",
            "Status",
        ],
    )
    writer.writeheader()
    writer.writerows(incident_history)

print("\nSimulation finished.")
print("Incidents created:", incident_count)
print("Incident history readings:", len(incident_history))