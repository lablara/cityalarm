Emergency Alarm Client

The MQTT topics published by the EPU are in the form of "EPU_CityAlarm_U", with U being the numerical id of the EPU

The EAC may receive three different parameters as command-line arguments:
-d debug (True or False)
-i ipBroker (the IP address of the MQTT Broker - the default MQTT port is considered)
-m requestEA (the MQTT topic that the EAC is subscribing to)
