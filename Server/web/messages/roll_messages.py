from influxdb import InfluxDBClient
import sys
from datetime import datetime
import time

last_avg_roll = 0.0

def get_messages(automatic_limit, manual_limit, influx):
    avg_roll = 0

    result = influx.query('SELECT mean(roll) FROM solar_sensor WHERE time > now() - 1s')
    points = result.get_points()
    for item in points:
        avg_roll = item["mean"]

    print("AVG_ROLl: " + str(avg_roll))

    alert_message = get_alert(avg_roll, automatic_limit, manual_limit)
    notification_message = get_notification(avg_roll)

    messages = {"alert_message" : alert_message, "notification_message": notification_message}
    return messages


def get_alert(avg_roll, automatic_limit, manual_limit):
    alert_message = ""
    if(avg_roll > automatic_limit):
        alert_message = "Alarma automatica de roll. Roll medio actualmente: " + str(avg_roll)
    elif(avg_roll > manual_limit):
        alert_message = "Alarma manual de roll. Roll medio actualmente: " + str(avg_roll)
    else:
        alert_message = "All normal"
    return alert_message


def get_notification(avg_roll):
    notification_message = ""
    global last_avg_roll
    if(avg_roll > 1.1*last_avg_roll or avg_roll < 0.9*last_avg_roll):
        notification_message = "Roll: " + str(avg_roll) + " Roll previo: " + str(last_avg_roll)
    else:
        notification_message = "All normal"
    last_avg_roll = avg_roll
    return notification_message
