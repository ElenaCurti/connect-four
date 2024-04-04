import threading
import socket
import os
from ForzaQuattro import ConnectFour
import re

def manda_mess(messaggio):
    """
    Function that send message to the server and also saves them in a file.
    """
    global log_file, buffer_to_write_before_creating_log_file
    assert isinstance(messaggio, str), "Message should be of type string"

    global client
    try:
        client.send(messaggio.encode('utf-8'))
        if "log_file" in globals():
            with open(log_file, "a") as file:
                file.write("OUT > " + messaggio + "\n")
        else:
            buffer_to_write_before_creating_log_file += "OUT > " + messaggio + "\n"
        
    except ConnectionResetError:
        print("Connection closed by server")
        exit(1)


def nuovo_turno(colonna=-1):
    """
    Function that represent a game turn. 
    An input equal to -1 represents the player's turn, so the program will ask the user to make a move.
    If the input is not -1, it will be interepreted as the adversary's move, so the program will memorize it.
    In both cases, anyway, the scoreboard will be updated accordingly and if the game ends, the program will stop.
    """
    global client, game, alias

    if colonna == -1: 
        print("It's your turn! You are player: " +game.get_colored_symbol_player())
        num_ok = False
        while not num_ok:
            try:
                colonna = int(input(f"Enter your move (1-7): "))
                if game.is_valid_move(colonna):
                    manda_mess("[new_move] " + str(colonna) +  " " + alias )
                    num_ok = True
                else:
                    print("Invalid move. Try again.")
                
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\nYou abandoned the game :( ")
                manda_mess("[left_game] " + alias)
                client.close()
                exit(0)
    
    if game.is_valid_move(colonna):
        game.make_move(colonna)
    
    if game.check_winner():
        game.print_board(alias, avversario)

        print(f"Player {ConnectFour.get_colored_symbol(game.current_player)} won!")
        
        if game.current_player == game.symbol_player:
            print("\nYOU WON!! :) :)" )
            manda_mess("[end_game] " + alias)
        else:
            print("\nYou lose  :( :(") 
        
        client.close()
        exit(0)

    game.switch_player()
    game.print_board(alias, avversario)



if __name__ == "__main__":

    buffer_to_write_before_creating_log_file = ""
    game = None
    
    # I check the connection with the server
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 3000))
    except ConnectionRefusedError:
        print("Connection closed by server")
        exit(1)

    # User must first choose an univoque valid name
    pattern = re.compile(r'^[a-zA-Z0-9]+$')
    alias = input('Choose a name (only letters and numbers are allowed. Maximum supported length is 20) >>> ')
    while True:
        if len(alias) <= 20 and pattern.match(alias):
            manda_mess("[new_player] " + alias)
            messaggio = client.recv(1024).decode('utf-8')
            buffer_to_write_before_creating_log_file += "IN  < " + messaggio + "\n"
            if messaggio == "[ok]":
                break
        
        print("\nError. The chosen name can't be used. It might be already used or it might contain unsupported characters (only letters and numbers are allowed).") 
        alias = input("Please choose a different name >>> ")

    # I initialize a log file
    log_file = "log/log_client_"+alias+".txt"
    with open(log_file, "w") as file:
        file.write(buffer_to_write_before_creating_log_file)

    # I listen the incoming messages and act accordingly
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            with open(log_file, "a") as file:
                file.write("IN  < " + message + "\n")
            
            if message == "[wait_player]":
                print("Waiting for a new player to join the game...")
            
            elif message.startswith("[new_game] "): 
                turno = int(message[11])
                avversario = message[13:]
                
                game = ConnectFour(turno)
                game.print_board(alias, avversario)
                
                print("A new game started! You are player: " + alias + ". Your adversary is:",  avversario)
                if turno == 0:
                    nuovo_turno(-1)
                
                print("You are player: ", game.get_colored_symbol_player())
                print("It's your adversary's turn! Waiting for his/her move...")
                

            elif message.startswith("[new_move] "):
                # Adversary's move
                colonna_scelta = int(message[11])
                nuovo_turno(colonna_scelta) # Adeversary's move
                nuovo_turno(-1)             # User's move
                print("You are player: ", game.get_colored_symbol_player())
                print("It's your adversary's turn! Waiting for his/her move...")

            elif message.startswith("[left_game] "):
                print("Your adversary abandoned the game.\nYou win! :)")
                client.close()
                exit(0)

        except ConnectionResetError:
            print("Connection closed by server")
            exit(1)
        except KeyError:
            print('Connection closed by user!')
            client.close()
            break
