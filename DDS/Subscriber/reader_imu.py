###############################################################################
# (c) 2005-2015 Copyright, Real-Time Innovations.  All rights reserved.       #
# No duplications, whole or partial, manual or electronic, may be made        #
# without express written permission.  Any such copies, or revisions thereof, #
# must display this notice unaltered.                                         #
# This code contains trade secrets of Real-Time Innovations, Inc.             #
###############################################################################

from __future__ import print_function
import rticonnextdds_connector as rti

with rti.open_connector(
    config_name="MyParticipantLibrary::MySubParticipant",
    url="./../SolarBoatExample.xml") as connector:

    #Se crea un nuevo Connector pasándole el XML y el nombre de configuración
    input = connector.get_input("MySubscriber::MyIMUReader")

    print("Esperando publicación...")
    input.wait_for_publications() # espera a alguna publicación

    print("Esperando los datos...")
    for i in range(1, 500):
        input.wait() # espera por los datos del input
        input.take()
        for sample in input.samples.valid_data_iter:
            # Se extraen todos los campos con get_dictionary()
            data = sample.get_dictionary()
            pitch = data['pitch']
            roll = data['roll']

            # También se puede acceder individualmente a los campos
            #gps = sample.get_string("gps_data")
            print("Info recibida de la IMU: picth = " + repr(pitch) + " || roll = " + repr(roll))
