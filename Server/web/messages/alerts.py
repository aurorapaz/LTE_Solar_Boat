from influxdb import InfluxDBClient
import messages.speed_messages as speed_messages
import messages.pitch_messages as pitch_messages
import messages.roll_messages as roll_messages
import messages.heigth_messages as heigth_messages
import messages.mqtt_alerts as mqtt_alerts

from datetime import datetime, timedelta

influx = InfluxDBClient(host='localhost', port=8086, database="SolarBoat")

MIN_ALARM_REPEAT_INTERVAL = 12

def check_alarm(status,socket):
    status["altura"][0]=check_altura(30, 20)
    status["pitch"][0]=check_pitch(30, 20)
    status["roll"][0]=check_roll(30, 20)
    status["speed"][0]=check_speed(10, 25, 20)

    for key,value in status.items():
        #ALARMAS
        if value[0]['alert_message'].startswith("Alarma") or (not value[0]['notification_message'].startswith("All normal")):
            if isValidAlarm(value[1]):
                print("ENVIA ALARMA")
                value[1] = datetime.now()
                socket.emit('ALARMA',data=value[0])
                if value[0]['alert_message'].startswith("Alarma automatica"):
                    send_alert(value[0]["alert_message"])


def isValidAlarm(lastAlarmTimestamp):
    valid = lastAlarmTimestamp < (datetime.now() - timedelta(seconds=MIN_ALARM_REPEAT_INTERVAL))
    return valid   

def check_altura(automatic_limit, manual_limit):
    return heigth_messages.get_messages(automatic_limit, manual_limit, influx)

def check_pitch(automatic_limit, manual_limit):
    return pitch_messages.get_messages(automatic_limit, manual_limit, influx)

def check_roll(automatic_limit, manual_limit):
    return roll_messages.get_messages(automatic_limit, manual_limit, influx)

def check_speed(automatic_limit, manual_limit, warning_limit):
    return speed_messages.get_messages(automatic_limit, manual_limit, warning_limit, influx)

def send_alert(message):
    mqtt_alerts.enviar_alarma(message)
