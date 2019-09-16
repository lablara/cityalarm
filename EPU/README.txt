Emergency Processor Unit

Default TCP port to receive ER: 55055

Dafault values to constants:
fe = 0.4
fr = 0.3
ft = 0.3

Medium in Gaussian = 12
Standard deviation in Gaussian = 6

Three Risk Zones as default values (la, lo, radius(km), rz)
definedRZ = [[41.179220,-8.597667,50,70], \
             [41.185324,-8.696129,20,50], \
             [41.129798,-8.607621,30,90]]

The EPU may receive three different parameters as command-line arguments:
-d debug (True or False)
-e idEPU (the numerical id of EPU)
-i ipBroker (the IP address of the MQTT Broker - default port is considered)
