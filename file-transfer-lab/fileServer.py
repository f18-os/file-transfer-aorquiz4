#! /usr/bin/env python3

import sys, os
sys.path.append("../lib")       # for params
import re, socket, params

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

sock, addr = lsock.accept()

print("connection rec'd from", addr)


from fileSock import fileSend, fileReceive

while True:
    header = fileReceive(sock, debug) # first recieves file's name
    if debug: print("rec'd: ", payload)
    if not payload:
        break
    else:
        fileName = header.decode() # convert to string by decoding bytes
        payload = fileReceive(sock, debug) # second recieves the payload (data in the file)
        wrtieFile = open(os.getcwd()+"/serverFiles/"+fileName, 'wb')
        wrtieFile.write(data)
        wrtieFile.close()  # write the new file and close it
        print("complete")
