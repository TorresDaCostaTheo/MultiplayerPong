import json
from shutil import ExecError
import signal
import socket
import sys
import threading
from time import sleep
from typing import Any

from game.Game import State,Game
from game.Player import Player


class ServerGameSocket(threading.Thread):

    def __init__(self,port:int) -> None:
        super(ServerGameSocket,self).__init__(target=self.run)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind(('',port))
        self.__socket.listen(1)
        self.__clients_socket:list[socket.socket] = []
        self.__game = Game.getInstance(server=self,callback=self.handleCallback) # type: ignore
        self.__game.thread.start()
        
        print("ServerGameSocket created")
        signal.signal(signal.SIGINT, self.quit) # type: ignore
        signal.signal(signal.SIGTERM, self.quit) # type: ignore
    def quit(self):
        self.__socket.close()
    def run(self):
        print("Server is running")
        while True:
            print("Waiting for client")
            try:
                (client_socket,client_address) =self.__socket.accept()
                print("Client accepted"+str(client_address))
            except:
                print("Error while accepting client")
                sys.exit(1)
            
            self.__clients_socket.append(client_socket) 
            print(f"New client connected {client_address}")
            client_thread = ClientGameThread(self,client_socket,client_address)
            client_thread.start()
            if self.__game.state == State.ENDED:
                print("Finishing server")
                break
            sleep(0.5)
    
    def handleSendMessage(self):
        for client_socket in self.__clients_socket:
            client_socket.send(self.__game.__str__().encode())
        pass
    def remove_socket(self,socket:socket.socket):
        self.__clients_socket.remove(socket)
        pass
    def handleCallback(self):
        print("Callback")
        pass
    @property
    def game(self):
        return self.__game
    @property
    def clients_socket(self):
        return self.__clients_socket

class ClientGameThread(threading.Thread):
    def __init__(self,server:ServerGameSocket,socket_data,address) -> None:
        super(ClientGameThread,self).__init__()
        self.__server = server
        self.__socket:socket.socket = socket_data
        self.__listening = True
        self.__address = address
        print("Client thread created")
    def run(self):
        print("Starting client thread for ",self.__address)
        while self.__listening:
            data = ""
            try :
                data = self.__socket.recv(1024).decode()
                self.handleMessage(data)
            except Exception as e: 
                print(f"Error while receiving data from client \n {e}")
                self.quit()
            sleep(0.1)
        print("Ending client thread for ",self.__address)
    def send(self,data:Any):
        self.__socket.sendall(data.encode())
    def handleMessage(self,data):
        print(data)
        if data is None:
            return
        try:
            decodeData =self.decodeJSON(data)
            self.isJoinTag(decodeData)
            pass
        except ExecError as exc:
            print(f"Error while decoding JSON \n {exc}")
        pass
    def isJoinTag(self,decodeData:Any):
         if decodeData['player'] is not None:
                print(decodeData['player'])
                if(decodeData['player']['join'] == True):
                    name:str = decodeData['player']['namePlayer']
                    id = 0
                    if(id == 1):
                        id = 1
                    elif(id == 2):
                        id = 2
                    player = Player(id,name,self.__address)
                    if(self.__server.game.joinPlayer(player)):
                        self.send("valid")
                    print(player.__str__())
                    pass
                elif(decodeData['player']['quit'] == True):
                    id:int = decodeData['player']['id']
                    self.__server.game.quit(id)
    def isQuitTag(self,decodeData):
        if decodeData['player'] is not None:
            if(decodeData['player']['quit'] == True):
                id:int = decodeData['player']['id']
                self.__server.game.quit(id)
        pass
    def isMoveTag(self,decodeData):
        if decodeData['player'] is not None:
            if(decodeData['player']['move']):
                id:int = decodeData['player']['id']
                y:int = decodeData['player']['y']
                
        pass
    def quit(self):
        self.__listening = False
        self.__socket.close()
        self.__server.remove_socket(self.__socket)
        pass
    def decodeJSON(self,data):
        obj =json.loads(data)
        return obj