from pc.camera import detectGoal, detectRobot 
from test.motor import moveForward, moveBackward, moveArmUp, moveArmDown
import cv2 #This may be changed

# Author: s194612 - Gülsen

def goalPhase():
    #Initialising camera (so frame is known)
    #This may be changed
    cap = cv2.VideoCapture(1)
    frame = cap.read()


    #Finds the locations of robot and goals
    robotPosition = detectRobot(frame)
    goalPositions = detectGoal(frame)

    #Calculate distance to closest goal
    #A 'Calculatedistance' method is the best solution
    #But an alternative solution is comparing x-values
    goalOne = goalPositions[0] #This should change later
    goalTwo = goalPositions[1] #This should change later

    #Move to the goal (but a few x-values off)
    #The code below is psuodo-code
    #if goalOne > goalTwo:
       #moveToLocation(robotPosition, goalPositions[1])
    #else:
       #moveToLocation(robotPosition, goalPositions[0])


    #Quickly pushes ball
    moveBackward(50)
    moveArmUp()
    moveForward(50)
    moveArmDown()


    