import cv2, socket, pickle, os  

server_ip = "192.168.10.188"
server_port = 9999
bufsize=10000000

#create a new socket
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, bufsize)

# Open the video stream
capture = cv2.VideoCapture(0)

while True:    
    ret,photo = capture.read()    
    
    cv2.imshow('streaming', photo)    
    
    ret, buffer = cv2.imencode(".jpg", photo,[int(cv2.IMWRITE_JPEG_QUALITY),30])    
    data_as_bytes = pickle.dumps(buffer)    
    
    client.sendto(data_as_bytes,(server_ip , server_port))    
    
    key = cv2.waitKey(1)
    # Press 'q' to quit
    if key == ord('q'):
        break 
    
cv2.destroyAllWindows()
capture.release()