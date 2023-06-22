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

        degree = float(instruction[0])
        distance = float(instruction[1])
        correctionDegree = float(instruction[2])
        if (ballIsHold == False):
            print('move to ball')
            ballIsHold = motor.moveToBall(degree, distance, correctionDegree)
        else:
            print('move to gate')
            ballIsHold = motor.moveToGate(degree, distance, correctionDegree)
        
        response = "ballIsHold:" + str(ballIsHold)
        client_socket.send(response.encode())
        print("send to pc: " + response)

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

    #client_thread = threading.Thread(target=handle_client, args= client_socket)
    #client_thread.start()

    handle_client(client_socket)
    

if __name__ == '__main__':
    run()






