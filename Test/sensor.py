#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import UltrasonicSensor, InfraredSensor, ColorSensor
from pybricks.parameters import Port, Stop, Color, SoundFile


# Initialize the EV3 Brick.
ev3 = EV3Brick()

# The colored objects are white or brwon.
POSSIBLE_COLORS = [Color.WHITE, Color.BROWN]

color_sensor = ColorSensor(Port.S2)
right_sensor = InfraredSensor(Port.S1)
front_sensor = UltrasonicSensor(Port.S4)


def color_sensor_detect():
    b= True
    ev3.speaker.say('Start testing color sensor')
    while b == True:
        color = color_sensor.color()        
        if (color_sensor.color() == Color.WHITE):
            b= False
        ev3.speaker.say(str(color))
    ev3.speaker.say('finished.')



def front_sensor_detect():
    b = True
    ev3.speaker.say('Start testing front sensor')
    while b == True:
        distance = front_sensor.distance()
        ev3.speaker.say('distance' + str(distance/10)) # ultrasonic return the distance in mm , to gain cm we divde by 10
        if (distance < 68):
            b= False
    ev3.speaker.say('finished.')



def right_sensor_detect():
    b = True
    ev3.speaker.say('Start testing right sensor')
    while b == True:
        distance = right_sensor.distance()
        ev3.speaker.say(str(distance))
        if (distance < 3):
            b= False
    ev3.speaker.say('finished.') 





def runTest():

    color_sensor_detect()

    front_sensor_detect()
    
    right_sensor_detect()