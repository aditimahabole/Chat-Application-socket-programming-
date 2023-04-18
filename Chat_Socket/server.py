import socket 
import threading 
HOST = '127.0.0.1'
PORT = 8000
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
clients = []
player_names = []

#broadcast
def broadcast(message):
    for client in clients:
        client.send(message)
#handle
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{player_names[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            player_name = player_names[index]
            player_names.remove(player_name)
            break

#receive
def receive():
    print('receive')
    while True:
        client_socket,client_address = server.accept()
        print(f"Connected with {str(client_address)}!")
        client_socket.send('NICK'.encode('utf-8'))
        player_name = client_socket.recv(1024)
        player_names.append(player_name)

        clients.append(client_socket)
        print(f"Player Name : {player_name}")
        broadcast(f"{player_name} connected to the sever hehe!\n".encode('utf-8'))
        #sending message to this particular client
        client_socket.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target = handle, args = (client_socket, ))
        thread.start()
print("Server is running...")
receive()





