"""
                                                                                      Hung Nguyen
Description: set up a server for client connection as they traverse through the directories
"""
import socket
import os
import pickle
import threading
import sys

#Store Client paths and change directories
def changeDirectory(path,user):
    #user1 = f"\{user}"
    #d = str(path+user1)
    d = os.path.join(path,user)
    print(d)
    try:
        os.chdir(d)
    except:
        return path
    return os.getcwd()

#list files/directories under a directory
def listFiles(userpath):
    os.chdir(userpath)
    L = os.listdir()
    return(L)

#walk through all directories and subdirectories
def listDirectories(userPath):
    L = []
    os.chdir(userPath)
    for (path, dirList, fileList) in os.walk(userPath):
        for d in dirList:
            L.append(os.path.join(path, d))
    return L

#handles client requests
def talkClient(conn,addr,path):

        conn.send(f'Current directory: {path}'.encode('utf-8'))
        connection = True
        userPath = path

        while connection:
            conn.send('c. change directory \nf. show files \nd. show directories \nq. quit'.encode('utf-8'))
            fromClient = conn.recv(1024).decode('utf-8')
            if fromClient == 'q':
                print(f"Connection to  {addr} closed")
                connection = False
            elif fromClient == 'f':
                msg = f'files found under {userPath}'
                conn.send(msg.encode('utf-8'))

                L = listFiles(userPath)

                if (len(L) != 0):
                    data = pickle.dumps(L)
                    conn.send(data)
                else:
                    msg = f'No files found under {os.getcwd()}'
                    data = pickle.dumps(msg)
                    conn.send(data)


            elif fromClient == 'c':
                user = conn.recv(1024).decode('utf-8')


                test = changeDirectory(userPath,user)
                msg = f'New path: {test}'

                if userPath == test:
                    msg = 'None found'
                    conn.send(msg.encode('utf-8'))
                else:
                    userPath = test
                    msg = f'New path: {test}'
                    conn.send(msg.encode('utf-8'))


            elif fromClient == 'd':
                msg = f'Directories found under {userPath}'
                conn.send(msg.encode('utf-8'))
                # os.chdir('..')
                L = listDirectories(userPath)
                data = pickle.dumps(L)
                conn.send(data)
            else:
                conn.send('try again'.encode('utf-8'))
        conn.close()
        popUser()

def popUser():
    lists.pop()

#handles command lines arguments
if len(sys.argv) == 3:
    if ((int(sys.argv[1]) <5) and  ((int(sys.argv[2]) <200) and (int(sys.argv[2])>3))):
        clientAmount = int(sys.argv[1])
        timer = int(sys.argv[2])
        # print(clientAmount)
        # print(timer)
    else:
        print('error on one of the condition')
else:
    print('usage: filename  number_of_clients time_for_timer  ')
    sys.exit()

HOST = "localhost"
PORT = 5551
lists = []

os.chdir('D:\Advanced Python\labs\lab5')

try:
    with socket.socket() as s :
            s.bind((HOST, PORT))
            print("Server hostname:", HOST, "port:", PORT)
            s.listen()
            run = True
            lists = []
            counter = 0
            for i in range(clientAmount):
                try:
                   s.settimeout(timer)
                   if(run == True):
                       (conn, addr) = s.accept()
                       counter +=1
                       path = 'D:\Advanced Python\labs\lab5'
                       # conn.send('0'.encode('utf-8'))
                       newClientThread = threading.Thread(target=talkClient, args=(conn, addr, path))
                       newClientThread.start()
                       lists.append(newClientThread)
                       print(f'Number of Clients: {threading.activeCount() - 1}')
                except socket.timeout:
                    run = False
                    print(f'{timer} seconds is up, closing {clientAmount-counter} unused')
                    for i in range(counter+1,clientAmount+1):
                        print(f"Closing client {i}")
            for i in lists:
                i.join()
except:
    for i in lists:
        i.join()
    quit(1)

