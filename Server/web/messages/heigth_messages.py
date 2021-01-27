from influxdb import InfluxDBClient
import sys
from datetime import datetime
import time

last_avg_heigth = 0.0

def get_messages(automatic_limit, manual_limit, influx):
    avg_heigth = 0

    result = influx.query('SELECT mean(height) FROM solar_sensor WHERE time > now() - 1s')
    #result = influx.query('SELECT mean(height) FROM solar_sensor ORDER BY time DESC LIMIT 10')
    points = result.get_points()
    for item in points:
        avg_heigth = item["mean"]

    print("AVG_HEIGTH: " + str(avg_heigth))

    alert_message = get_alert(avg_heigth, automatic_limit, manual_limit)
    notification_message = get_notification(avg_heigth)

    messages = {"alert_message" : alert_message, "notification_message": notification_message}
    return messages


def get_alert(avg_heigth, automatic_limit, manual_limit):
    alert_message = ""
    if(avg_heigth > automatic_limit):
        alert_message = "Alarma automatica de altura. Altura media actualmente: " + str(avg_heigth)
    elif(avg_heigth > manual_limit):
        alert_message = "Alarma manual de altura. Altura media actualmente: " + str(avg_heigth)
    else:
        alert_message = "All normal"
    return alert_message

def get_notification(avg_heigth):
    notification_message = ""
    global last_avg_heigth
    if(avg_heigth > 1.1*last_avg_heigth or avg_heigth < 0.9*last_avg_heigth):
        notification_message = "Aviso de altura: " + str(avg_heigth)
    else:
        notification_message = "All normal"
    last_avg_heigth = avg_heigth
    return notification_message
