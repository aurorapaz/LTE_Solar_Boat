import paho.mqtt.client as mqtt
from datetime import datetime
import time, sys, random

SERVER_IP = 'localhost'
TOPIC = 'solar_sensor'
TOPIC_ALARMAS = 'server_alarm'
VALUE_SEPARATOR = '%'
SAMPLES_SENT = 10

timestamp_list = []
height_list = []
pitch_list = []
roll_list = []
speed_list = []
latitude_list = []
longitude_list = []

alarm_number = 0
send_instants = []

def mqtt_client():
    client = mqtt.Client("solarboat", clean_session=True, transport="tcp")
    client.username_pw_set("solarboat", password="solarboat")
    client.connect(SERVER_IP)
    client.on_message = on_message
    client.subscribe(TOPIC_ALARMAS)
    client.loop_start()

    while True:
        #reset_lists()
        read_arduino_data()
        #print_ardunio_data()
        send_instants.append(datetime.utcnow())
        client.publish(TOPIC, f'{format_mqtt_data()}', qos=0)
        


def check_data_len():
    lens = [len(timestamp_list),len(height_list),len(pitch_list),len(roll_list),len(speed_list),len(latitude_list),len(longitude_list)]
    print(lens)
    for l in lens:
        if l != 10:
            print("LENGTH ERROR")

def on_message(client, userdata, msg):
    global alarm_number
    print((datetime.utcnow()-send_instants[alarm_number]))
    alarm_number = alarm_number + 1


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
    

def read_arduino_data():
    for _ in range(SAMPLES_SENT):
        time.sleep(0.1)
        timestamp_list.append(datetime.utcnow())
        pitch = "50"
        roll = "0.2" 
        height = "5" 
        #pitch = "20"
        #roll = "10"
        pitch_list.append(pitch)
        roll_list.append(roll)
        #height = "15"
        height_list.append(height)
        lat = "24.80"
        lon = "10.18"
        speed = "5"
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
    mqtt_client()
