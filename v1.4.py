from webbrowser import Chrome
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from turtle import Screen
import psutil
import wmi

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
driver = webdriver.Chrome(chrome_options=chrome_options)

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
    )

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
    global link
    link = msg.payload.decode()

    if link == "" or "1" or "0":
        link= "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        pass
    if msg.payload.decode().startswith("https"):
        link = msg.payload.decode()
    else:
        pass
    if msg.payload.decode() == "1":
        driver = webdriver.Chrome()
        driver.get(link)

    else:
        pass


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
mqtt.message_callback_add('APS/lightBulb', on_message_lb)
mqtt.message_callback_add('APS/resources', on_message_active_resources)
# mqtt.on_message = on_message

#conexao e sub para ver todas as msgs
mqtt.connect("test.mosquitto.org", 1883, 30)
mqtt.subscribe("APS/#")


#inicia o loop infinito do mqtt
mqtt.loop_forever()