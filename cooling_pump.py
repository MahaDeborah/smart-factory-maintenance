import random
import csv
from datetime import datetime


machine_id  = "UTL-002"
machine_name = "cooling pump"
department = "Utilities"


print ("SMART FACTORY MAINTENANCE")
print("Machine ID:", machine_id)
print("Machine Name:", machine_name)
print("Department:", department)

water_flow =100
motor_temperature = 45
water_pressure = 4.0
vibration =1.5

incidents = {
   "flow":{"open":False, "normal_count":0, "id":None},
   "pressure":{"open":False, "normal_count":0, "id":None},
   "temperature":{"open":False, "normal_count":0, "id":None},
   "vibration":{"open":False, "normal_count":0, "id":None}
}
stage = "NORMAL"
readings_data = []
incident_history = []
incident_count = 0


for reading in range (1,31):
     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     if reading <= 10:
        stage = "NORMAL"
     elif reading <= 20:
        stage = "BLOCKAGE"
     else:
        stage = "RECOVERY"

     if stage=="NORMAL":
        change = random.randint(-2, 2)
     elif stage =="BLOCKAGE":   
      change = random.randint(-8, 3)
     elif stage=="RECOVERY":
        if water_flow < 95: 
         change = random.randint(-3,8) 
        else:
            change = random.randint(-2,2) 
     water_flow = water_flow + change 
     
     temperature_change = random.randint(-1, 1)
     motor_temperature = motor_temperature + temperature_change

     pressure_change = random.uniform(-0.1, 0.1)
     water_pressure = round(water_pressure + pressure_change, 2)
        
     vibration_change = random.uniform(-0.2, 0.2)
     vibration = max(0.0, round(vibration + vibration_change, 2))

     if vibration > 4.5:
        vibration_status = "CRITICAL"
     elif vibration > 2.5 :
        vibration_status = "WARNING"
     else:
        vibration_status = "NORMAL"

     if water_pressure < 3.0 or water_pressure > 5.0:
        pressure_status = "CRITICAL"
     elif water_pressure < 3.5 or water_pressure > 4.5:
        pressure_status = "WARNING"
     else:
        pressure_status = "NORMAL"

     if motor_temperature >=70:
        temperature_status = "CRITICAL"
     elif motor_temperature >= 55:
        temperature_status = "WARNING"
     else:
        temperature_status = "NORMAL"

     if water_flow < 70:
        status = "CRITICAL"
     elif water_flow >= 70 and water_flow < 90:
        status = "WARNING"
     elif water_flow >= 90 and water_flow <=110:
        status = "NORMAL"
     else:
        status = "WARNING"

     if (status=="CRITICAL" or pressure_status=="CRITICAL" or temperature_status=="CRITICAL" or vibration_status=="CRITICAL"):
        machine_status = "CRITICAL!!"
     elif (status=="WARNING" or pressure_status=="WARNING" or temperature_status=="WARNING" or vibration_status=="WARNING"):  
        machine_status = "WARNING"
     else:
        machine_status = "NORMAL"

     sensor_status = {
        "flow": status,
        "pressure": pressure_status,
        "temperature": temperature_status,
        "vibration": vibration_status,  
    }
     for sensor, sensor_stat in sensor_status.items():
         incident = incidents[sensor]
         was_open = incident["open"]
         print("checking:", sensor, "|status:", sensor_stat)

         if sensor_stat in ("WARNING", "CRITICAL"):
          incident["normal_count"] = 0
          if not incident["open"]:
           incident["open"] = True
           incident_count += 1
           incident["id"] = f"INC-{incident_count:03d}"
           print("NEW INCIDENT:", incident["id"], "| Sensor:", sensor)
         elif sensor_stat == "NORMAL":
          if incident["open"]:
            incident["normal_count"] += 1
            print(sensor, "recovery:", incident["normal_count"], "/4")

            if incident["normal_count"] == 4:
               incident["open"] = False
               print("INCIDENT CLOSED:", incident["id"], "| Sensor:", sensor)
               incident["normal_count"] = 0
         if incident["open"] or was_open:
             incident_history.append({
                 "Incident ID": incident["id"],
                 "Sensor": sensor,
                 "Reading": reading,
                 "Timestamp": timestamp,
                 "Status": sensor_stat
             })
     print("Simulation stage:", stage)
     print ("water_flow:",water_flow ,"L/min | Status:", status)
     print("Motor temperature:", motor_temperature, "°C| Temperature Status:", temperature_status)
     print("Water pressure:", water_pressure, "bar | Pressure Status:", pressure_status)
     print("Vibration:", vibration, "mm/s | Vibration Status:", vibration_status)
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
         "Vibration Recovery Count": incidents["vibration"]["normal_count"]
     })
     

with open("pump_readings.csv", "w", newline="", encoding="utf-8") as file:
           writer = csv.DictWriter(file, fieldnames=readings_data[0].keys())
           writer.writeheader()
           writer.writerows(readings_data)
print("Incident history readings:", len(incident_history)) 
for item in incident_history:
         print(item)    

if incident_history:
    with open("incident_history.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=incident_history[0].keys())
        writer.writeheader()
        writer.writerows(incident_history)