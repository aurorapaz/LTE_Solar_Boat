from influxdb import InfluxDBClient
import sys
from datetime import datetime
import time

last_avg_pitch = 0.0

def get_messages(automatic_limit, manual_limit, influx):
    avg_pitch = 0

    result = influx.query('SELECT mean(pitch) FROM solar_sensor WHERE time > now() - 1s')
    points = result.get_points()
    for item in points:
        avg_pitch = item["mean"]

    alert_message = get_alert(avg_pitch, automatic_limit, manual_limit)
    notification_message = get_notification(avg_pitch)

    messages = {"alert_message" : alert_message, "notification_message": notification_message}
    return messages


def get_alert(avg_pitch, automatic_limit, manual_limit):
    alert_message = ""
    if(avg_pitch > automatic_limit):
        alert_message = "Alarma automatica de pitch. Pitch medio actualmente: " + str(avg_pitch) 
        #alert_message = "Alarma automatica " + str(datetime.utcnow()) 
    elif(avg_pitch > manual_limit):
        alert_message = "Alarma manual de pitch. Pitch medio actualmente: " + str(avg_pitch)
    else:
        alert_message = "All normal"
    return alert_message


def get_notification(avg_pitch):
    notification_message = ""
    global last_avg_pitch
    print("LAST_AVG_PITCH: " + str(last_avg_pitch))
    print("AVG_PITCH: " + str(avg_pitch))
    if(avg_pitch > 1.1*last_avg_pitch or avg_pitch < 0.9*last_avg_pitch):
        notification_message = "Pitch: " + str(avg_pitch) + " Pitch previo: " + str(last_avg_pitch)
    else:
        notification_message = "All normal"

    last_avg_pitch = avg_pitch
    return notification_message
