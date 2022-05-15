import webbrowser
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from turtle import Screen
import psutil
import wmi
from subprocess import Popen


#luz
def on_message_lb(mosq, obj, msg):
    if msg.payload.decode()=="1":
        print("liga")
        screen= Screen()
        screen.bgcolor("White")
    if msg.payload.decode()=="0":
        print("desliga")
        screen=Screen()
        screen.bye()


#youtube
def on_message_yt(mosq, obj,msg):
    global linkhttps

    if msg.topic == "APS/youtubelink":
        if msg.payload.decode().startswith("https"):
            linkhttps = msg.payload.decode()
            print(linkhttps)
        else:
            pass
        
    # printa o link do youtube e abre ou mata a task
    if msg.topic == "APS/youtube":
        if msg.payload.decode() == "1":
            print(linkhttps)
            webbrowser.open(linkhttps)
        if msg.payload.decode() == "0":
            Popen('taskkill /F /IM chrome.exe', shell=True)



w = wmi.WMI(namespace="root\OpenHardwareMonitor")
temperature_infos = w.Sensor()

#uso porcentagem
def on_message_active_resources(mosq, obj,msg):
    msg=msg.payload.decode()
    print(msg)
    if msg=="1":
        msgMemory = psutil.virtual_memory()[2]
        publish.single("APS/MEMuse", msgMemory, hostname="test.mosquitto.org")
        print (msgMemory)
        msgCpu = psutil.cpu_percent(4)
        publish.single("APS/CPUse", msgCpu, hostname="test.mosquitto.org")
        print(msgCpu)

        for sensor in temperature_infos:
            if sensor.SensorType==u'Temperature':

                if sensor.Name == "CPU Core #1":
                    print(sensor.Value)
                    CpuTemp = sensor.Value


        publish.single("APS/CPUtemp", CpuTemp ,hostname="test.mosquitto.org" )
        
    if msg=="0":
        publish.single("APS/CPUse", msg, hostname="test.mosquitto.org")
        publish.single("APS/MEMuse", msg, hostname="test.mosquitto.org")
        
#definição inicio do client mqtt
mqtt = mqtt.Client()

mqtt.message_callback_add('APS/youtube', on_message_yt)
mqtt.message_callback_add('APS/youtubelink', on_message_yt)

mqtt.message_callback_add('APS/lightBulb', on_message_lb)
mqtt.message_callback_add('APS/resources', on_message_active_resources)
# mqtt.on_message = on_message

#conexao e sub para ver todas as msgs
mqtt.connect("test.mosquitto.org", 1883, 30)
mqtt.subscribe("APS/#")


#inicia o loop infinito do mqtt
mqtt.loop_forever()