# cityalarm
Implementation of the CityAlarm Emergency Management System
This implementation is in accordance with a scientific paper that describes it. The paper is still under peer-reviewing and will be linked here as soon as it is published

The CityAlarm implementation is divided in three elements:

Event Dectection Unit (EDU)
Emergency Processor Unit (EPU)
Emergency Alarm Client (EAC)

The EDU is implemented in Python around the GrovePi+. However, other interfaces for interaction with sensor devices can be used. In fact, the expected functions of EDU are modularized, allowing that other types of sensor devices be easilly inserted.

The EDU also employs the TM1637 module, which requires two additional libraries that can be installed through the following commands: 

pip3 install numpy

pip3 install haversine

pip3 install paho-mqtt



curl -kL dexterindustries.com/update_grovepi | bash

Links for grovepi installation
Links to allow gps to operate

