import cv2, socket, numpy, pickle
import detectRobot as dr

ip="192.168.10.188" #replace this with EVR IP Address
port = 9999 # Feel free to change this port
bufsize = 1000000

#create a new socket
server = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
server.bind((ip,port))
print("Robot is listening on %s:%d" % (ip, port))

while True:
    # recieve message from the client
    request = server.recvfrom(bufsize)
    clientIp = request[1][0]    
    data = request[0] 
    print("Recived data: ")    
    print(data)  
    data=pickle.loads(data)
    print(type(data))
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    cv2.imshow('server', data) #to display image in awindow
    dr.detect_robot(data)
    
    
    key = cv2.waitKey(1)
    # Press 'q' to quit
    if key == ord('q'):
        break 

cv2.destroyAllWindows()


