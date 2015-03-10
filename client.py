#!/usr/bin/env python

import socket
import time
import traceback

TCP_IP = 'vita.kuangqi.me'
TCP_PORT = 9058
BUFFER_SIZE = 1024

status = {'L': 0, 'A': 0, 'W': 0, 'H': 0}

while True:
    # start with a socket at 5-second timeout
    print "Creating the socket"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)

    try:
        s.connect((TCP_IP, TCP_PORT))
    except socket.timeout:
        print 'Connect timeout. Retry after 5 sec...'
        time.sleep(5)
        continue
    except:
        print 'Socket connect failed! Loop up and try socket again'
        traceback.print_exc()
        time.sleep(5)
        continue

    # Waiting for handshake
    data = s.recv(BUFFER_SIZE)
    if data == 'SPOT' :
        print 'Connected to server'
    else:
        print 'Handshake failed'
        s.close()
        exit()

    s.settimeout(15.0)

    # Main loop
    while 1:
        try:
            data = s.recv(BUFFER_SIZE)
        except:
            print 'Connection lost, reconnecting...'
            break
        
        if(len(data) == 0):
            print 'Connection lost, reconnecting...'
            break

        print 'Data received: ' + data
        if data[0] == '?' :                         # Accquire
            s.send(str(status[data[1]]))
            #print '[' + str(status[data[1]]) + ']'
        if data[0] == '!' :                         # ON/OFF
            if data[1].isupper() :   # Turn on
                status[data[1].upper()] = 1
                print data[1].upper()
            elif data[1].islower() : # Turn off
                status[data[1].upper()] = 0
                print data[1].lower()
            s.send('R')
        if data[0] == '~' and data[1] == 'L' :      # PWM
            status['L'] = int(data[2:])
            s.send('R')
            print 'L' + str(status['L']).zfill(3)

    s.close()
