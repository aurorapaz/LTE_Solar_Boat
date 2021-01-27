import paho.mqtt.client as mqtt
import time
from datetime import datetime
import time
import sys
import serial
import threading

BROKER_IP = 'localhost'
TOPIC = 'solar_sensor'
VALUE_SEPARATOR = '%'
SAMPLES_SENT = 10
TOPIC_ALARMAS = 'server_alarm'

timestamp_list = []
height_list = []
pitch_list = []
roll_list = []
speed_list = []
latitude_list = []
longitude_list = []
i=0

client = mqtt.Client("solarboat", clean_session=True, transport="tcp")
client.username_pw_set("solarboat", password="solarboat")
client.connect(BROKER_IP)
paqueteAlarma=0
datosAlarmaTimestamps=[]
def mqtt_client_publisher():
    SECS = 0
    print("LOOP P")
    paquete=0
    while True:
        reset_lists()
        read_arduino_data(SECS)
        SECS = SECS +1
        if SECS == 51:
            SECS=0
        datosAlarmaTimestamps.append(datetime.utcnow())
        client.publish(TOPIC, f'{format_mqtt_data()}', qos=0)

def mqtt_client_subscriber():
    client.on_message = on_message
    client.subscribe(TOPIC_ALARMAS)
    print("LOOP S")
    client.loop_forever()


def on_message(client, userdata, msg):
    global paqueteAlarma
    print((datetime.utcnow()-datosAlarmaTimestamps[paqueteAlarma]))
    paqueteAlarma=paqueteAlarma+1
    print(msg)



def check_data_len():
    lens = [len(timestamp_list),len(height_list),len(pitch_list),len(roll_list),len(speed_list),len(latitude_list),len(longitude_list)]
    print(lens)
    for l in lens:
        if l != 10:
            print("LENGTH ERROR")


def print_ardunio_data():
    for i in range(len(timestamp_list)):
        print(f'{timestamp_list[i]}:')
        print(f'height: {height_list[i]}')
        print(f'pitch: {pitch_list[i]}')
        print(f'roll: {roll_list[i]}')
        print(f'speed: {speed_list[i]}')
        print(f'latitude: {latitude_list[i]}')
        print(f'longitude: {longitude_list[i]}')

def format_mqtt_data():
    to_send_string = ''
    for i in range(len(timestamp_list)):
        value = f'{timestamp_list[i]}%{height_list[i]}%{pitch_list[i]}%{roll_list[i]}%{speed_list[i]}%{latitude_list[i]}%{longitude_list[i]}'
        if i == 0:
            to_send_string = value
        else:
            to_send_string += f'//{value}'
    return to_send_string


def read_arduino_data(SECS):
    global i
    for _ in range(SAMPLES_SENT):
        time.sleep(0.1)
        timestamp_list.append(datetime.utcnow())
        if SECS < 10 or 13<=SECS<=22 or 35<=SECS<=44 or 48<=SECS:
            pitch = "15"
            height = "15"
            roll = "15"
            speed = "3"
        elif 10<=SECS<=12: #alarmas automaticas
            pitch = "80"
            height = "80"
            roll = "80"
            speed = "10"
        elif 23<=SECS<=25: #alarma manual altura
            pitch = "15"
            height = "25"
            roll = "15"
            speed = "3"
        elif 26<=SECS<=28: #alarma manual speed
            pitch = "15"
            height = "15"
            roll = "15"
            speed = "50"
        elif 29<=SECS<=31: #alarma manual pitch
            pitch = "25"
            height = "15"
            roll = "15"
            speed = "3"
        elif 32<=SECS<=34: #alarma manual roll
            pitch = "15"
            height = "15"
            roll = "25"
            speed = "3"
        elif 45<=SECS<=47: #avisos
            pitch = "18"
            height = "18"
            roll = "18"
            speed = "23"
        pitch_list.append(pitch)
        roll_list.append(roll)
        height_list.append(height)
        lat = str(41.23282-(0.001*i))
        lon = str(-9.72264+(0.001*i))
        i=i+1
        latitude_list.append(lat)
        longitude_list.append(lon)
        speed_list.append(speed)

def reset_lists():
    timestamp_list.clear()
    height_list.clear()
    pitch_list.clear()
    roll_list.clear()
    speed_list.clear()
    latitude_list.clear()
    longitude_list.clear()

if __name__ == '__main__':

    thread_subscriber = threading.Thread(target = mqtt_client_subscriber, daemon = True)

    thread_subscriber.start()
    mqtt_client_publisher()
import paho.mqtt.client as mqtt
import time
from datetime import datetime
import time
import sys
import serial
import threading

