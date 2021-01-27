import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
import time
from flask_socketio import SocketIO
import messages.alerts as alerts

SERVER_IP = 'localhost'
TOPIC = 'solar_sensor'
DATABASE = 'SolarBoat'


influx = InfluxDBClient(host='localhost', port=8086)
#influx.drop_database(DATABASE)
#influx.create_database(DATABASE)
influx.switch_database(DATABASE)


def mqtt_client(socketio):
    global socket
    socket=socketio
    client = mqtt.Client("server", clean_session=True, transport="tcp")
    client.username_pw_set("server", password="solarboat")
    client.connect(SERVER_IP)
    client.on_message = on_message

    #init alarm status dict
    global status
    status = dict()
    for key in ["altura","pitch","roll","speed"]:
        status[key] = [{'alert_message': 'All normal'}, datetime.now()]

    client.subscribe(TOPIC)
    client.loop_forever()

def on_message(client, userdata, msg):
    print("NEW MESSAGE:")
    try:
        sensor_data = get_json_body(msg.payload.decode('utf-8'))
    except Exception:
        print("INVALID MESSAGE DISCARTED")
        return
    save_data(sensor_data)
    alerts.check_alarm(status,socket)
    print("")

def get_json_body(payloads):
    pay = payloads.split('//')
    json_body = []
    for p in pay:
        my_json = mqtt_to_json(p)
        json_body.append(my_json)
    return json_body


def mqtt_to_json(payload):
    timestamp, height, pitch, roll, speed, latitude, longitude = payload.split('%')
    json_body = {
        "measurement": TOPIC,
        "tags": {
            "host": "local"
        },
        "time": timestamp,
        "fields": {
            "height": float(height),
            "pitch": float(pitch),
            "roll": float(roll),
            "speed": float(speed),
            "latitude": float(latitude),
            "longitude": float(longitude)
        }
    }

    return json_body


def save_data(sensor_data):
    influx.write_points(sensor_data)

