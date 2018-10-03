#! /usr/bin/env python3

import sys
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
    payload = fileReceive(sock, debug) # first payload is files name
    if debug: print("rec'd: ", payload)
    if not payload:
        break
    else:
        fileName = payload.decode() # convert to string by decoding bytes
        data = fileReceive(sock, debug) # second payload is the data in the file
        wrtieFile = open('new_'+fileName, 'wb')
        wrtieFile.write(data)
        wrtieFile.close()  # write the new file and close it
        print("complete")
