#!/usr/bin/env python

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 9058
BUFFER_SIZE = 1024

status = {'L': 0, 'A': 0, 'W': 0, 'H': 0}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# Waiting for handshake
data = s.recv(BUFFER_SIZE)
if data == 'SPOT' :
    print 'Connected to server'
else:
    print 'Handshake failed'
    s.close()
    exit()

# Main loop
while 1:
    data = s.recv(BUFFER_SIZE)
    if data[0] == '?' :          # Accquire
        s.send(str(status[data[1]]))
        #print '[' + str(status[data[1]]) + ']'
    if data[0] == '!' :
        if data[1].isupper() :   # Turn on
            status[data[1].upper()] = 1
            print data[1].upper()
        elif data[1].islower() : # Turn off
            status[data[1].upper()] = 0
            print data[1].lower()
        s.send('R')
    if data[0] == '~' and data[1] == 'L' :          # PWM
        status['L'] = int(data[2:])
        s.send('R')
        print 'L' + str(status['L']).zfill(3)

s.close()
