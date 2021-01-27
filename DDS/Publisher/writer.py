###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

from time import sleep
import rticonnextdds_connector as rti

with rti.open_connector(
        config_name="MyParticipantLibrary::MyPubParticipant",
        url="./../SolarBoatExample.xml") as connector:

    output_altura = connector.get_output("MyPublisher::MyAlturaWriter")
    output_gps = connector.get_output("MyPublisher::MyGPSWriter")
    output_imu = connector.get_output("MyPublisher::MyIMUWriter")

    #Podria esperarse a tener subscribers para publicar
    #print("Waiting for subscriptions...")
    #output.wait_for_subscriptions()

    print("Publicando...")
    #Probar a enviar 100 iteraciones de datos simulados: habrá que sustituir esto por el código de lectura del Arduino
    for i in range(1, 100):
        output_altura.instance.set_number("height", i)
        output_gps.instance.set_string("gps_data", "GPS = "+str(i*2))
        output_imu.instance.set_number("pitch", 30)
        output_imu.instance.set_number("roll", 50)
        output_altura.write()
        output_gps.write()
        output_imu.write()

        sleep(0.5) # Se publica cada 0.5 seconds

    print("Exiting...")
    # Espera a que todas las subscripciones reciban los datos antes de salir
    output_altura.wait()
    output_gps.wait()
    output_imu.wait()
