#!/usr/bin/env python

import socket
import time
import traceback
import serial
import sys

TCP_IP = 'api.jinhao.me'
TCP_PORT = 9058
BUFFER_SIZE = 1024
DEMO_MODE = False
s = None

if(len(sys.argv) != 2):
    print 'Running in demo mode'
    DEMO_MODE = True

if(not DEMO_MODE): ser = serial.Serial(sys.argv[1], baudrate = 9600)

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
        except KeyboardInterrupt:
            s.close()
            print "Bye"
            sys.exit()
        except:
            print 'Connection lost, reconnecting...'
            s.close()
            break

        if(len(data) == 0):
            print 'Connection lost, reconnecting...'
            s.close()
            break

        data = data.replace('K', '')
        if len(data) == 0: continue

        print 'Data received: ' + data
        if data[0] == '?' :                         # Accquire
            s.send(str(status[data[1]]))
            #print '[' + str(status[data[1]]) + ']'
        if data[0] == '!' :                         # ON/OFF
            if data[1].isupper() :   # Turn on
                status[data[1].upper()] = 1
                command = data[1].upper()
                print command
                if(not DEMO_MODE): ser.write(command)
            elif data[1].islower() : # Turn off
                status[data[1].upper()] = 0
                command = data[1].lower()
                print command
                if(not DEMO_MODE): ser.write(command)
            s.send('R')
        if data[0] == '~' and data[1] == 'L' :      # PWM
            status['L'] = int(data[2:])
            s.send('R')
            command = 'L' + str(status['L']).zfill(3)
            print command
            if(not DEMO_MODE): ser.write(command)

    s.close()
