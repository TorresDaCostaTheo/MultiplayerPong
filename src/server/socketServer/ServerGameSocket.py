from enum import Enum
import json
from pydoc import plain
from shutil import ExecError
import signal
import socket
import sys
import threading
from time import sleep
from typing import Any

from game.Game import State,Game
from game.Player import Player
class EnumPlayerKey(Enum):
    JOIN = "join"
    QUIT = "quit"
    MOVE = "move"
    PLAYER = "Player"
    PLAYER_NAME = "namePlayer"
    def __str__(self) -> str:
        return self.value

class ServerGameSocket(threading.Thread):

    def __init__(self,port:int) -> None:
        super(ServerGameSocket,self).__init__(target=self.run)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind(('',port))
        self.__socket.listen(1)
        self.__clients_socket:list[socket.socket] = []
        self.__game = Game.getInstance(server=self,callback=self.handleCallback) # type: ignore
        self.__game.thread.start()
        self.__clients_thread:list[ClientGameThread] = []
        
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
            self.__clients_thread.append(client_thread)
            if self.__game.state == State.ENDED:
                break
            sleep(0.5)
    
    def handleSendMessage(self):
        for client_socket in self.__clients_socket:
            client_socket.send(self.__game.__str__().encode())
        pass
    def remove_socket(self,socket:socket.socket):
        self.__clients_socket.remove(socket)
        pass
    def handleCallback(self,data:Any):
        try:
            print(data)
            message =json.loads(data)
        
            if("receiver" in message):
                for client_socket in self.__clients_socket:
                    print(client_socket.getpeername().__str__())
                    if(message["receiver"] == client_socket.getpeername().__str__()):
                        del message["receiver"]
                        client_socket.sendall(json.dumps(message).encode())
            else:
                for client_socket in self.__clients_socket:
                    client_socket.sendall(json.dumps(message).encode())
            pass
        except:
            print("Error while sending message")
    @property
    def clients_thread(self):
        return self.__clients_thread
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
        self.__id = -1
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
        message ={
            "responseRequest": data
        }
        self.__socket.sendall(json.dumps(message).encode())
    def handleMessage(self,data):
        print(data)
        if data is None:
            return
        try:
            decodeData =self.decodeJSON(data)
            self.isJoinTag(decodeData)
            self.isQuitTag(decodeData)
            self.isMoveTag(decodeData)
            pass
        except ExecError as exc:
            print(f"Error while decoding JSON \n {exc}")
        pass
    def isJoinTag(self,decodeData:Any):
         if 'player' in decodeData:
                if(decodeData['player']['join'] == True):
                    name:str = decodeData['player']['namePlayer']
                    self.__id = self.attributeId()
                    player = Player(self.__id,name,self.__address)
                    for playerGame in self.__server.game.players:
                        if(self.__address == playerGame.address):
                            self.send(False)
                            return
                    if(self.__server.game.joinPlayer(player)):
                        self.send(True)
                    print(player.__str__())
    def isQuitTag(self,decodeData):
        if decodeData[EnumPlayerKey.PLAYER] is not None:
            if(decodeData[EnumPlayerKey.PLAYER]['quit'] == True):
                id:int = decodeData[EnumPlayerKey]['id']
                self.__server.game.quit(id)
        pass
    def isMoveTag(self,decodeData):
        if decodeData['player'] is not None:
            if(decodeData['player']['move']):
                id:int = decodeData['player']['id']
                playerYFac:int = decodeData['player']['playerYFac']
                for player in self.__server.game.players:
                    if(player.id == id):
                        player.striker.move(playerYFac)
                
        pass
    
    def quit(self):
        self.__listening = False
        self.__socket.close()
        self.__server.remove_socket(self.__socket)
        pass
    def decodeJSON(self,data):
        obj =json.loads(data)
        return obj
    def attributeId(self)->int:
        if self.__server.clients_thread.__len__() > 0:
            id = 0
            for client_thread in self.__server.clients_thread:
                if (id != client_thread.__id):
                    return id
                else:
                    id+=1
        return -1