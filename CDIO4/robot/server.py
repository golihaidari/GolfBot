import socket, time


#write code to fetch & deliver the ball
def handleRequest(ballPosition):
    print(f'4.1-move to {ballPosition}')
    time.sleep(3)
    print('4.2- grap the ball')
    print('4.3- move to delivering gate')
    time.sleep(3)
    print('4.4- release the ball')
    print('4.5- push the ball to the gate')


try:
    hostname=socket.gethostname()
    IP = socket.gethostbyname(hostname)
    Port = 6666

    server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server.bind((IP,Port))
    server.listen(5)
    print (f"1-Server- {IP} - start listening....")

    while True:    
        client, address = server.accept()    
        print (f'2-Connection established - {address[0]} : {address[1]}')   

        data= client.recv(1024)
        ballPosition= data.decode('utf-8')
        print('3-recived data (ball-position) from client:' + ballPosition)

        handleRequest(ballPosition)

        client.send('Ball collected!'.encode())
        print ('5-response to client: ball is collected')

        client.close()
        print ('6-Connection Closed') 

except:
    print('Error occured! : cannot run the program')



