import socket

class Player:
    def __init__(self, name):
        self.name = name
        self.socket = None
        self.adversary = None
        self.adversary_socket = None

# Dictionary to store players' information
players = {}

# Function to add a player
def add_player(name, sock):
    if name not in players:
        players[name] = Player(name)
        players[name].socket = sock
    else:
        print("Player already exists.")

# Function to remove all players
def remove_all_player():
    for name in players.keys():
        del players[name]
    else:
        print("Player not found.")

def remove_player_and_adversary(name):
    if name in players:
        adversary_name = players[name].adversary
        
        # Remove player and adversary from the dictionary
        del players[name]
        if adversary_name:            
            del players[adversary_name]
        
        # Reset adversary information for other players
        for player in players.values():
            if player.adversary == name:
                player.adversary = None
                player.adversary_socket = None
        
        print(f"Player {name} and {adversary_name} have been removed.")
    else:
        print("Player not found.")

def get_adversary_name(player_name):
    if player_name in players:
        adversary_name = players[player_name].adversary
        if adversary_name:  
            return adversary_name
    return None

# Function to add socket for a player
def add_socket(name, sock):
    if name in players:
        players[name].socket = sock
    else:
        print("Player not found.")

def get_all_socket():
    return [player.socket for player in players.values() if player.socket]
   


# Function to get a player's socket by name
def get_player_socket(name):
    if name in players:
        return players[name].socket
    else:
        print("Player not found.")
        return None
    

# Function to set adversary and adversary socket for a player
def set_adversary(player_name, adversary_name):
    if player_name in players and adversary_name in players:
        players[player_name].adversary = adversary_name
        players[player_name].adversary_socket = players[adversary_name].socket

        players[adversary_name].adversary = player_name
        players[adversary_name].adversary_socket = players[player_name].socket
        # print("avv")
        # print(players[player_name].adversary_socket)
        return players[player_name].adversary_socket
    else:
        print("One or both players not found.")
    return None


# Function to check if player's name already exists
def player_exists(name):
    return name in players


# Function to get the adversary's socket
def get_adversary_socket_from_player_socket(sock):
    for player in players.values():
        if player.socket == sock:
            if player.adversary:
                return players[player.adversary].adversary_socket
            else:
                return None
    return None

def get_adversary_socket_from_player_name(player_name):
    if player_name in players and players[player_name].adversary:
        # adversary_name = players[player_name].adversary
        return players[player_name].adversary_socket
    else:
        print("Player not found or player does not have an adversary.")
        return None


# Function that checks if there is a player without an adversary
def find_adversary_for_player(player_name):
    for other_player_name, other_player in players.items():
        if player_name!= other_player_name and not other_player.adversary:
            return other_player_name
    return None
