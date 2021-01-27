from influxdb import InfluxDBClient
import sys
from datetime import datetime
import time 

def get_messages(automatic_limit, manual_limit, warning_limit, influx):
    avg_speed = 0

    result = influx.query('SELECT mean(speed) FROM solar_sensor WHERE time > now() - 1s')
    points = result.get_points() 
    for item in points:
        avg_speed = item["mean"]

    print("AVG_SPEED: " + str(avg_speed))

    alert_message = get_alert(avg_speed, manual_limit, automatic_limit)
    notification_message = get_notification(warning_limit, avg_speed, manual_limit)

    messages = {"alert_message" : alert_message, "notification_message": notification_message}
    return messages

def get_alert(avg_speed, manual_limit, automatic_limit):
    alert_message = ""
    if(avg_speed > manual_limit): 
        alert_message = "Alarma manual de velocidad. Velocidad media actualmente: " + str(avg_speed)
    elif(automatic_limit - 1 < avg_speed < automatic_limit + 1):
        alert_message = "Alarma automatica de velocidad. Velocidad media actualmente: " + str(avg_speed)
    else:
        alert_message = "All normal"
    return alert_message


def get_notification(warning_limit, avg_speed, manual_limit):
    notification_message = ""
    if(warning_limit < avg_speed < manual_limit):
        notification_message = "Velocidad media actualmente: " + str(avg_speed)
    else:
        notification_message = "All normal"
    return notification_message
