'Chat Room Connection - Client-To-Client'
import threading
import socket

host = '127.0.0.1'
port = 3000


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(5)    # Il timeout serve per capire se si vuole interrompere il server
server.bind((host, port))
server.listen()

# Dict of clients (key = name of the player, value = client socket)
clients = {}

# List of players' names. It's a list of tuple of players. Every player in the same tuple is playing in the same match
aliases = []


def broadcast(message):
    for client in clients:
        client.send(message)


def sconnetti_tutti():
    global clients, aliases
    for client in clients:
        client.close()
    aliases = []
    clients = {}


def search_tuple_list(tuple_list, target):
    mapping_dict = {key: value for key, value in tuple_list}
    reverse_mapping_dict = {value: key for key, value in tuple_list}
    
    if target in mapping_dict:
        return mapping_dict[target]
    elif target in reverse_mapping_dict:
        return reverse_mapping_dict[target]
    else:
        return None

def handle_client(client):
    # Function to handle clients'connections
    while True:
        try:
            message = str(client.recv(1024).decode())
            print(message)
            if message.startswith("[new_player] "): 
                # A new player joined the game. I check that name is univoque... 
                alias = message[13:]

                print("A new player attempted to play with name", alias,"\tResult:",  end="")
                if clients.keys().__contains__(alias):
                    client.send("[no]".encode())
                    print("Refused!")
                    continue
                
                client.send("[ok]".encode())
                clients[alias] = client
                print("OK!")

                # ... and I seek for an adversary (if any)
                if len(aliases) >0 and len(aliases[-1]) == 1:
                    avversario = aliases[-1][0]
                    print(alias, "will play against", avversario)
                    aliases[-1] = (avversario, alias)
                    clients[avversario].send(("[new_game] 0 " + alias).encode()) # If in the message there is 0 -> it's the players' turn. 
                    clients[alias].send(("[new_game] 1 " + avversario).encode()) # Otherwise -> it's the adversary's turn
                else:
                    print(alias, "is waiting for a new player")
                    aliases.append((alias,))
                    clients[alias].send(("[wait_player]").encode())

            elif message.startswith("[new_move] "):
                alias_player = message[13:]
                alias_avversario = search_tuple_list(aliases, alias_player)
                clients[alias_avversario].send(message.encode())
            elif message.startswith("[end_game] "):
                alias_player = message[11:]
                alias_avversario = search_tuple_list(aliases, alias_player)
                clients.pop(alias_player, None)
                clients.pop(alias_avversario, None)
                # TODO rimuovi anche dagli aliases
            

            # broadcast(message)
        except:
            index = clients[client]
            clients.pop(client, None) # FIX questo
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break
# Main function to receive the clients connection


def check_received_new_connection():
    while True:
        try:
            client, address = server.accept()
            # print(f'connection is established with {str(address)}')
            
            # client.send('[player_name]'.encode('utf-8'))
            # alias = client.recv(1024)
            # if aliases.__contains__(alias):
            #     client.send('[NO]'.encode('utf-8'))
            #     continue
            # else:
            #     client.send('[OK]'.encode('utf-8'))

            # aliases.append(alias)
            # clients.append(client)
            
            # print(f'The alias of this client is {alias}'.encode('utf-8'))
            # broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
            # client.send('you are now connected!'.encode('utf-8'))
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
        except TimeoutError:
            try:
                print("", end="") # nop
            except KeyboardInterrupt:
                print("Fine")
                sconnetti_tutti()
                exit(1)

if __name__ == "__main__":
    print('Server is running and listening ...')
    check_received_new_connection()
