from socket import *



s = socket (AF_INET, SOCK_STREAM)
s.bind(('0.0.0.0', 5050)) # bind to the port
s.listen(1) # listen for incoming connections

try:
    while True:
        print('Server is listening...')
        conn, addr = s.accept() # accept the connection
        print('Connected by', addr) # print the address of the client
        # receive data from the client
        while True:
            data = conn.recv(1024) # receive the data
            print('Received data:', data.decode()) # print the received data
            # if not data: break 
            conn.send(data+ b"*") # send the response
except KeyboardInterrupt:
    print("Server stopped by user")
finally:
    #conn.close()
    s.close()

