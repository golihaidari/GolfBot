import math
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import cv2, imutils, socket
import numpy as np
import camera


IP="192.168.43.155"
PORT=6666

colors = ((240, 0, 159), (0, 0, 255), (0, 255, 0), (0, 165, 255), (255, 255, 0))
def run():   
    cap = cv2.VideoCapture(0) 
    balls = 0    
    ballExist = True    
    while ballExist:
        print("1.client: Start taking a photo")                        
        ret, frame = cap.read() 
        cv2.imshow("window", frame)
        if cv2.waitKey(1) == ord('q'):
            break
        
        if ret:    
            ballsPositions = camera.detectBalls(frame)
            if len(ballsPositions) == 0 : 
                print('-client*: No ball is detected!!!!')
                print('-client*: Retry to detect balls')
                continue

            print('2. client: number of detected balls: '+ str(len(ballsPositions)))
            (rx, ry, rw) =  camera.detectRobot(frame)
            if rx == 0:
                print("-client*: Robot is not detected")
                print('-client*: Retry to detect Robot')
                continue                    

            print('3. client: robot position: '+ str(rx) +str(ry))
            ((bx,by),ballDistance) = findNearestBall(ballsPositions, (rx, ry, rw))             
            print('4. client: closest ball position: ' + str(bx)+','+str(by))  

            # draw circles corresponding to the current points and
            cv2.circle(frame, (rx,ry), 10, colors[0], -1)
            cv2.circle(frame, (bx,by), 10, colors[1], -1)
		    # connect them with a line
            cv2.line(frame, (rx,ry), (bx,by), colors[2], 2)  
            
            # compute the Euclidean distance between the coordinates,
		    # and then convert the distance in pixels to distance in units
            # pixelsPerMetric = (rw/float(133))
            # D = dist.euclidean((rx,ry), (bx,by)) / pixelsPerMetric 
            (mX, mY) = midpoint((rx,ry), (bx,by))
            cv2.putText(frame, "{:.1f}mm".format(ballDistance), (int(mX), int(mY - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, colors[1], 2)

            #compute adjacent
            cv2.circle(frame,(rx,by), 10, colors[1], -1)
            cv2.line(frame,(rx, ry), (rx,by), colors[2], 2)
            (aX, aY)= midpoint((rx,ry), (rx,by))
            adjacentPointDistance = dist.euclidean((rx,ry), (rx,by)) / (rw/float(133)) 
            cv2.putText(frame, "{:.1f}mm".format(adjacentPointDistance), (int(aX), int(aY - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, colors[1], 2)

            #compute opposite
            cv2.circle(frame,(rx,by), 10, colors[1], -1)
            cv2.line(frame,(rx, ry), (rx,by), colors[2], 2)
            (aX, aY)= midpoint((rx,ry), (rx,by))
            adjacentPointDistance = dist.euclidean((rx,ry), (rx,by)) / (rw/float(133)) 
            cv2.putText(frame, "{:.1f}mm".format(adjacentPointDistance), (int(aX), int(aY - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, colors[1], 2)

            c = (rx * rx)+(ry * by)+ (rw *rw)
            rl= math.sqrt((rx**2) + (ry**2) ) 
            al= math.sqrt((rx**2) + (by**2) )
            ral= c/ (rl*al)
            degree= np.arccos(ral) 
            print("degree: " + str(degree))
            # show the output image
            cv2.imshow("Image", frame)
            cv2.waitKey(0)
		                           
            msg = sendToRobot((bx,by))
            if msg != "ball catched":
                continue
            
            ret, frame = cap.read() 
            if ret:
                gatesPosition = camera.detectGates(frame)
                robotPosition = camera.detectRobot(frame)
                closestGate= findNearestGate(gatesPosition, robotPosition)
                msg= sendToRobot(closestGate)

            print('6. Robot*: '+ msg)

    cap.release()
    cv2.destroyAllWindows()

def midpoint(robotPosition, ballPosition):
	return ((robotPosition[0] + ballPosition[0]) * 0.5, (robotPosition[1] + ballPosition[1]) * 0.5)

def findNearestBall(ballsPositions, robotPosition):
    closestBall = ballsPositions[0]
    ballDistance = dist.euclidean((robotPosition[0],robotPosition[1]), (closestBall)) / (robotPosition[2]/float(133))    
    for bp in ballsPositions:
        newdistance = dist.euclidean((robotPosition[0],robotPosition[1]), (bp)) / (robotPosition[2]/float(133))
        if(newdistance < ballDistance):
            ballDistance = newdistance
            closestBall = bp
    return (closestBall, ballDistance)
    
def findNearestGate(robotPosition, gatesPosition):
    closestGate = gatesPosition[0]
    gateDistance = dist.euclidean((robotPosition[0],robotPosition[1]), (closestGate)) / (robotPosition[2]/float(133))    
    for gp in gatesPosition:
        newPosition = dist.euclidean((robotPosition[0],robotPosition[1]), (gp)) / (robotPosition[2]/float(133))
        if(newPosition < gateDistance):
            gateDistance = newPosition
            closestGate = gp
    return (closestGate, gateDistance)    
    

def sendToRobot(ballposition):
    server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server.connect((IP, PORT))

    data_string = str(ballposition)
    server.send(bytes(data_string,'utf-8'))
    print('5. client: sent closestball-position to server')

    buffer = server.recv(1024)
    buffer = buffer.decode('utf-8')

    server.close()

    return buffer
    

if __name__ == '__main__':
    run()

