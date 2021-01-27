import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from datetime import datetime
import time

SERVER_IP = 'localhost'
TOPIC = 'solar_sensor'
DATABASE = 'SolarBoat'


influx = InfluxDBClient(host='localhost', port=8086)
#influx.drop_database(DATABASE)
#influx.create_database(DATABASE)
influx.switch_database(DATABASE)

def mqtt_client():
    client = mqtt.Client("server", clean_session=True, transport="tcp")
    client.username_pw_set("server", password="solarboat")
    client.connect(SERVER_IP)
    client.on_message = on_message

    client.subscribe(TOPIC)
    client.loop_forever()


def on_message(client, userdata, msg):
    print("Topic {}: {}".format(msg.topic,msg.payload))
    #print(datetime.utcnow())
    sensor_data = get_json_body(msg.payload.decode('utf-8'))
    save_data(sensor_data)



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
            "height": int(height),
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



if __name__ == '__main__':
    mqtt_client()
