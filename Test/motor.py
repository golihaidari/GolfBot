#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop, SoundFile
from pybricks.tools import wait
from pybricks.robotics import DriveBase

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.D)
gripper_motor = Motor(Port.A)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

def moveForward(distance):
    ev3.speaker.say('forward')
    robot.straight(distance)

def moveBackward(distance):
    ev3.speaker.say('backward')
    robot.straight(-distance)

def turnRight(degree):
    ev3.speaker.say('right')
    robot.turn(degree)

def turnLeft(degree):
    ev3.speaker.say('left')
    robot.turn(-degree)

def uTurn():
    ev3.speaker.say('U turn')
    robot.turn(180) 


def moveArmUp():
    ev3.speaker.say('arm up')
    gripper_motor.run_until_stalled(-200, then=Stop.COAST, duty_limit=50)
    gripper_motor.reset_angle(0)
       
def moveArmDown():
    ev3.speaker.say('hold ball')
    gripper_motor.reset_angle(0)
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)

def runTest():
    ev3.speaker.play_file(SoundFile.READY)    
    moveForward(500)
    moveBackward(500)
    turnRight(90)
    turnLeft(90)
    uTurn()
    moveArmDown() 
    moveArmUp()
    



