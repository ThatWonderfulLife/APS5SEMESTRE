import wmi
w = wmi.WMI(namespace="root\OpenHardwareMonitor")
temperature_infos = w.Sensor()
for sensor in temperature_infos:
    if sensor.SensorType==u'Temperature':

        if sensor.Name == "CPU Core #1":
            print(sensor.Value)