#! /usr/bin/env python3
import sys
sys.path.append("../lib")       # for params

import os, socket, params


switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

# Copied what fileServer.py does in the while loop to receive messages
while True:
    sock, addr = lsock.accept() 

    from fileSock import fileSend, fileReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = fileReceive(sock, debug) # first payload is files name
            if debug: print("rec'd: ", payload)
            if not payload:
                break
            else:
                fileName = payload.decode() 
                data = fileReceive(sock, debug) # second payload is the data in the file
                wrtieFile = open('new_'+fileName, 'wb')
                wrtieFile.write(data)
                wrtieFile.close() # write the new file and close it
                print("complete")