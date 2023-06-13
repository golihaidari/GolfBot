#!/usr/bin/env pybricks-micropython
import socket
import traceback
import motor

#Author Golbas Haidari

#write code to fetch & deliver the ball
def handleRequest(randomBall,distance):
    #print(f'move to {ballPosition}') 
    distance = float(distance)   
    motor.moveTowardBall(randomBall,distance)
    print('ball is delivered')

# try:
print("hej")
#hostname=socket.gethostname()
#IP = socket.gethostbyname(hostname)
IP = "172.20.10.3"
Port=6666

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
print("hejhej")
server.bind((IP,Port))
server.listen(5)
print ("Start listening....")

while True:    
  client, address = server.accept()    
  #print (f'Connection established - {address[0]} : {address[1]}')   

  data= client.recv(1024)
  decoded_data= data.decode('utf-8')
  
  print("Received data:", decoded_data)

  split_data = decoded_data.split(" & ")
  if len(split_data) == 2:

        randomBall = split_data[0]
        distance = split_data[1]
        print("Random Ball Position:", randomBall)
        print("Distance:", distance)
  
         
  
  handleRequest(randomBall,distance)

  client.send('Ball collected!'.encode())

  client.close()


  

# except: 
# print('Error occoured!!')











