# *********************************************************************
# Accessory classes for the EPU
# They model the concepts of Events Report and Emergency Alarm
# Author      : Daniel G. Costa
# E-mail      : danielgcosta@uefs.br
# Date        : 2019/09/10
# *********************************************************************

import json

########################################################

## Just like in the EDU
class ER:
    def __init__(self, u, i, ts, latitude, longitude):
        self.edu = u
        self.id = i
        self.timestamp = ts
        self.gps = GPS(latitude,longitude)
        self.events = []

    def putEvent(self, y):
        self.events.append(y)

    def getEventsTypes (self):
        return self.events

    def getTimestamp (self):
        return self.timestamp

    def getLatitude (self):
        return self.gps.la

    def getLongitude (self):
        return self.gps.lo

    def getNumberEI(self):
        return len(self.events)

    def printTypes(self):
        print ("ER with the following EI types:")
        for y in self.events:
            print ("Type:",  y)

    def toJSON(self):
        return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True, indent=4)

########################################################

## Supportive class for the JSON conversion
class GPS():
    def __init__(self, latitude, longitude):
        self.la = latitude
        self.lo = longitude

########################################################

class RiskZone():
    ## Basic definitions of the risk zones
    def __init__(self, i, latitude, longitude, radius, risk):
        self.id = i
        self.gps = GPS(latitude,longitude)
        self.dz = radius
        self.rz = risk

    def getId(self):
        return self.id

    def getRZ(self):
        return self.rz

    def getLatitude (self):
        return self.gps.la

    def getLongitude (self):
        return self.gps.lo

    def getRadius(self):
        return self.dz

    def printValues(self):
        print ("Latitude:",self.gps.la,", Longitude:",self.gps.lo,", Radius",self.dz,", Risk level:",self.rz)

########################################################

# Definition of an Emergency Alarm
class EA():
    def __init__(self, i, ts, latitude, longitude):
        self.id = i
        self.gps = GPS(latitude,longitude)
        self.timestamp = ts
        self.events = []
        self.sl = 0

    def getLatitude (self):
        return self.gps.la

    def getLongitude (self):
        return self.gps.lo

    def putEvent(self, y):
        self.events.append(y)

    def getEventsTypes (self):
        return self.events

    def setSeverityLevel(self, sev):
        self.sl = sev

    def getSeverityLevel (self):
        return self.sl

    def getId(self):
        return self.id

    def printValues(self):
        print ("EA id:",self.id,", Timestamp:",self.timestamp,", Latitude:",self.gps.la,", Longitude:",self.gps.lo, " SL:", self.sl)
        print ("This EA has the following EI types:")
        for e in self.events:
            print ("Type:",e)

    def toJSON(self):
        return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True, indent=4)