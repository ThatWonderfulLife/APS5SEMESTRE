from webbrowser import Chrome
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import random
from turtle import Screen
import psutil
import wmi


active="0"





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

    if msg.payload.decode().startswith("https"):
        link = msg.payload.decode()
    elif msg.payload.decode() == "1":
        print("abre carai",link)
    else:
        pass



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