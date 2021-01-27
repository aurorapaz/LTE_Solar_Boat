###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

from time import sleep
import rticonnextdds_connector as rti
import serial

with rti.open_connector(
        config_name="MyParticipantLibrary::MyPubParticipant",
        url="./../SolarBoatExample.xml") as connector:

    if __name__ == '__main__':
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.flush()

    output_altura = connector.get_output("MyPublisher::MyAlturaWriter")
    output_gps = connector.get_output("MyPublisher::MyGPSWriter")
    output_imu = connector.get_output("MyPublisher::MyIMUWriter")

    #Podria esperarse a tener subscribers para publicar
    #print("Waiting for subscriptions...")
    #output.wait_for_subscriptions()

    print("Publicando...")

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line.startswith('Pitch:'):
                pitch = line.split('Pitch: ')[1]
                output_imu.instance.set_number("pitch", pitch)
            if line.startswith('Roll:'):
                roll = line.split('Roll: ')[1]
                output_imu.instance.set_number("roll", roll)
            if line.startswith('Altura:'):
                height = line.split(' ')[1]
                output_imu.instance.set_number("height", height)
            if line.startswith('$'):
                output_gps.instance.set_string("gps_data", "GPS = "+line)
            output_altura.write()
            output_gps.write()
            output_imu.write()
            sleep(0.5) # Se publica cada 0.5 seconds

    # Espera a que todas las subscripciones reciban los datos antes de salir
    #output_altura.wait()
    #output_gps.wait()
    #output_imu.wait()