BROKER_IP = 'localhost'
TOPIC = 'solar_sensor'
VALUE_SEPARATOR = '%'
SAMPLES_SENT = 10
TOPIC_ALARMAS = 'server_alarm'

timestamp_list = []
height_list = []
pitch_list = []
roll_list = []
speed_list = []
latitude_list = []
longitude_list = []
i=0

client = mqtt.Client("solarboat", clean_session=True, transport="tcp")
client.username_pw_set("solarboat", password="solarboat")
client.connect(BROKER_IP)
paqueteAlarma=0
datosAlarmaTimestamps=[]
def mqtt_client_publisher():
    SECS = 0
    print("LOOP P")
    paquete=0
    while True:
        reset_lists()
        read_arduino_data(SECS)
        SECS = SECS +1
        if SECS == 51:
            SECS=0
        client.publish(TOPIC, f'{format_mqtt_data()}', qos=0)

def mqtt_client_subscriber():
    client.on_message = on_message
    client.subscribe(TOPIC_ALARMAS)
    print("LOOP S")
    client.loop_forever()


def on_message(client, userdata, msg):
    global paqueteAlarma
    print((datetime.utcnow()-datosAlarmaTimestamps[paqueteAlarma]))
    paqueteAlarma=paqueteAlarma+1
    print(msg)



def check_data_len():
    lens = [len(timestamp_list),len(height_list),len(pitch_list),len(roll_list),len(speed_list),len(latitude_list),len(longitude_list)]
    print(lens)
    for l in lens:
        if l != 10:
            print("LENGTH ERROR")


def print_ardunio_data():
    for i in range(len(timestamp_list)):
        print(f'{timestamp_list[i]}:')
        print(f'height: {height_list[i]}')
        print(f'pitch: {pitch_list[i]}')
        print(f'roll: {roll_list[i]}')
        print(f'speed: {speed_list[i]}')
        print(f'latitude: {latitude_list[i]}')
        print(f'longitude: {longitude_list[i]}')

def format_mqtt_data():
    to_send_string = ''
    for i in range(len(timestamp_list)):
        value = f'{timestamp_list[i]}%{height_list[i]}%{pitch_list[i]}%{roll_list[i]}%{speed_list[i]}%{latitude_list[i]}%{longitude_list[i]}'
        if i == 0:
            to_send_string = value
        else:
            to_send_string += f'//{value}'
    return to_send_string


def read_arduino_data(SECS):
    global i, datosAlarmaTimestamps
    for _ in range(SAMPLES_SENT):
        time.sleep(0.1)
        timestamp_list.append(datetime.utcnow())
        if SECS < 10 or 13<=SECS<=22 or 35<=SECS<=44 or 48<=SECS:
            pitch = "15"
            height = "15"
            roll = "15"
            speed = "3"
        elif 10<=SECS<=12: #alarmas automaticas
            pitch = "80"
            height = "80"
            roll = "80"
            speed = "10"
            datosAlarmaTimestamps.append(datetime.utcnow())
        elif 23<=SECS<=25: #alarma manual altura
            pitch = "15"
            height = "25"
            roll = "15"
            speed = "3"
            datosAlarmaTimestamps.append(datetime.utcnow())
        elif 26<=SECS<=28: #alarma manual speed
            pitch = "15"
            height = "15"
            roll = "15"
            speed = "50"
            datosAlarmaTimestamps.append(datetime.utcnow())
        elif 29<=SECS<=31: #alarma manual pitch
            pitch = "25"
            height = "15"
            roll = "15"
            speed = "3"
            datosAlarmaTimestamps.append(datetime.utcnow())
        elif 32<=SECS<=34: #alarma manual roll
            pitch = "15"
            height = "15"
            roll = "25"
            speed = "3"
            datosAlarmaTimestamps.append(datetime.utcnow())
        elif 45<=SECS<=47: #avisos
            pitch = "18"
            height = "18"
            roll = "18"
            speed = "23"
        pitch_list.append(pitch)
        roll_list.append(roll)
        height_list.append(height)
        lat = str(41.23282-(0.001*i))
        lon = str(-9.72264+(0.001*i))
        i=i+1
        latitude_list.append(lat)
        longitude_list.append(lon)
        speed_list.append(speed)

def reset_lists():
    timestamp_list.clear()
    height_list.clear()
    pitch_list.clear()
    roll_list.clear()
    speed_list.clear()
    latitude_list.clear()
    longitude_list.clear()

if __name__ == '__main__':

    thread_subscriber = threading.Thread(target = mqtt_client_subscriber, daemon = True)

    thread_subscriber.start()
    mqtt_client_publisher()