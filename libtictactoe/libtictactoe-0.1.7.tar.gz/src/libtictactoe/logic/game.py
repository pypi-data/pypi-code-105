import copy
import enum
from libtictactoe.cursesUI import constants as const


class GameLogic:
    """ Class of logic game
    """

    class Cell(enum.Enum):
        EMPTY = " "
        CH_X = "X"
        CH_O = "O"

        def __str__(self):
            return f'{self.value}'

    def __init__(self):
        self.x_pos = 1             # x position in matrix
        self.y_pos = 1             # y position in matrix
        self.count_moves = 0       # total of moves make along game
        self.board_game = [[self.Cell.EMPTY.__str__()] * const.NUM_COLUMNS for _ in range(const.NUM_LINES)]
        self.game_states = []      # all game states of one game
        self.player_flag = False   # flag to know the player's turn
        self.end_game = False      # flag to find out if the game has come to an end

    def update_player(self) -> None:
        """ Updates which player to play """
        self.player_flag = not self.player_flag

    def has_victory(self) -> bool:
        """ Check if player has victory """
        return (
                (self.board_game[0][self.x_pos] == self.board_game[1][self.x_pos] == self.board_game[2][self.x_pos]) # check horizontal line
                or (self.board_game[self.y_pos][0] == self.board_game[self.y_pos][1] == self.board_game[self.y_pos][2])# check vertical line
                or (self.x_pos == self.y_pos and self.board_game[0][0] == self.board_game[1][1] == self.board_game[2][2])# check diagonal
                or (self.x_pos + self.y_pos == 2 and self.board_game[0][2] == self.board_game[1][1] == self.board_game[2][0])# check diagonal
        )

    def has_draw(self) -> bool:
        """ Check if it is a draw """
        return (
            self.count_moves == const.MAX_MOVES
        )

    def move(self) -> None:
        """ Make each move in game. """
        # Validates if the move can be done (empty cell)
        if self.board_game[self.y_pos][self.x_pos] == self.Cell.EMPTY.__str__():
            # Play the new move
            self.board_game[self.y_pos][self.x_pos] = (
                self.Cell.CH_O.__str__()
                if self.player_flag
                else self.Cell.CH_X.__str__()
            )
            # Update the number of moves
            self.count_moves += 1
            # Save each game state
            self.game_states.append(copy.deepcopy(self.board_game))
            # Check if the game have result for end game
            if self.has_victory() or self.has_draw():
                self.end_game = True
            # Switch player
            if self.end_game is False:
                self.update_player()

    def update_input_positions(self, key) -> None:
        """ Update the game for each movement input key """
        if key == const.KEY_UP:
            self.y_pos = max(0, self.y_pos - 1)
        elif key == const.KEY_DOWN:
            self.y_pos = min(2, self.y_pos + 1)
        elif key == const.KEY_LEFT:
            self.x_pos = max(0, self.x_pos - 1)
        elif key == const.KEY_RIGHT:
            self.x_pos = min(2, self.x_pos + 1)

    def update_input(self, key) -> None:
        """ Update the game for input key """
        if key in const.KEY_QUIT:
            self.end_game = True
        elif key == const.KEY_MOVE:
            self.move()
        else:
            self.update_input_positions(key=key)
