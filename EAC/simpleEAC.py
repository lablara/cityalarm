#!/usr/bin/env python3

# *********************************************************************
# This is a simple Emergency Alarm Client (EAC)
# It only shows the received EA in the JSON format
# This implementation is based on the CityAlarm paper
# Author      : Daniel G. Costa
# E-mail      : danielgcosta@uefs.br
# Date        : 2019/09/01
# *********************************************************************

import paho.mqtt.client as mqtt
from time import sleep
import sys, getopt
import atexit

## Constants and variables
debug = True
ipBroker = "127.0.0.1"

requestEA = "CityAlarm_EPU1"

#Main code of this EAC
###############################################################

#Called when program exits
def exit_handler():
    global debug
    
    if debug:
        print ("Emergency Alarm Client is exiting...")
        
###############################################################
        
def on_connect(client,userdata,flags,rc):
    global debug, ipBroker
    
    if debug:
        #print ("Connected to the MQTT Broker. Code:", rc)
        print ("Connected to the MQTT Broker:", ipBroker)
    
###############################################################

def on_disconnect(client,userdata,rc):
    global debug
    
    if debug:
        #print ("Disconnected from the MQTT Broker. Code:", rc)
        print ("Disconnected from the MQTT Broker")

###############################################################

def on_message(client,userdata,ea):
    print ("Received Emergency Alarm:")
    print (ea.payload.decode())
    
###############################################################

def main(argv):
    global requestEA,ipBroker, debug
        
    ## Parse arguments from the command-line
    ## Options: debug idU ipEPU portEPU
    opts, ars = getopt.getopt(argv,"hd:i:m:",["debug=","ipBroker=","requestEA="])
    for opt,arg in opts:
        if opt == "-h":
            print ("edu.py -d <debug> -i <ipBroker> -m <requestEA>")
            sys.exit(1)
        elif opt in ("-d", "--debug"):
            if arg == "True":
                debug = True                
            else:
                debug = False        
        elif opt in ("-i", "--ipBroker"):
            ipBroker = arg
        elif opt in ("-m", "--requestEA"):
            requestEA = arg
    ######## 
        
    if debug:
        print ("Initializig the EAC...")
    
    clientmqtt = mqtt.Client("")
    
    ## Basics MQTT configurations
    clientmqtt.on_connect = on_connect
    clientmqtt.on_disconnect = on_disconnect
    clientmqtt.on_message = on_message
    
    clientmqtt.connect(ipBroker)
        
    clientmqtt.subscribe(requestEA)
    if debug:
        print ("Subscribing to the MQTT Broker with topic:", requestEA)
    
    atexit.register(exit_handler)
    
    ## Keep receivig MQTT messages indefinetely
    clientmqtt.loop_forever()
    
###############################################################

if __name__ == '__main__':
    main(sys.argv[1:])
