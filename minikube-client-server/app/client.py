from socket import *
from time import sleep
import os

import argparse

args = argparse.ArgumentParser(description='Client for socket communication')       
args.add_argument('-p', '--port', type=int, default=5050, help='Port number to connect to') 
args.add_argument('-m', '--msg', type=str, default="Hello_world!", help='Message to send') 

# args.parse_args()
args = args.parse_args()
s = socket (AF_INET, SOCK_STREAM)

SERVER_URL = os.getenv('SERVER_URL')

s.connect((SERVER_URL, args.port)) # connect to server (block until accepted)

# receive the response

# send some data
while True:
    s.send (f'{args.msg}'.encode()) # send some data
    data = s.recv(1024) # receive the data
    print('Received data:', data.decode()) # print the received data
    #if not data: break 
    s.send(data+ b"*") # send the response
    # print the received data
    data = s.recv(1024)#* receive the response
    print("data:", data) # print the received data
    sleep(1)
# print the result
# s.close()
# close the connection
