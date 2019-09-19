# *********************************************************************
# This class received EA and send it to the requesting EAC
# It is implemented to communicate through the MQTT protocol
# Author      : Daniel G. Costa
# E-mail      : danielgcosta@uefs.br
# Date        : 2019/09/10
# *********************************************************************

import paho.mqtt.client as mqtt
from time import sleep

########################################################

class epuMQTT():
    def __init__(self, ipBroker, epuId):
        self.broker = ipBroker
        self.description = "CityAlarm_EPU" + str(epuId)

        self.clientmqtt = mqtt.Client("")

    def publishEA (self, eaJSON):

        print ("Broker address:", self.broker)
        self.clientmqtt.connect(self.broker)

        self.clientmqtt.publish (self.description, eaJSON)  # Associating a "topic" to a "payload"

        sleep(1)
        self.clientmqtt.disconnect()

        print("Publishing an Emergency Alarm to the MQTT Broker...")
