#!/usr/bin/env python3
#-*-coding:utf-8-*-

import socket
import sys
import signal
import time
import re 


ip = sys.argv[1]
regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)''' 
if re.search(regex, ip):  
    print("Adresse IP valide") 
else:  
    print("Adresse IP invalide")
    exit(0)

def signal_handler(sig, frame):
    connection_with_server.send("END".encode())
    print("Connexion fermée")
    connection_with_server.close()
    sys.exit(0)

host = ip
port = 4242

connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection_with_server.connect((host, port))
print(f"Connexion établie avec le serveur sur le {port}")

msg = b""
retry = 0
while msg != b"END" and retry < 5:
    retry = 0
    try:
        signal.signal(signal.SIGINT, signal_handler)
        msg = input("> ")
        msg = msg.encode()
        connection_with_server.send(msg)
        msg_rcv = connection_with_server.recv(1024)
        print(msg_rcv.decode())
    except BrokenPipeError:
        continue

print("Connexion fermée")
connection_with_server.close()