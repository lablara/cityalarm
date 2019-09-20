# *********************************************************************
# This is a simple Emergency Alarm Client (EAC)
# It only shows the received EA in the JSON format
# This implementation is based on the CityAlarm paper
# Author      : Daniel G. Costa
# E-mail      : danielgcosta@uefs.br
# Date        : 2019/09/01
# *********************************************************************

import time, datetime

########################################################

## Definition of an Emergency Alar

class ListEA:

    def __init__(self):
        self.alarms = []

    def putAlarm(self, ea, debug):

        lat = ea.getLatitude()
        lon = ea.getLongitude()

        control = True
        ## Only insert new EA for new coordinates
        for alarm in self.alarms:
            if alarm.getLatitude() == lat and alarm.getLongitude() == lon:  ## Refresh alarm
                self.alarms.remove(alarm)
                self.alarms.append(ea)
                control = False
                if debug:
                    print("Removing old EA and inserting updated alarm...")

        if control:
            if debug:
                print ("Inserting new EA...")
            self.alarms.append(ea)


    ## Remove very old EA
    def updateAlarms(self, maxTime, debug):

        t = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
        now = t.timestamp()

        for alarm in self.alarms:
            alarmTime = datetime.datetime.strptime(alarm.getTimestamp(), "%a %b %d %H:%M:%S %Y").timestamp()

            if (now - alarmTime) > maxTime:  ## Old EA
                self.alarms.remove(alarm)
                if debug:
                    print ("Removing old EA with id:", alarm.getId())


    def getAlarms(self):
        return self.alarms

    def printValues(self):
        for ea in self.alarms:
           print("Id:", ea.getId(), ": Latitude =", ea.getLatitude(), ": Longitude =", ea.getLongitude(), ": Severity =", ea.getSeverityLevel())

###############################################################

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

    def getTimestamp(self):
        return self.timestamp

    def printValues(self):
        print ("EA id:",self.id,", Timestamp:",self.timestamp,", Latitude:",self.gps.la,", Longitude:",self.gps.lo, " SL:", self.sl)
        print ("This EA has the following EI types:")
        for e in self.events:
            print ("Type:",e)

    def toJSON(self):
        return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True, indent=4)

###############################################################

class GPS():
    def __init__(self, latitude, longitude):
        self.la = latitude
        self.lo = longitude

###############################################################