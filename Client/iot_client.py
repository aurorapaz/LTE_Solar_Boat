import paho.mqtt.client as mqtt
import time
from datetime import datetime
import time
import sys
import serial
import threading

BROKER_IP = 'solarboat.ddns.net'
BROKER_PORT = 1883
TOPIC = 'solar_sensor'
TOPIC_ALARMAS = 'server_alarm'
VALUE_SEPARATOR = '%'
SAMPLES_SENT = 10

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.flush()

timestamp_list = []
height_list = []
pitch_list = []
roll_list = []
speed_list = []
latitude_list = []
longitude_list = []

client = mqtt.Client("solarboat2", clean_session=True, transport="tcp")
client.username_pw_set("solarboat", password="solarboat")
client.connect(BROKER_IP, BROKER_PORT)

def mqtt_client_publisher():
    while True:
        reset_lists()
        read_arduino_data()
        print_ardunio_data()
        client.publish(TOPIC, f'{format_mqtt_data()}', qos=0)

def mqtt_client_subscriber():
    client.on_message = on_message
    client.subscribe(TOPIC_ALARMAS)
    client.loop_forever()

def on_message(client, userdata, msg):
    print("{}: {}".format(msg.topic, msg.payload))

def print_ardunio_data():
    try:
        for i in range(len(timestamp_list)):
            print(f'{timestamp_list[i]}:')
            print(f'height:{height_list[i]}')
            print(f'pitch:{pitch_list[i]}')
            print(f'roll:{roll_list[i]}')
            print(f'speed:{speed_list[i]}')
            print(f'latitude:{latitude_list[i]}')
            print(f'longitude:{longitude_list[i]}')
    except Exception:
        pass

def format_mqtt_data():
    try:
        to_send_string = ''
        for i in range(len(timestamp_list)):
            value = f'{timestamp_list[i]}%{height_list[i]}%{pitch_list[i]}%{roll_list[i]}%{speed_list[i]}%{latitude_list[i]}%{longitude_list[i]}'
            if i == 0:
                to_send_string = value
            else:
                to_send_string += f'//{value}'
        return to_send_string
    except Exception:
        pass


def read_arduino_data():
    for _ in range(SAMPLES_SENT * 3):
        ser.flush()
        line = ser.readline().rstrip()
        line = str(line)[2:-1]
        if line.startswith('P'):
            try:
                pitch = line.split(' ')[1]
                roll = line.split(' ')[3]
                if(float(pitch) != -10000000.00 and float(roll) != -10000000.00):
                    pitch_list.append(pitch)
                    roll_list.append(roll)
                    timestamp_list.append(datetime.utcnow())
            except Exception:
                print("LINEA MAL FORMADA: " + line)

        elif line.startswith('H'):
            try:
                height = line.split(' ')[1]
                if(float(height) != -10000000.00):
                    height_list.append(height)
            except Exception:
                print("LINEA MAL FORMADA: " + line)
            
        elif line.startswith('S'):
            try:
                speed = line.split(' ')[1]
                lat = line.split(' ')[3]
                lon = line.split(' ')[5]
                float(speed)
                float(lat)
                float(lon)
                speed_list.append(speed)
                latitude_list.append(lat)
                longitude_list.append(lon)
            except Exception:
                print("LINEA MAL FORMADA: " + line)
        else:
            print("LINEA MAL FORMADA: " + line)


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
