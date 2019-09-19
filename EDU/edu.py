#!/usr/bin/env python3

# *********************************************************************************
# This is the Events Detector Unit (EDU)
# It is intended to detect different Events of Interest (EI), processing them as
# Events Report (ER). ER are transmitted to the Emergency Processor Unit (EPU).
# This implementation is based on the CityAlarm paper
# Author      : Daniel G. Costa
# E-mail      : danielgcosta@uefs.br
# Date        : 2019/09/01
# *********************************************************************************

## Basic modules and libraries
import datetime, time
import threading
import atexit
import socket
import math
import sys, getopt
import grovepi  #Has to be installed

## Elements to support the operation of the EDU
from elementsEDU import ListEI,EI,ER
import moduleGPS

########################################################
debug = True  #Used to present trace messages on the screen

## Variables and constants
idEDU = 1 #ID of the EDU (variable u). It can be provided as command-line options
fs = 5 #Sensing frequency in seconds
fx = 60 #Transmission frequency to refresh Events Reports
la = 0 #Latitude of the EDU
lo = 0 #Longitude of the EDU
events = ListEI() #List of all possible EI (both detected and undetected)
idER = 1 #Indicates the current id of generated Events Reports

## Communication with the Emergency Processor Unit (EPU)
## They can be provided as command-line options
ipEPU = "192.168.0.140" #EPU address
portEPU = 55055         #EPU port

###############################################
## List of possible EI
## The detection of these EI depends on the empoyed sensor devices
## These definitions are based on Table 1 of the CityAlarm paper
## The format is [type,threshold,symbol(1 for >= and 0 for <=),textual description]
possibleEI = [[1,60,1,"Heating"], \
              [2,-20,0,"Freezing"], \
              [3,10,0,"Humidty"], \
              [4,500,1,"Smoke"], \
              [5,35,1,"Gas"], \
              [6,10,1,"Rain"], \
              [7,6.5,1,"Earhquake"], \
              [8,50,1,"Noise"], \
              [9,300,1,"Radiation"], \
              [10,5,1,"BlastWave"], \
              [11,80,1,"Wind"], \
              [12,1,0,"Luminosity"], \
              [13,50,1,"Snowing"], \
              [14,95,1,"DamLevel"], \
              [15,600,1,"Pollution"], \
              [16,0,0,"Flooding"]]

#####################################################
## This part will depend on the employed hardware components
## This referece implementation of the EDU is based on the
## GrovePi+ platform
#####################################################

## List of sensor devices: Grove Ports
sensorAudio = 0 #analog A0
sensorSmoke = 1 #analog A1
sensorTemperature = 2 #analog A2
sensorWater = 4 #digital D4
sensorHumidity = 7 # Digital D7
display = 8 #Numerical display to show the number of detected events: D8

grovepi.pinMode (sensorAudio,"INPUT")
grovepi.pinMode (sensorSmoke,"INPUT")
grovepi.pinMode (sensorTemperature,"INPUT")
grovepi.pinMode (sensorWater,"INPUT")
grovepi.pinMode (sensorHumidity,"INPUT")
grovepi.pinMode (display,"OUTPUT")

#####################################################
### MAIN CODE ###
#####################################################

## Thread 1 - transmit an ER every fs seconds
## This thread senses the environment and transmits the generated ER
class sensingThread (threading.Thread):
    global fs, events
        
    def __init__(self):
        threading.Thread.__init__(self)
      
    def run(self):
                
        currentEI = 0 # This variable is used to avoid the transmission of multiple ER for the same set of detected EI
        
        while True:
            try:                
                ## Check all connected sensors
                
                ## Only humidity is taken from DHT11, since the detectable temperature range is short
                [temp,humidity] = grovepi.dht(sensorHumidity,0) #0 because the component is the "blue" one; 1 is for the "white" (DHT22) sensor
                noise = grovepi.analogRead(sensorAudio)
                noise = 20 * math.log(noise,10) #Simple simplification to return value in dB (approximation, since the sensor is not calibrated)
                smoke = grovepi.analogRead(sensorSmoke) #MQ-2 reading (is also needs calibration)
                water = grovepi.digitalRead(sensorWater) #Returns 1 if it is dry, and 0 otherwise
                temperature = grovepi.temp(sensorTemperature, '1.2') #This sensor has a better temperature range
                
                if debug:
                    print ("\nSensed data at", datetime.datetime.today())
                    print ("Relative humidity:", humidity, "%")
                    print ("Noise:", noise, "dB")
                    print ("Smoke:", smoke, "ppm")
                    if water == 1:
                        print ("Water:", water, "- It is dry.")
                    else:
                        print ("Water:", water, "- It is wet.")   
                    print ("Temperature:", temperature, "C")
                
                ## Test if any EI was detected.
                ## The sensors are mapped to the corresponding value of Y
                detectEI(humidity,events.getEventY(3))
                detectEI(noise,events.getEventY(8))
                detectEI(smoke,events.getEventY(4))
                detectEI(water,events.getEventY(16))
                ## Temperature is related to two EI (Heating and Freezing)
                detectEI(temperature,events.getEventY(1))
                detectEI(temperature,events.getEventY(2))
                               
                ## If debug=False, only the LCD display will show information about detected events 
                showDetectedEI()
                
                ## In this thread, a new ER is sent only when the current status of detected
                ## events is chaged
                if events.getNumberDetectedEI() == 0:
                    currentEI = 0
                elif events.getNumberDetectedEI() > 0 and currentEI != events.getNumberDetectedEI():
                    if debug:
                        print ("A new EI was detected. An ER will be created...")
                    currentEI = events.getNumberDetectedEI()
                    createER(self)
                                
            except (IOError, TypeError) as e:
                print (str(e))
            
            ## Frequency of monitoring
            time.sleep (fs)

