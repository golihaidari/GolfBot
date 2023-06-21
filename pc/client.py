from scipy.spatial import distance as dist
import numpy as np
import cv2, socket
import camera

#Author Golbas Haidari

IP="192.168.38.142"

PORT=6666
robotRealWidth = 170 #133

colors = ((240, 0, 159), (0, 0, 255), (0, 255, 0), (0, 165, 255), (255, 255, 0))
def run(): 
    server_socket = connectToRobot(IP, PORT)
    head= 'EAST'
    cap = cv2.VideoCapture(1)  
    ballExist = True
    ballIsHold = False    
    while ballExist:
        print("Start taking a photo")        
        ret, frame = cap.read() 
        cv2.imshow("window", frame)
        if cv2.waitKey(1) == ord('q'):
            break

        if ret: 
            (rx,ry,rw) = camera.detectRobot(frame)
            if(rx == 0):
                print('Robot is not detetced!, Retry...')
                continue

            objectPositions = []
            if (ballIsHold == False): 
                objectPositions = camera.detectBalls(frame)
                if(len(objectPositions) == 0): 
                    print('Balls not detected. Retry...')
                    sendToRobot('disconnect' , 'NA',-'NA' )
                    continue
            else:
                objectPositions = camera.detectGates(frame)  
                if(len(objectPositions) == 0):
                    print('Gates not detected. Retry...')
                    continue

            ((objectX,objectY),objectDistance) = findNearestObject(objectPositions, (rx, ry, rw))             
                    
            displayObjects(frame, (rx,ry), (objectX,objectY)) 

            displayDistance(frame, (rx,ry), (objectX,objectY), objectDistance)

            adjacent = getAdjacent((rx,ry), head)
                
            displayObjects(frame, (rx,ry), adjacent) 

            degree= getAngle((rx,ry), adjacent, (objectX,objectY)) 

            #(direction, autoCorrectionDegree) = AutoCorrect(head, degree)
            #head = direction
            print('Robot is headed:', head)
              
            # show the output image
            cv2.imshow("Image", frame)
            print('Enter to send the data to the robot')
            cv2.waitKey(0)

            msg = sendToRobot(server_socket, degree , (objectDistance-110), (degree*-1) )
            print('Robot*:'+ msg)

            if msg == "ballIsHold:True":
                ballIsHold = True
            else:
                ballIsHold = False
        else:
            print('Error: could NOT read frame!!')          

    cap.release()
    cv2.destroyAllWindows()
    disconnect(server_socket)

def displayObjects(frame, object1, object2):
    # draw circles corresponding to the current points and
    cv2.circle(frame, object1, 10, colors[0], -1)
    cv2.circle(frame, object2, 10, colors[1], -1)
	# connect them with a line
    cv2.line(frame, object1, object2, colors[2], 2)

def midpoint(robotPosition, objectPosition):
	return ((robotPosition[0] + objectPosition[0]) * 0.5, (robotPosition[1] + objectPosition[1]) * 0.5)

def displayDistance(frame, object1, object2, objectDistance):
    (mX, mY) = midpoint(object1, object2)
    cv2.putText(frame, "{:.1f}mm".format(objectDistance), (int(mX), int(mY - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, colors[1], 2)

#Compute angle between robot direction and ball position
def getAngle(robotposition, adjacent, objectPosition):
    # Calculate the direction vectors of the lines
    line1 = np.array([adjacent[0] - robotposition[0], adjacent[1] - robotposition[1]])
    line2 = np.array([objectPosition[0] - robotposition[0], objectPosition[1] - robotposition[1]])

    # Calculate the angle between the lines in radians
    angle_radians = np.arctan2(line2[1], line2[0]) - np.arctan2(line1[1], line1[0])
    
    # Convert the angle to degrees
    angle_degrees = np.degrees(angle_radians)

    # Ensure the angle is within the range of -180 to 180 degrees
    if angle_degrees > 180:
        angle_degrees -= 360
    elif angle_degrees < -180:
        angle_degrees += 360
    
    # Print the angle
    print("Angle (in degrees):", angle_degrees)

    return angle_degrees

#compute adjacent
def getAdjacent(robotPosition, head):
    adjacent= None
    
    if head == 'NORTH':
        adjacent= (robotPosition[0], (robotPosition[1] - 100) )
    elif head == 'SOUTH':
        adjacent= (robotPosition[0], (robotPosition[1] + 100) )
    elif head == 'EAST':
        adjacent= ( (robotPosition[0] + 100), robotPosition[1])
    elif head == 'WEST':
        adjacent= ( (robotPosition[0] - 100), robotPosition[1])

    return adjacent

def AutoCorrect(head, degree):
    direction= head
    if(head=='EAST' and degree >= -90 and degree <= 90):
        degree = -degree
        direction= 'EAST'
    elif(head=='EAST' and degree > 90 ):
        degree = 180 - degree
        direction = 'WEST'
    elif(head=='EAST' and degree < -90):
        degree = 180 + degree
        direction = 'WEST'

    elif(head=='WEST' and degree >= -90 and degree <= 90):
        degree = -degree
        direction = 'WEST'
    elif(head=='WEST' and degree > 90 ):
        degree = -180 + degree
        direction = 'EAST'
    elif(head=='WEST' and degree < -90):
        degree = 180 + degree
        direction = 'WEST'
    print('head: '+ head + "correctionDegree: "+ str(degree))
    return(direction, str(degree))



def findNearestObject(objectPositionList, robotPosition):
    closestPosition = objectPositionList[0]
    objectDistance = dist.euclidean((robotPosition[0],robotPosition[1]), closestPosition) / (robotPosition[2]/float(robotRealWidth))    
    for object in objectPositionList:
        newDistance = dist.euclidean((robotPosition[0],robotPosition[1]), (object)) / (robotPosition[2]/float(robotRealWidth))
        if(newDistance < objectDistance):
            objectDistance = newDistance
            closestPosition = object
    print('Closest-object position: ' + str(closestPosition[0])+','+str(closestPosition[1])) 
    return (closestPosition, objectDistance) 

def connectToRobot(IP, PORT):
    server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server_socket.connect((IP, PORT))
    print('Connection to the robot is established.')
    return server_socket

def sendToRobot(server_socket, rotattionDegree, objectDistance, autoCorrectionDegree):
    data_string = str(rotattionDegree) +','+ str(objectDistance) + ','+ str(autoCorrectionDegree)
    print(data_string)
    server_socket.send(bytes(data_string,'utf-8'))
    print('Instruction is sent to robot')

    message = server_socket.recv(1024).decode('utf-8')
    return message

def disconnect(server_socket):
    server_socket.close()
    
if __name__ == '__main__':
    run()

