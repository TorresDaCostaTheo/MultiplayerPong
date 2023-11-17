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

    def add_values_to_json(self,nomJoueur,playerYFac,pause):
        json_file_path = "./src/client/socket/data.json"

        # Charger le JSON existant
        try:
            with open(json_file_path, 'r') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            # Si le fichier n'existe pas, initialiser avec une structure de base
            existing_data = {"Players": []}

        # Ajouter les nouvelles valeurs
        existing_data["Players"][0]["namePlayer"] = nomJoueur
        existing_data["Players"][0]["playerYFac"] = playerYFac
        existing_data["Players"][0]["pause"] = pause
    
        # Réécrire le fichier JSON avec les données mises à jour
        with open(json_file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=2)

    def read_data_from_json(self):
        json_file_path = "./src/client/socket/data.json"
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        return data


    def send_message(self,nomJoueur,playerYFac,pause):
        try:
            # Écrire les données dans le fichier JSON
            self.add_values_to_json(nomJoueur,playerYFac,pause)

            # Lire les données à partir du fichier JSON
            dataJson = self.read_data_from_json()

            # Convertir le dictionnaire JSON en une chaîne JSON
            json_data = json.dumps(dataJson)

            # Ajouter un caractère de nouvelle ligne après chaque message JSON
            message = f"{json_data}\n"
        
            # Envoi du nom d'utilisateur et des données JSON
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
