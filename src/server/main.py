from socketServer.ServerGameSocket import ServerGameSocket
if(__name__ == "__main__"):
    server = ServerGameSocket(2100)
    server.start()
    server.join()