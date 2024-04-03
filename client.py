import threading
import socket
import os
from ForzaQuattro import ConnectFour


def manda_mess(messaggio):
    assert isinstance(messaggio, str), "Message should be of type string"

    global client
    try:
        client.send(messaggio.encode('utf-8'))

    except ConnectionResetError:
        print("Connection closed by server")
        exit(1)

# L'utente sceglie il proprio nome e si connette
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 3000))
except ConnectionRefusedError:
    print("Connection closed by server")
    exit(1)

alias = input('Choose an alias >>> ')
manda_mess("[new_player] " + alias)
while client.recv(1024).decode('utf-8') != "[ok]":
    alias = input('Choose a different alias >>> ')
    manda_mess("[new_player] " + alias)

log_file = "log/log_client_"+alias+".txt"
with open(log_file, "w") as file:
    file.write("")

game = None


def nuovo_turno(colonna=-1):
    global client, game, alias

    turno_giocatore = colonna == -1
    if turno_giocatore: 
        print("It's your turn! You are player: " +game.get_colored_symbol_player())
        num_ok = False
        while not num_ok:
            try:
                colonna = int(input(f"Enter your move (1-7): "))
                if game.is_valid_move(colonna):
                    num_ok = True
                else:
                    print("Invalid move. Try again.")
                
            except ValueError:
                print("Invalid input. Please enter a number.")
            except EOFError or KeyboardInterrupt:
                print("\nYou abandoned the game :( ")
                manda_mess("[left_game] " + alias)
                client.close()
                exit(0)
    
    game.make_move(colonna)
    
    if turno_giocatore:
        manda_mess("[new_move] " + str(colonna) +  " " + alias )
    
    if game.check_winner():
        os.system('clear' if os.name == 'posix' else 'cls')
        game.print_board()
        print(f"Player {ConnectFour.get_colored_symbol(game.current_player)} won!")
        if game.current_player == game.symbol_player:
            print("\nYOU WON!! :) :)" )
            manda_mess("[end_game] " + alias)
        else:
            print("\nYou lose  :( :(\nWanna play again? ") # TODO
        client.close()
        exit(0)
    game.switch_player()

    os.system('clear' if os.name == 'posix' else 'cls')
    game.print_board()


    

    
if __name__ == "__main__":
    # global stop, game
    # Thread in ascolto dei messaggi arrivati
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            with open(log_file, "a") as file:
                file.write(message + "\n")
            if message == "[wait_player]":
                print("Waiting for a new player to join...")
            elif message.startswith("[new_game] "):
                turno = int(message[11])
                avversario = message[13:]
                
                game = ConnectFour(turno)
                game.print_board()
                
                print("A new game started! You are player: " + alias + ". Your adversary is:",  avversario)
                if turno == 0:
                    nuovo_turno(-1)
                
                print("You are player: ", game.get_colored_symbol_player())
                print("It's your adversary's turn! Waiting for his/her move...")
                

            elif message.startswith("[new_move] "):
                colonna_scelta = int(message[11])
                nuovo_turno(colonna_scelta)
                nuovo_turno(-1)
                print("You are player: ", game.get_colored_symbol_player())
                print("It's your adversary's turn! Waiting for his/her move...")

            elif message.startswith("[left_game] "):
                print("Your adversary abandoned the game.\nYou win! :)")
                client.close()
                exit(0)

                # game.print_board()
             
                

                
            # print(message)
        except ConnectionResetError:
            print("Connection closed by server")
            exit(1)
        except KeyError:
            
            print('Chiusura thread receive!')
            client.close()
            # if stop:
            #     client.close()
            # stop = False
            break


# def client_send():
#     global stop
#     # Thread per mandare messaggi
#     while True:
#         try:
#             message = f'{alias}: {input("")}'
#             client.send(message.encode('utf-8'))
#         except:
#             print('Chiusura thread send!')
#             if  stop:
#                 client.close()
#             stop = False
#             break

# stop = True 

# receive_thread = threading.Thread(target=client_receive)
# receive_thread.start()

# send_thread = threading.Thread(target=client_send)
# send_thread.start()

