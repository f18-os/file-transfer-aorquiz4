#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from fileSock import fileSend, fileReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

path = os.getcwd()+"/serverFiles"
try:  
    os.mkdir(path)
except OSError: 
    print ("Creation of the directory %s failed" % path)
else:  
    print ("Created the directory %s " % path)

# Get file info
fileName = ''
print("Enter File for transfer (only puts file, does not get): ")
fileName = input()

newPath = path+"/"+fileName

if os.path.exists(newPath):
    print("File already exists on server.")
    sys.exit()

# Read file
if '.txt' in fileName: # handles text files, read as string and decoded into bytes
    header = str.encode(fileName)
    try:
        file = open(fileName, 'r') # reading text file
    except FileNotFoundError: # if the file doesn't exist don't run
        print(fileName+" does not exist.")
        print("Exiting program...")
        sys.exit(0)
    
    print("Transferring %s to default location on server." % (fileName))
    
    statinfo = os.stat(fileName) # checking the size of file

    if statinfo:
        print("Size of file (in bytes): %s" % (statinfo.st_size)) 
    else:
        print("File is of size zero (empty file).") # if size is zero then dont continue because file is empty.
        print("Exiting program...")
        sys.exit(0)

    readFile = file.read()
    readFile = readFile.replace('\n', '\0')
    readFile = readFile.encode()
    fileSend(s, header) # send file name
    fileSend(s, readFile) # send the data 
else:                                       # handles other file types, read as bytes
    header = str.encode(fileName)

    try:
        file = open(fileName, 'rb') # read that jpg's and exe's are read in bytes
    except FileNotFoundError:
        print(fileName+" does not exist.")
        print("Exiting program...")
        sys.exit(0)

    print("Transferring %s to default location on server." % (fileName))
    
    statinfo = os.stat(fileName) # checking the size of file

    if statinfo:
        print("Size of file (in bytes): %s" % (statinfo.st_size)) 
    else:
        print("File is of size zero (empty file).") # if size is zero then dont continue because file is empty.
        print("Exiting program...")
        sys.exit(0)

    readFile = file.read()
    fileSend(s, header) # send file name
    fileSend(s, readFile, debug) # send the data
