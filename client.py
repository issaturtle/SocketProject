"""
                                                                                      Hung Nguyen
Description: connect with the server to move through directories
"""
import socket
import pickle
import django


HOST = "localhost"
PORT = 5551
#creates a connection with the server, then choose which options
with socket.socket() as s:
    s.connect((HOST, PORT))
    print("Client connect to:", HOST, "port:", PORT)
    msg = s.recv(1024).decode('utf-8')
    if msg == '1':
        print('maxed client')
        s.close()
    else:
        print(msg)
        mesg = ''
        while mesg != 'q':
            msg = s.recv(1024).decode('utf-8')
            if msg == '1':
                 print('Connection failed, maxed clients')
                 s.close()
            print(msg)

            mesg = input("Enter choice: ")


            s.send(mesg.encode('utf-8'))
            if mesg == 'f':
                fromServer = s.recv(1024).decode('utf-8')
                print(fromServer)

                data = s.recv(4096)
                data = pickle.loads(data)
                if type(data) == list:
                    for i in data:
                        print(i)
                else:
                    print(data)

            elif mesg == 'd':
                fromServer = s.recv(1024).decode('utf-8')
                print(fromServer)
                data = s.recv(4096)
                data = pickle.loads(data)
                if len(data) != 0:
                    for i in data:
                        print(i)
                else:
                    print("None found")

            elif mesg == 'c':
                choice = input('Enter path, starting from current directory: ')
                s.send(choice.encode('utf-8'))
                fromServer = s.recv(2048).decode('utf-8')
                print(fromServer)
            else:
                print(s.recv(1024).decode('utf-8'))

