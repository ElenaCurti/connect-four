class Player:
    def __init__(self, name):
        self.name = name                # Name of player
        self.socket = None              # Socket of player
        self.adversary = None           # Adversary's name
        self.adversary_socket = None    # Adversary's socket

# Dictionary to store players' information. (key = player name; value=relative Player class' object)
players = {}

def add_player(name, sock):
    """Funtion that memorizes the player and the relative socket"""
    if name not in players:
        players[name] = Player(name)
        players[name].socket = sock
    else:
        print("Player already exists.")

def remove_all_player():
    """Function that removes all memorized players"""
    for name in players.keys():
        del players[name]
    else:
        print("Player not found.")

def remove_player_and_adversary(name):
    """Function that removes a player and it's adversary (e.g. for the end of their game)"""
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
        
        print(f"Player {name} and {adversary_name} finished the game.")
    else:
        print("Player not found.")

def get_adversary_name(player_name):
    """Function that returns the adversary's name"""
    if player_name in players:
        adversary_name = players[player_name].adversary
        if adversary_name:  
            return adversary_name
    return None

def add_socket(name, sock):
    """Function to add socket for a player"""
    if name in players:
        players[name].socket = sock
    else:
        print("Player not found.")

def get_all_socket():
    """Function that return all memorized socket"""
    return [player.socket for player in players.values() if player.socket]
   

def get_player_socket(name):
    """Function to get a player's socket by name"""
    if name in players:
        return players[name].socket
    else:
        print("Player not found.")
        return None
    


def set_adversary(player_name, adversary_name):
    """ Function to set adversary's name"""
    if player_name in players and adversary_name in players:
        players[player_name].adversary = adversary_name
        players[player_name].adversary_socket = players[adversary_name].socket

        players[adversary_name].adversary = player_name
        players[adversary_name].adversary_socket = players[player_name].socket
        return players[player_name].adversary_socket
    else:
        print("One or both players not found.")
    return None


def player_exists(name):
    """Function to check if player's name already exists"""
    return name in players


def get_adversary_socket_from_player_socket(sock):
    for player in players.values():
        if player.socket == sock:
            if player.adversary:
                return players[player.adversary].adversary_socket
            else:
                return None
    return None

def get_adversary_socket_from_player_name(player_name):
    """Function to get the adversary's socket (by using the player's name)"""
    
    if player_name in players and players[player_name].adversary:
        return players[player_name].adversary_socket
    else:
        print("Player not found or player does not have an adversary.")
        return None


def find_adversary_for_player(player_name):
    """Function that checks if there is a player without an adversary"""
    for other_player_name, other_player in players.items():
        if player_name!= other_player_name and not other_player.adversary:
            return other_player_name
    return None
