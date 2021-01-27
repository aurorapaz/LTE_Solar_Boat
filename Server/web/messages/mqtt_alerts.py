import paho.mqtt.client as mqtt

BROKER_IP = '127.0.0.1'
TOPIC_ALARMAS = 'server_alarm'

client = mqtt.Client("server2", clean_session=True, transport="tcp")
client.username_pw_set("server", password="solarboat")
client.connect(BROKER_IP)


def enviar_alarma(cadena_alarma):
    print(cadena_alarma)
    client.publish(TOPIC_ALARMAS, cadena_alarma, qos=0)
    print("--> ALERT SENT!!!!!!!!!!!")
