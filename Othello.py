# Author: Aubrey Floyd
# GitHub username: aubreyfloyd2
# Description: Program to function as the two-player text-based game, Othello. Two players take turns placing
#              their colored pieces on a 8x8 board with the objective of capturing the opponent's pieces and
#              having the majority of their pieces on the board at the end of the game.
#              Program has two classes: Player and Othello.


class Player:
    """Player Class represents a player in the game, parameters are a name and color.
    Used by the Othello class for players.
    """

    def __init__(self, player_name, color):
        """Initialize private data members: player name and color of player"""
        self._player_name = player_name  # string
        self._color = color  # string "black" or "white"


    def get_player_name(self):
        """Get method to be used for calling the player's name in the Othello class."""
        return self._player_name


    def get_color(self):
        """Get method to be used for calling the player's color in the Othello class."""
        return self._color


class Othello:
    """Othello class to represent the two person text-based game of Othello.
     Uses Player Class for its two players.

     The game board is represented by a 10x10 grid with symbols:
     Edge: * (star), Black piece: X, White piece: O, Empty space: . (dot)
     """

    def __init__(self):
        """Initialize private data members: game board to starting player positions,
        with game edges, and an empty player list. Takes no parameters.
        Board and players will be used through all functions to play game.
        """
        # initialize board positions as either edge or empty position
        self._board = [["*" if (i == 0 or i == 9 or j == 0 or j == 9) else "." for i in range(10)] for j in range(10)]
        # place colored X and O starting positions
        self._board[4][4] = "O"
        self._board[5][5] = "O"
        self._board[4][5] = "X"
        self._board[5][4] = "X"
        self._players = []  # initialize empty player list


    def print_board(self):
        """Prints out the current 10x10 board, including the edges. Takes no parameters.
        Uses the Othello board.
        """
        for row in self._board[0:10]:
            print(" ".join(row[0:10]))


    def create_player(self, player_name, color):
        """Creates a player object with parameters of the player's given name and color
        and adds the player to the player list. Uses Player Class and player list.
        """
        player = Player(player_name, color)
        self._players.append(player)


    def return_winner(self):
        """Returns a message with the winner of the game. Takes no parameters.
        Finds winner or tie by counting colored pieces and returning the winner as the player
        with the most colored pieces on the game board. Uses board and player list.
        """
        black_count = 0
        white_count = 0

        # iterate over 8x8 game board to count
        for row in range(1,9):
            for col in range(1,9):
                if self._board[row][col] == "X":
                    black_count += 1
                elif self._board[row][col] == "O":
                    white_count += 1

        black_player = None
        white_player = None

        # find the player's name for the player's color
        for player in self._players:
            if player.get_color() == "black":
                black_player = player
            elif player.get_color() == "white":
                white_player = player

        if black_count > white_count:
            return "Winner is black player: " + black_player.get_player_name()
        elif white_count > black_count:
            return "Winner is white player: " + white_player.get_player_name()
        else:
            return "It's a tie"


    def return_available_positions(self, color):
        """Returns a list of possible positions for the player with the given color
        to move on current board. Takes color as a parameter. Uses board and valid_move.
        """
        available_positions = []

        # iterate over game board
        for row in range(1,9):
            for col in range(1,9):
                if self._board[row][col] == ".":  # if empty
                    # if self.flip_pieces(row, col, color) != []:  # check if valid move
                    if self.valid_move(row, col, color) == True:
                        available_positions.append((row, col))
        return available_positions


    def valid_move(self, row, col, color):
        """Checks if a possible move at the given position for the given color is valid.
        Returns True if the move is valid or False if invalid.
        Used by return_available_positions.
        """
        # check all 8 possible move directions
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

        if color == "black":
            symbol = "X"
            opponent_symbol = "O"
        else:  # if color is "white"
            symbol = "O"
            opponent_symbol = "X"

        if self._board[row][col] != ".":  # if not empty
            return False

        for move in directions:
            move_row, move_col = move
            current_row, current_col = row + move_row, col + move_col

            # check if current row and column are within valid range
            if 1 <= current_row <= 8 and 1 <= current_col <= 8:
                # check adjacent piece for opponent's symbol
                if self._board[current_row][current_col] == opponent_symbol:
                    current_row += move_row
                    current_col += move_col

                    # continue direction until reach a piece in player's color or empty space
                    while 1 <= current_row <= 8 and 1 <= current_col <= 8:
                        if self._board[current_row][current_col] == symbol:
                            return True
                        elif self._board[current_row][current_col] == opponent_symbol:
                            current_row += move_row
                            current_col += move_col
                        elif self._board[current_row][current_col] == ".":
                            break
        return False


    def make_move(self, color, piece_position):
        """Puts a player's colored piece on a specific position of the board and updates the board accordingly.
        Takes color and piece position as parameters. Calls flip_pieces to check and flip opponent pieces.
        Returns 2D list of current board. Called by play_game method.
        """
        row, col = piece_position

        if color == "black":
            symbol = "X"
        else:  # if color is "white"
            symbol = "O"
        self._board[row][col] = symbol  # place X or O on board

        self.flip_pieces(row, col, color)  # check directions and flip pieces

        return self._board


    def flip_pieces(self, row, col, color):
        """Called by make_move. Checks all 8 possible directions for opponent pieces to flip
        in a line that ends with the current player's color.
        Flips opponent colored pieces if captured by opponent's colored piece move in make_move.
        """
        # check all 8 possible move directions
        directions = [(0,1), (1,1), (1,0), (1,-1), (0,-1),(-1,-1), (-1,0), (-1,1)]

        if color == "black":
            symbol = "X"
            opponent_symbol = "O"
        else:  # if color is "white"
            symbol = "O"
            opponent_symbol = "X"

        for move in directions:
            move_row, move_col = move
            current_row, current_col = row + move_row, col + move_col
            flip_list = []  # initialize for each direction

            # check if current row and column are within valid range
            if 1 <= current_row <= 8 and 1 <= current_col <= 8:
                # check adjacent piece for opponent's symbol for possible flip
                if self._board[current_row][current_col] == opponent_symbol:
                    flip_list.append((current_row, current_col))
                    current_row += move_row
                    current_col += move_col

                    # continue direction until reach a piece in player's color
                    while 1 <= current_row <= 8 and 1 <= current_col <= 8:
                        if self._board[current_row][current_col] == symbol:
                            # flip captured opponent's pieces
                            for flip_row, flip_col in flip_list:
                                self._board[flip_row][flip_col] = symbol
                            break
                        if self._board[current_row][current_col] == ".":  # check if empty
                            break
                        if self._board[current_row][current_col] == "*":  # check if edge
                            break
                        if self._board[current_row][current_col] == opponent_symbol:  # check if player's symbol
                            flip_list.append((current_row, current_col))
                            current_row += move_row
                            current_col += move_col


    def play_game(self, player_color, piece_position):
        """Checks available positions using return_available_positions.
        If valid it moves and updates by calling make_move method.
        If not valid returns possible positions to move.
        Checks if game is over. If game is over, returns winner with return_winner.
        """
        available_positions = self.return_available_positions(player_color)

        if piece_position not in available_positions:
            print("Here are the valid moves: ", available_positions)
            return "Invalid move"

        else:
            self.make_move(player_color, piece_position)

        # check if game is over; if over return winner
        if not self.return_available_positions("X") and not self.return_available_positions("O"):
            black_count = 0
            white_count = 0

            # iterate over 8x8 game board to count
            for row in range(1, 9):
                for col in range(1, 9):
                    if self._board[row][col] == "X":
                        black_count += 1
                    elif self._board[row][col] == "O":
                        white_count += 1
            print("Game is ended white piece: " + str(white_count) + "  black piece: " + str(black_count))
            return self.return_winner()
