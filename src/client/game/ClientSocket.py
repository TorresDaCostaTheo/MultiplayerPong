import socket
import threading
import json

# Classe ClientSocket qui gère la communication avec le serveur
class ClientSocket:

    def __init__(self, username, server, port, callback):
        self.username = username
        self.server = server
        self.port = port
        self.callback = callback
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect((self.server, self.port))
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            print("Erreur de connexion au serveur:", str(e))

    def send_message(self, nomJoueur, playerYFac, pause,x,y):
            try:
                # Créer un dictionnaire avec les données du joueur
                player_data = {
                    "player":
                        {
                            "namePlayer": nomJoueur,
                            "playerYFac": playerYFac,
                            "pause": pause
                        }
                    ,"ball":
                        {
                         "x":x,
                         "y":y
                        }
                }

                # Convertir le dictionnaire en une chaîne JSON
                json_data = json.dumps(player_data)

                # Ajouter un caractère de nouvelle ligne après chaque message JSON
                message = f"{json_data}\n"

                # Envoi du message JSON
                self.socket.send(message.encode())
            except Exception as e:
                print("Erreur lors de l'envoi du message:", str(e))

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                message = data.decode()
                self.callback(message)
            except Exception as e:
                # print("Erreur lors de la réception du message:", str(e))
                break

    def sendMessage(self,nomJoueur,playerYFac):
        message = {
                "player":
                    {
                        "namePlayer": nomJoueur,
                        "playerYFac": playerYFac,
                        "join": True,
                    }
            }
        json_data = json.dumps(message)
        self.socket.send(json_data.encode())

    def disconnect(self):
        self.socket.close()
