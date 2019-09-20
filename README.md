# cityalarm
Implementation of the CityAlarm Emergency Alerting System.

This implementation is in accordance with a scientific paper that describes it. The paper is still under peer-reviewing and will be linked here as soon as it is published.

The CityAlarm implementation is divided in three elements:

Events Dectection Unit (EDU)
Emergency Processor Unit (EPU)
Emergency Alarm Client (EAC)

All codes are written in Python3, using some libraries.

*******************************************************************

The EDU is implemented around the GrovePi+ hardware framework. However, other interfaces for interaction with sensor devices can be used. In fact, the expected functions of EDU are modularized, allowing that other types of sensor devices be easilly inserted.

The GrovePi+ has to be installed and enabled, as specified by the manufacturer (https://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/)

Before using the EDU, one library has also to be installed through the following command:

pip3 install numpy

As a second remark about the EDU and GrovePi+, the GPS module operates through the serial port of Raspberry and thus the Bluetooth module needs to be deactivated in some versions

*******************************************************************

For the EPU, the haversine lib has to be installed:

pip3 install haversine

For the EPU and the EAC, the paho-mqtt library has also to be installed, using the follwing command:

pip3 install paho-mqtt

*******************************************************************

If the EAC_Map is employed, the Folium library has to be installed through the following command:

pip3 install paho-mqtt
