import socket
import threading

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
            self.send_message(self.username, "a rejoint.")
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            print("Erreur de connexion au serveur:", str(e))

    def send_message(self, username, message):
        try:
            message = f"{username},{message}"
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
                print("Erreur lors de la réception du message:", str(e))
                break

    def disconnect(self):
        self.socket.close()
