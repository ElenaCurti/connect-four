'Chat Room Connection - Client-To-Client'
import threading
import socket
from player import *
import traceback

host = '127.0.0.1'
port = 3000


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(1)    # Il timeout serve per capire se si vuole interrompere il server
server.bind((host, port))
server.listen()

log_file = "log/server_log.txt"
with open(log_file, "w") as file:
    file.write("")

# Dict of clients (key = name of the player, value = client socket)
# clients = {}

# List of players' names. It's a list of tuple of players. Every player in the same tuple is playing in the same match
# aliases = []


def sconnetti_tutti():
    all_socket = get_all_socket()
    for s in all_socket:
        s.close()
    


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
            if client.fileno() == -1:
                client.close()
                break # Fine thread per il client
            # print(f"{client=}")
            
            message = str(client.recv(1024).decode())
            with open(log_file, "a") as file:
                file.write(str(client) + "\t" + message + "\n")
            
            if message.startswith("[new_player] "): 
                # A new player joined the game. I check that name is univoque... 
                alias = message[13:]

                print("A new player attempted to play with name", alias,"\tResult:",  end="")
                if player_exists(alias):
                    client.send("[no]".encode())
                    print("Refused!")
                    continue
                
                add_player(alias, client)
                client.send("[ok]".encode())
                print("OK!")

                # ... and I seek for an adversary (if any)
                avversario_name = find_adversary_for_player(alias)
                if avversario_name != None:
                    client_adv = set_adversary(alias, avversario_name)                    
                    print(alias, "will play against", avversario_name)
                    
                    client.send(("[new_game] 1 " + avversario_name).encode()) # If in the message there is 0 -> it's the players' turn. 
                    client_adv.send(("[new_game] 0 " + alias).encode())       # If in the message there is 1 -> it's the adversary's turn
                else:
                    print(alias, "is waiting for a new player")
                    # aliases.append((alias,))
                    client.send(("[wait_player]").encode())

            elif message.startswith("[new_move] "):
                alias_player = message[13:]
                client_adv = get_adversary_socket_from_player_name(alias_player) 
                client_adv.send(message.encode())
            elif message.startswith("[end_game] "):
                alias_player = message[11:]
                get_player_socket(alias_player).close()
                get_adversary_socket_from_player_name(alias_player).close()

                remove_player_and_adversary(alias_player)
            
            elif message.startswith("[left_game] "):
                alias_player = message[12:]
                client_adv = get_adversary_socket_from_player_name(alias_player)
                client_adv.send(message.encode())
                client_adv.close()
                client.close()
                remove_player_and_adversary(alias_player)
                
            # broadcast(message)
        except Exception as e:
            if client.fileno() == -1:
                client.close()
            # Exception handling
            # print("An error occurred:")
            # traceback.print_exc()  #
            # print("Exception")
            # index = clients[client]
            # clients.pop(client, None) # FIX questo
            # client.close()
            # alias = aliases[index]
            # broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            # aliases.remove(alias)
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
                print("Server chiuso")
                sconnetti_tutti()
                exit(1)

if __name__ == "__main__":
    print('Server is running and listening ...')
    check_received_new_connection()