##########################################################################
            
## Second thread - transmit an ER every fx seconds
## This thread creates an ER with already detected EI
class refreshThread (threading.Thread):
    global fx, events
    
    def __init__(self):
        threading.Thread.__init__(self)
      
    def run(self):
        while True:
            ## It has to sleep first, making this more reasonable for refreshing            
            time.sleep (fx)
            
            try:
                ## It must not refresh an ER when there is no detected event
                if events.getNumberDetectedEI() > 0:
                    if debug:
                        print ("\nRefreshing the transmission of ER having", events.getNumberDetectedEI(), "events detected.")
                    createER(self)
                    
            except (IOError, TypeError) as e:
                print (str(e))
            
###########################################################################
        
## This method checks if a certain EI can be assumed as detected
def detectEI(sensed, event):    
    
    threshold = event.getThreshold()
    symbol = event.getMath()
    
    if symbol == 1:
        if sensed >= threshold: # EI detected
            event.setDetected()
        else:            
            event.setUndetected() # EI is undetected
    else:
        if sensed <= threshold: # EI detected
            event.setDetected()                
        else:            
            event.setUndetected() # EI is undetected

##########################################################################

def showDetectedEI():
    global events
    for event in events.getEvents():
        if event.isDetected():
            if debug:
                print ("*** EI ", event.getType(), " is detected ***")
    
    showDisplayNumberEI() # Uses the display
    
##########################################################################
    
def showDisplayNumberEI():
    global events, display
    grovepi.fourDigit_number(display, events.getNumberDetectedEI(), 1)
    
##########################################################################
    
## This method creates the Events Reports
## This method is accessed by two concurrent threads
def createER(self):        
    global idEDU, idER, la, lo, events
        
    ## Requesting block for the use of this method
    lock = threading.Lock()
    lock.acquire()
    
    ## Current time
    timestamp = time.ctime()
    
    eventsReport = ER(idEDU, idER, timestamp, la, lo)
    idER = idER + 1
    
    ## Insert events. The limit is 5 EI, as described in CityAlam paper
    countEI = 0
    for event in events.getEvents():
        if event.isDetected():
            countEI = countEI + 1
            if countEI <= 5:                
                eventsReport.putEventType (event.getType()) # Only the value of Y is relevant
    
    if countEI > 5:
        if debug:
            print ("More than 5 EI were detected, but only 5 events will be reported.")
        
    ## Send the ER to the EPU
    transmitER (eventsReport)
    
    ## Releasing this method to be used by other thread
    lock.release()

##########################################################################
    
## Communication with the EPU
def transmitER(er):
    global debug, ipEPU, portEPU
    
    if debug:
        print ("Transmitting ER generated at " + str(er.getTimestamp()) + ". Number of reported EI: " + str(er.getNumberEI()))
        
    ## Serializing the ER to the JSON format
    jsonER = er.toJSON()
    
    if debug:
        print ("\nER in the JSON format:")
        print (jsonER)
    
    ## Open connection to the EPU, send ER, and then close the connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    try:
        s.settimeout(10) # Timeout of 10 seconds
        s.connect((ipEPU, portEPU))
        
        if debug:
            print ("\nConnection established to the EPU. Sending ER...")
        
        s.sendall(bytes(jsonER, 'utf-8'))
        s.close()
        
    except socket.error as e:
        print ("The EPU could not be contacted. Exiting EDU...")
        print ("Error:", e)
        sys.exit(1)
        
##########################################################################
      
## Initiliaze all Events of Interest
def initializeEI(): 
    global events, possibleEI
    
    for ei in possibleEI:
        events.putEvent(ei[0],ei[1],ei[2],ei[3])
    
    if debug:
        print ("\nList of configured Events of Interest:")
        events.printValues()

##########################################################################
 
## Called when program exits
def exit_handler():
    if debug:
        print ("Events Detector Unit is exiting...")
    sys.exit(0)
    
##########################################################################    

# main code of the EDU      
def main(argv):
    global display, la, lo, debug, idEDU, ipEPU, portEPU
    
    ## Parse arguments from the command-line
    ## Options: debug idU ipEPU portEPU
    opts, ars = getopt.getopt(argv,"hd:u:i:p:",["debug=","idEDU=","ipEPU=","portEPU="])
    for opt,arg in opts:
        if opt == "-h":
            print ("edu.py -d <debug> -u <idEDU> -i <ipEPU> -p <portEDU>")
            sys.exit(1)
        elif opt in ("-d", "--debug"):
            if arg == "True":
                debug = True                
            else:
                debug = False
        elif opt in ("-u", "--idEDU"):
            idEDU = arg
        elif opt in ("-i", "--ipEPU"):
            ipEPU = arg
        elif opt in ("-p", "--portEPU"):
            portEPU = int(arg)
    ########            
    
    print ("Events Detector Unit is initializing... Ready to detect events.")
    
    ## Initialize display
    grovepi.fourDigit_init(display)
    grovepi.fourDigit_brightness(display,6)
    time.sleep(.2)
    showDisplayNumberEI()
    
    ## Get GPS location - only once at startup
    if debug:
        print("Obtaining GPS position...")
    gps = moduleGPS.groveGPS()    
    gps.read()
    la = gps.latitude
    lo = gps.longitude
    if debug:
        print ("EDU at latitude =", la, "and longitude =", lo)
    
    ## Initialize EI definitions
    initializeEI()    

    ## Initialize thread to read all the sensors
    checkSensors = sensingThread()    
    checkSensors.start()
    
    ## Initialize thread to refresh ER
    refreshER = refreshThread()    
    refreshER.start()
    
    atexit.register(exit_handler)

if __name__ == '__main__':
    main(sys.argv[1:])
