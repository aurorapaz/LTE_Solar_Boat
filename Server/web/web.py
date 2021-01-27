from flask import Flask, render_template, jsonify, request
from flask_cors import cross_origin
from flask_socketio import SocketIO,emit
import os
import messages.alerts as alerts
import threading
import iot_server
from influxdb import InfluxDBClient

DATABASE = 'SolarBoat'

app = Flask(__name__)
socketio =  SocketIO(app,cors_allowed_origins='*')
thread_launched = False

def mqtt_comm():
    iot_server.mqtt_client(socketio)

@socketio.on('SEND_ACTION')
def send_action(message):
    alerts.send_alert(message)

@socketio.on('CUSTOM_ACTION')
def custom_action(message):
    print("Sendig custom message")
    alerts.send_alert(message)

@socketio.on('connect')
def test_connect():
    global thread_client
    global thread_launched
    if thread_launched == True:
        print("Thread is still alive")
    else:
        print("New Thread, any Thread alive")
        thread_client = threading.Thread(target = mqtt_comm, daemon=True)
        thread_client.start()
        thread_launched = True

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)


