#!/usr/bin/env pybricks-micropython
import socket
import motor
import threading

#Author Golbas Haidari

def handle_client(client_socket):
    ballIsHold= False
    while True:
        # Receive message from the client
        message = client_socket.recv(1024).decode('utf-8')
        instruction =  message.split(',')
        print('msg'+message)
        # Check if client wants to exit
        if instruction[0] == 'disconnect':
            print('Received instruction: ' + str(instruction[0]) )
            break

        print("ballIsHold:"+ str(ballIsHold))
        degree = float(instruction[0])
        distance = float(instruction[1])
        correctionDegree = float(instruction[2])
        if (ballIsHold == False):
            ballIsHold = motor.moveToBall(degree, distance, correctionDegree)
        else:
            ballIsHold = motor.moveToGate(degree, distance, correctionDegree)
        response = "ballIsHold:" + str(ballIsHold)
        print(response)
        client_socket.send(response.encode())

    client_socket.close()

def run():
    IP = '192.168.43.155'
    Port=6666   

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, Port))  
    server_socket.listen(1)
    print('Start listening...')

    # Accept client connections
    client_socket, address = server_socket.accept()
    print('connected to', address)

    handle_client(client_socket)
    

if __name__ == '__main__':
    run()






