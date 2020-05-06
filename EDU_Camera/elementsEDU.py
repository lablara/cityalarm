# **************************************************
# Accessory classes for the EDU
# They model the concepts of Event of Interest and Events Report
# Author      : Daniel G. Costa
# E-mail      : danielgcosta@uefs.br
# Date        : 2019/09/01
# **************************************************

import json

## Models a list of all EI
class ListEI:   
    
    def __init__(self):
        self.events = []
    
    def putEvent(self, y, th, math, txt):
        ## math describes if the symbol is <= (0) or >= (1)
        event = EI(y, th, math, txt)
        self.events.append(event)        
    
    def removeEvent(self, event):
        self.events.remove(event)
    
    def getEvents (self):
        return self.events
    
    def getEventY (self, y):
        for event in self.events:
            if event.getType() == y:  #As the values of y are unique, there is only one answer here
                return event
    
    def getNumberDetectedEI(self):
        numberEI = 0
        for event in self.events:
            if event.isDetected():
                numberEI = numberEI + 1
        
        return numberEI
        
    def printValues(self):
        for event in self.events:
            if event.getMath() == 0:
                print ("Type:",  event.getType(),  ": Threshold =", event.getThreshold(), ": Symbol is <=. Description:", event.getDescription())
            else:
                print ("Type:",  event.getType(),  ": Threshold =", event.getThreshold(), ": Symbol is >=. Description:", event.getDescription())

## Models an Event of Interest
class EI:
    
    def __init__(self, idy, th, m, text):
        self.y = idy
        self.detected = False
        self.threshold = th
        self.math = m
        
        #this is not in CityAlarm paper, but it may help to "track" events
        self.description = text 

    def getType (self):
        return self.y
    
    def getThreshold (self):
        return self.threshold

    def getDescription (self):
        return self.description

    def getMath (self):
        return self.math

    def setDetected (self):
        self.detected = True
    
    def setUndetected (self):
        self.detected = False
    
    def isDetected (self):
        return self.detected
    
## Models an Events Report    
class ER:
    
    def __init__(self, u, i, ts, latitude, longitude):
        self.edu = u
        self.id = i
        self.timestamp = ts
        self.gps = GPS(latitude,longitude)
        self.events = []  # array of integers (types of detected events)
    
    def putEventType(self, y):        
        self.events.append(y)

    def getTimestamp (self):
        return self.timestamp
    
    def getLatitude (self):
        return self.la

    def getLongitude (self):
        return self.lo
    
    def getEventsTypes (self):
        return self.events
    
    def getNumberEI(self):        
        return len(self.events)  # Number of EI in the ER
        
    def printValues(self):
        for y in self.events:
            print ("Type =",  y)
            
    ## This is required to convert the ER to JSON
    def toJSON(self):
        return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True, indent=4)
   
## Supportive class for the JSON convertion
class GPS():
    def __init__(self, latitude, longitude):
        self.la = latitude
        self.lo = longitude
    
