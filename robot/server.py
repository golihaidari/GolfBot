#!/usr/bin/env pybricks-micropython
import socket
import motor

#Author Golbas Haidari

#write code to fetch & deliver the ball
def handleRequest(ballPosition):
    split_instruct=  ballPosition.split(',')
    msg =''   
    motor.runTest(split_instruct)
    msg = 'Ball collected!'
    print('ball is delivered')
    return msg

try:
    #hostname=socket.gethostname()
    #IP = socket.gethostbyname(hostname)
    IP = '192.168.43.155'
    Port=6666

    server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server.bind((IP,Port))
    server.listen(5)
    print ("Start listening....")

    while True:    
        client, address = server.accept()    
        #print (f'Connection established - {address[0]} : {address[1]}')   

        data= client.recv(1024)
        ballPosition= data.decode('utf-8')
        print(ballPosition)         
        
        handleRequest(ballPosition)

        client.send('Ball collected!'.encode())

        client.close()

except: 
    print('Error occoured!!')









