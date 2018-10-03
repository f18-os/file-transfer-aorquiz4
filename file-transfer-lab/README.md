# file-transfer-aorquiz4
tcp file transfer with stammerproxy, and multiple clients

File `fileServer.py` is a simple tcp file server

File `fileClient.py` is a simple tcp file client

File `fileSock.py` is a simple tcp socket creator for sending and recieving files

Directory `lib` includes the params package required for many of the programs

Directory `stammer-proxy` (/nets-tcp-framed-echo/stammer-proxy/) includes stammerProxy, which is useful for demonstrating and testing framing

*   `stammerProxy.py` forwards tcp streams. It may delay the transmission of data but ensures all data will be forwarded, eventually.
   By default,
   it listens on port 50000 and forwards to localhost:50001.  Use the -?
   option for help. To run use `./fileClient.py -s 127.0.0.1:50000`. This connects client to proxy which the forwards to localhost:50001.

File `fileForkServer.py` is code that works simillarly to fileServer.py except it allows for multiple clients

* FramedForkServer uses `fork()` to handle multiple simultaneous clients.    

*  The -? (usage) option prints parameters and default values. 


To run:
* Simple file server and client run and execute the following commands on seperate terminals. Once running `fileClient.py` will ask for a file name.

$ ./fileServer.py

$ ./fileClient.py


* With stammer-proxy it's the same as above but first run `stammerProxy.py`. One different is when running client. Again each command in a seperate terminal.
	$ ./stammerProxy.py
	$ ./fileServer.py
	$ ./fileClient -s 127.0.0.1:50000

* With multiple clients use 'fileForkServer.py' with the server and client. Each command in seperate terminal.
	$ ./fileForkServer.py
	$ ./fileServer.py
	$ ./fileClient.py

