import os

BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"

class ConnectFour:
    def __init__(self, turno):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        
        # self.symbol_player indicates the user's symbol
        if turno == 0:
            self.symbol_player = 'O'
        else:
            self.symbol_player = 'X'

        # By default, it always starts the player with 'O' symbol
        self.current_player = 'O'

    def get_colored_symbol(simbolo):
        if simbolo == 'X':
            return BLUE + "X" + RESET
        elif simbolo =='O':
            return RED + "O" + RESET
        else:
            return simbolo
    
    def get_colored_symbol_player(self):
        return ConnectFour.get_colored_symbol(self.symbol_player)
    
    
    def print_board(self, nome_player1, nome_player2):
        # Clear the terminal
        os.system('clear' if os.name == 'posix' else 'cls') 
        
        # Print player1 vs player2
        print(" "*35, end="")
        if self.symbol_player == 'X':
            print(f"{BLUE}({nome_player1}){RESET} vs {RED}({nome_player2}){RESET}")
        else:
            print(f"{RED}({nome_player1}){RESET} vs {BLUE}({nome_player2}){RESET}")

        # Print border and content of the scoreboard
        print("+" + "-" * 27 + "+")
        for row in self.board:
            print("| ", end="")
            for col in row:
                print(ConnectFour.get_colored_symbol(col), end=" | ")
            print()
        print("+" + "-" * 27 + "+", "\n  ", end="")

        # Print scoreboard index column
        for i in range(1,8):
            print(i, "  ", end="")
        print("\n")
        
    def is_valid_move(self, column):
        return 1 <= column <= 7 and self.board[0][column - 1] == ' '

    def make_move(self, column):
        for row in range(5, -1, -1):
            if self.board[row][column - 1] == ' ':
                self.board[row][column - 1] = self.current_player
                break

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        for row in range(6):
            for col in range(7):
                if self.board[row][col] != ' ':
                    # Check horizontally
                    if col + 3 < 7 and all(self.board[row][col + i] == self.current_player for i in range(4)):
                        return True
                    # Check vertically
                    if row + 3 < 6 and all(self.board[row + i][col] == self.current_player for i in range(4)):
                        return True
                    # Check diagonally (positive slope)
                    if row + 3 < 6 and col + 3 < 7 and all(self.board[row + i][col + i] == self.current_player for i in range(4)):
                        return True
                    # Check diagonally (negative slope)
                    if row - 3 >= 0 and col + 3 < 7 and all(self.board[row - i][col + i] == self.current_player for i in range(4)):
                        return True
        return False

# def main():
#     game = ConnectFour()

#     while True:
#         os.system('clear' if os.name == 'posix' else 'cls')
#         game.print_board()
#         try:
#             column = int(input(f"Player {game.current_player}, enter your move (1-7): "))
#         except ValueError:
#             print("Invalid input. Please enter a number.")
#             continue
        
#         if game.is_valid_move(column):
#             game.make_move(column)
#             if game.check_winner():
#                 os.system('clear' if os.name == 'posix' else 'cls')
#                 game.print_board()
#                 print(f"Player {game.current_player} wins!")
#                 break
#             game.switch_player()
#         else:
#             print("Invalid move. Try again.")

# if __name__ == "__main__":
#     main()
