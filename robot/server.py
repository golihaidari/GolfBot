#!/usr/bin/env pybricks-micropython
import socket
import motor
import threading

#Author Golbas Haidari

def handle_client(client, address):
    ballIsHold= False
    while True:
        # Receive message from the client
        message = client.recv(1024).decode('utf-8')
        instruction =  message.split(',')
        
        # Check if client wants to exit
        if instruction[0] == 'disconnect':
            print('Received instruction: ' + str(instruction[0]) )
            break

        print("ballIsHold:"+ str(ballIsHold))
        degree = float(instruction[0])
        distance = float(instruction[1])
        if (ballIsHold == False):
            ballIsHold = motor.moveToBall(degree, distance)
        else:
            ballIsHold = motor.moveToGate(degree, distance)
        response = "ballIsHold:" + str(ballIsHold)
        print(response)
        client.send(response.encode())

    client.close()

def run():
    IP = '192.168.43.155'
    Port=6666   

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, Port))  
    server.listen(5)
    print('Start listening...')

    while True:
        # Accept client connections
        client, address = server.accept()

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client, address))
        client_thread.start()

if __name__ == '__main__':
    run()






