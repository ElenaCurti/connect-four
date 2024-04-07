'Chat Room Connection - Client-To-Client'
import threading
import socket
from player import *
import traceback
import os
import shutil

def disconnect_all_users():
    """Function that disconnects all users"""
    all_socket = get_all_socket()
    for s in all_socket:
        s.close()

def manda_mess(client, messaggio):
    """Function that sends a message to a client and stores the message in the log file"""
    assert isinstance(messaggio, str), "Message should be of type string"
    assert isinstance(client, socket.socket), "client should be of type socket.socket"

    if client != None:
        client.send(messaggio.encode('utf-8'))
        with open(log_file, "a") as file:
            file.write(str(client) + "\tOUT >\t" + messaggio + "\n")

    
def handle_client(client):
    """Function to handle clients'connections"""
    while True:
        try:
            if client.fileno() == -1: # Client closed it's connection
                client.close()
                break 
            
            message = str(client.recv(1024).decode())
            if message == "":
                client.close()
                break 
            
            with open(log_file, "a") as file:
                file.write(str(client) + "\tIN  <\t" + message + "\n")
            
            if message.startswith("[new_player] "): 
                # A new player joined the game. 
                alias = message[13:]
                
                # I check that the chosen name is univoque... 
                print("A new player attempted to play with name", alias,"\tResult:",  end="")
                if player_exists(alias):
                    manda_mess(client, "[no]")
                    print("Refused!")
                    continue
                
                add_player(alias, client)
                manda_mess(client, "[ok]")
                print("OK!")

                # ... and I seek for an adversary (if any)
                avversario_name = find_adversary_for_player(alias)
                if avversario_name != None:
                    # If there is an adversary, I pair the current player with him/her
                    client_adv = set_adversary(alias, avversario_name)                    
                    print(alias, "will play against", avversario_name)
                    
                    manda_mess(client, "[new_game] 1 " + avversario_name)     # If in the message there is 1 -> it's the adversary's turn
                    manda_mess(client_adv, "[new_game] 0 " + alias)           # If in the message there is 0 -> it's the players' turn. 
                else:
                    # If there isn't an adversary, i communicate to the client to wait
                    print(alias, "is waiting for a new player")
                    manda_mess(client, "[wait_player]")

            elif message.startswith("[new_move] "):
                # If a player made a move, the server will communicate it to the adversary
                alias_player = message[13:]
                client_adv = get_adversary_socket_from_player_name(alias_player) 
                manda_mess(client_adv, message)
            elif message.startswith("[end_game] "):
                # If the match ended, the server will communicate it to the adversary and the players are removed 
                alias_player = message[11:]
                get_player_socket(alias_player).close()
                get_adversary_socket_from_player_name(alias_player).close()

                remove_player_and_adversary(alias_player)
            
            elif message.startswith("[left_game] "):
                # If a player abandon the game, the server will communicate it to the adversary and the players are removed
                alias_player = message[12:]
                client_adv = get_adversary_socket_from_player_name(alias_player)
                manda_mess(client_adv, message)
                client_adv.close()
                client.close()
                remove_player_and_adversary(alias_player)
                
        except Exception as e:
            if client.fileno() == -1:
                client.close()
            break


def check_received_new_connection():
    """Main function to receive the clients connection"""
    while True:
        try:
            client, address = server.accept()
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
        except TimeoutError:
            try:
                print("", end="") # nop
            except KeyboardInterrupt:
                print("Server closed")
                disconnect_all_users()
                exit(1)

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 3000
    
    # Creation of the listening socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4. Bidirectional, reliable, sequenced, and unduplicated flow of data without record
    server.settimeout(1)            # Timeout is necessary to check if user wants to terminate the server using CTRL+C
    server.bind((host, port))
    server.listen()

    # I reset the log directory and create a log file for the server
    LOG_DIR = "log"
    if os.path.exists(LOG_DIR):
        shutil.rmtree(LOG_DIR)
    os.makedirs(LOG_DIR)

    log_file = LOG_DIR+"/server_log.txt"
    with open(log_file, "w") as file:
        file.write("")

    # Server running
    print('Server is running and listening. To shutdown press CRTL+C ...')
    check_received_new_connection()
