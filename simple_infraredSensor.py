#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

#The ev3 can play notes
#This can be used for debugging and instructions
#ev3.speaker.play_notes(['C4/6', 'C3/6'])

#Can say a text string in google translate way
ev3.speaker.set_speech_options(language='es', voice='m2', speed=190, pitch=80)

#ev3.speaker.say('Un, dos, tres. Un pasito pa lante, María. Un, dos, tres. Un pasito pa atrás')

ev3.speaker.set_speech_options(language='da', voice='f3', speed=190, pitch=80)

ev3.speaker.play_notes(['C4/6', 'D4/6', 'E4/6', 'F4/4', 'E4/4'])

#initialise sensor (see which port it is connected to)
infrared_sensor = InfraredSensor(Port.S1)

#the proximity towards an object, which will cause an action
proximityLimit=20 #percentage of range of the sensor

#Note: the sensor may be especially sensitive to light in environment
#The proximityLimit may therefore change depending on the environment

#Easier way to test sensor without using motors
while True:
   if (infrared_sensor.distance() < proximityLimit):
      ev3.speaker.say('Infrarød sensor ser en væg')
    
#Med proximityLimit 40 er den 25 cm fra den infrarøde sensor (i lys miljø)
#Med proximityLimit 20 er den 10,5 cm fra den infrarøde sensor (i lys miljø)

#Med proximityLimit 40 er den 23 cm fra den infrarøde sensor (i mørkt miljø)
#Med proximityLimit 20 er den 10,5 cm fra den infrarøde sensor (i mørkt miljø)
