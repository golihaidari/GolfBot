import cv2, socket
import camera

IP="192.168.43.155"
PORT=6666


def run():   
    cap = cv2.VideoCapture(1) 
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
                closestBall = findNearestBall(ballsPositions, robotPosition)
                print('3. client: closest ball position: ' + str(closestBall))
                
                msg = sendToRobot(closestBall)
                print('5. Robot*: '+ msg)
            else: 
                print('-client*: there is no ball')
                ballExist = False 
        else:
            print("-client*: No image detected. Please! try again") 
    
    cap.release()
    cv2.destroyAllWindows()

# need implementation!!!!!!!!!!!!!!!   use vector to find the closest ball and return it
def findNearestBall(ballsPositions, robotPosition):
    if len(ballsPositions) > 2 :
        return ballsPositions[1]
    else:
        return ballsPositions[0]


def sendToRobot(ballposition):
    server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server.connect((IP, PORT))

    data_string = str(ballposition)
    server.send(bytes(data_string,'utf-8'))
    print('4. client: sent closestball-position to server')

    buffer = server.recv(1024)
    buffer = buffer.decode('utf-8')

    server.close()

    return buffer
    

if __name__ == '__main__':
    run()

