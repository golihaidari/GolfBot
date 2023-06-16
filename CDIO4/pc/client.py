import cv2, socket
import camera
import random 
import math 

IP="172.20.10.3"
PORT=6666
robotHeading = 'SOUTH'


def run():   
    cap = cv2.VideoCapture(0) 
    balls = 0    
    ballExist = True    
    while ballExist:                        
        ret, frame = cap.read() 
        cv2.imshow("window", frame)
        if cv2.waitKey(1) == ord('q'):
            break
        
        if ret:    
            ballsPositions = camera.detectBalls(frame)
            balls= len(ballsPositions)
            if balls > 0 :
                print('1. client: number of detected balls: '+ str(balls))
                robotPosition = camera.detectRobot(frame)
                print('2. client: robot position: '+ str(robotPosition))
                randomBall = chooseRandomBall(ballsPositions)
                randomBall2 = chooseRandomBall(ballsPositions)

                print('3. client: closest ball position: ' + str(randomBall))
                distance = calculateDistance(randomBall, randomBall2)
                msg = sendToRobot(randomBall,distance)
                print('5. Robot*: '+ msg)
            else: 
                print('-client*: there is no ball')
                ballExist = False 
        else:
            print("-client*: No image detected. Please! try again") 
    
    cap.release()
    cv2.destroyAllWindows()

#calculate the distance between the robot and the ball
def calculateDistance(position1, position2):
    x1, y1 = position1
    x2, y2 = position2
    nx= (x2-x1)
    ny= (y2-y1)
    #distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    print("distance :!!!!")
    print((nx, ny))
    return (nx,ny)

def moveRobot():
    distance = calculateDistance()
    nx = distance.nx
    ny = distance.ny

    def southCase():
        if nx > 0 and ny > 0:
            moveForward(ny)
            turnLeft()
            moveForward(nx)
            robotHeading = 'EAST'
            pass
            

        elif nx < 0 and ny > 0:
            moveForward(ny)
            turnRight()
            moveForward(nx)
            robotHeading = 'WEST'
            pass
            
        
        elif nx > 0 and ny < 0:
            moveBackward(ny)
            turnLeft()
            moveForward(nx)
            robotHeading = 'EAST'
            pass
            

        elif nx < 0 and ny < 0:
            moveBackward(ny)
            turnRight()
            moveForward(nx)
            robotHeading = 'WEST'
            pass

        return robotHeading
        
        
    def northCase():
        if nx >0 and ny >0:
            moveBackward(ny)
            turnRight()
            moveForward(nx)
            robotHeading = 'EAST'
            pass

        elif nx < 0 and ny >0:
            moveBackward(ny)
            turnLeft()
            moveForward(nx)
            robotHeading ='WEST'
            pass

        elif nx > 0 and ny <0:
            moveForward(ny)
            turnRight()
            moveForward(nx)
            robotHeading = 'EAST'
            pass
        
        elif nx < 0 and ny < 0:
            moveForward(ny)
            turnLeft()
            moveForward(nx)
            robotHeading = 'WEST'
            pass

        return robotHeading

    


    def eastCase():

        if nx >0 and ny >0:
            moveForward(nx)
            turnRight()
            moveForward(ny)    
            robotHeading = 'SOUTH'

        elif nx < 0 and ny >0:
            moveBackward(nx)
            turnRight
            moveForward(ny)
            robotHeading = 'SOUTH'
        
        elif nx > 0 and ny <0:
            moveForward(nx)
            turnLeft
            moveForward(ny)
            robotHeading = 'NORTH'

        elif nx < 0 and ny < 0:
            moveBackward(nx)
            turnLeft
            moveForward(ny)
            robotHeading = 'NORTH'


        return robotHeading


    def westCase():


        if nx >0 and ny >0:
            moveBackward(nx)
            turnLeft
            moveForward(ny)
            robotHeading = 'South'
            

        elif nx < 0 and ny >0:
            moveForward(nx)
            turnLeft
            moveForward(ny)
            robotHeading = 'South'
        
        elif nx > 0 and ny <0:
            moveBackward(nx)
            turnRight
            moveForward(ny)
            robotHeading = 'NORTH'

            
        

        elif nx < 0 and ny < 0:
            moveForward(nx)
            turnRight
            moveForward(ny)
            robotHeading ='NORTH'

        return robotHeading
        
    switch = {
        'North': northCase,
        'South': southCase,
        'East': eastCase,
        'West': westCase,
    }

    # Call the function retrieved from dictionary
    func = switch.get(robotHeading)
    if func:
        func()
    else:
        print("Invalid heading")


#Choses a random ball
def chooseRandomBall(ballsPositions):
    randomIndex = random.randint(0, len(ballsPositions) - 1)
    return ballsPositions[randomIndex]


def sendToRobot(randomBall,distance,instruction):
    server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server.connect((IP, PORT))

    server.send(bytes(instruction, 'utf-8'))
    print('Client: sent instruction to server: ' + instruction)


    data_string = str(randomBall)+' & '+ str(distance)
    server.send(bytes(data_string,'utf-8'))
   
    print('4. client: sent randomBall-position and calculated distance to server')

    buffer = server.recv(1024)
    buffer = buffer.decode('utf-8')

    server.close()

    return buffer


def moveForward(distance):
    instruction = 'moveforward' +str(distance)
    response = sendToRobot(instruction)
    return response

def moveBackward(distance):
    instruction = 'movebackward'+str(distance)
    response = sendToRobot(instruction)
    return response

def turnLeft():
    instruction = 'turnleft'
    response = sendToRobot(instruction)
    return response

def turnRight():
    instruction = 'turnright'
    response = sendToRobot(instruction)
    return response
    

if __name__ == '__main__':
    run()

