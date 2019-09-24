Emergency Alarms Client

This is a very simple implementation to only print received Emergency Alarms on the screen

The MQTT topics subscribed by this EAC are in the form of "CityAlarm_EPUu", with u being the numerical id of the EPU

The EAC may receive three different parameters as command-line arguments:
-d debug (True or False)
-i ipBroker (the IP address of the MQTT Broker - the default MQTT port is always used)
-m requestEA (the MQTT topic that the EAC is subscribing to)
