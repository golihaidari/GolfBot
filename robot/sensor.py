#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import UltrasonicSensor, InfraredSensor, ColorSensor
from pybricks.parameters import Port, Stop, Color, SoundFile

#Author Golbas Haidari

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# The colored objects are white or brwon.
POSSIBLE_COLORS = [Color.WHITE, Color.BROWN]

front_sensor = UltrasonicSensor(Port.S1)
right_sensor = InfraredSensor(Port.S2)
color_sensor = ColorSensor(Port.S3)

def detecBallColor():
    x= 0
    while x< 3:
        color = color_sensor.color()
        if(color == Color.WHITE or color == Color.YELLOW):
            return str(color)
    return 'unknown'
    

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