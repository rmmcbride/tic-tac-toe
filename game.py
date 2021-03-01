# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12

@author: Rachael
"""
import numpy as np
import logging
import utils

invalid_moves_counter = 0


class Game:

    def __init__(self, grid_width, grid_height, players, order=None, empty_cell=' ', num_to_win=3, display_grid=True):
        self.width = grid_width
        self.height = grid_height
        self.grid = None
        self.players = players  # List of player objects
        self.player_order = order
        self.turns = players  # Same as self.players initially but will change as the game progresses
        self.empty = empty_cell
        self.to_win = num_to_win
        self.game_status = "Incomplete"
        self.winner = None
        self.max_invalid_moves = 2
        self.BUFFER = "==================================="  # For visual aesthetics
        self.display_grid = display_grid

    def get_current_game_state(self):
        """
        Used to inform players / agents of the current game state
        """
        return {
            'width': self.width,
            'height': self.height,
            'grid': self.grid,
            'empty_cell': self.empty
        }

    def setup_game(self):
        try:
            if self.width > 9 or self.height > 9:
                logging.critical("Game grid has a maximum height and a maximum width of 9")
            else:
                self.grid = np.array([' '] * (self.width * self.height))
            logging.info("Game set up")
        except Exception as e:
            logging.error("Error with setup_game " + str(e))

    def display(self):
        """
        Print the current grid
        """
        print(self.BUFFER)
        rearranged = self.grid.reshape(self.height, self.width)

        row_buffer = "--" * (self.width + 1)

        cols = [str(ind) for ind in range(self.width)]
        for row in range(len(rearranged)):
            if row == 0:
                print(" |" + "|".join(cols) + "|")
            print(row_buffer)
            curr = ''
            for col in range(len(rearranged[row])):
                if col == 0:
                    curr = str(row) + '|'
                curr = curr + str(rearranged[row][col]) + '|'
            print(curr)
        print(self.BUFFER)

    def is_valid_move(self, move):
        """
        Check if the proposed move is valid
        :param move: Proposed move
        :return: Boolean. True, if valid. False, if negative.
        """
        if move in utils.available_moves(self.grid, self.empty):
            return True
        else:
            return False

    def check_for_win(self):
        """
        Check for a winning move.

        Return the winning player if there is one. Otherwise, return None
        """
        try:
            of_interest = np.where(self.grid != self.empty)[0]

            for cell in of_interest:
                # check across
                if (cell + self.width) % self.to_win == 0:  # If there are enough cells to potentially win, check for a win
                    unique_contents = []
                    for ind in range(self.to_win):
                        unique_contents.append(self.grid[cell + ind])
                    if len(set(unique_contents)) == 1:  # If there is only one type of token or player in selection
                        print('Have a winner across')
                        logging.info('Have a winner across')
                        return unique_contents[0]
                # check down
                if cell + (self.width * self.to_win - 1) <= len(self.grid) - 1 :  # If there are enough cells to potentially win, check for a win
                    unique_contents = []
                    for ind in range(self.to_win):
                        unique_contents.append(self.grid[cell + self.height * ind])
                    if len(set(unique_contents)) == 1:  # If there is only one type of token or player in selection
                        print('Have a winner down')
                        logging.info('Have a winner down')
                        return unique_contents[0]
                # check the left diagonal
                # If there is enough space horizontally
                if int(cell / self.width) == int((cell + self.to_win - 1) / self.width):  # check if on the same row
                    # If there is enough space vertically
                    if (cell + self.to_win - 1) + (cell + self.to_win - 1) * self.height <= len(self.grid) - 1:
                        cnt = 1
                        unique_contents = []
                        curr = cell
                        while cnt <= self.to_win:
                            unique_contents.append(self.grid[curr])
                            curr = curr + self.width + 1
                            cnt += 1
                        if len(set(unique_contents)) == 1:  # If there is only one type of token or player in selection
                            print('Have a winner left diagonal')
                            logging.info('Have a winner left diagonal')
                            return unique_contents[0]
                # check the right diagonal
                # If there is enough space horizontally
                if int(cell / self.width) == int((cell - self.to_win) / self.width):  # check if on the same row
                    # If there is enough space vertically
                    if cell + self.width * (self.to_win - 1) - 1 <= len(self.grid):
                        cnt = 1
                        unique_contents = []
                        curr = cell
                        while cnt <= self.to_win:
                            unique_contents.append(self.grid[curr])
                            curr = curr + self.width - 1
                            cnt += 1
                        if len(set(unique_contents)) == 1:  # If there is only one type of token or player in selection
                            print('Have a winner right diagonal')
                            logging.info('Have a winner right diagonal')
                            return unique_contents[0]

            return None
        except Exception as e:
            logging.error("Error with check_for_win " + str(e))

    def is_end_game(self):
        try:
            is_win = self.check_for_win()
            if is_win is not None:
                self.game_status = "Finished"
            elif is_win is None and len(utils.available_moves(self.grid, self.empty)):
                self.game_status = "Incomplete"
            else:
                self.game_status = "Draw"
            logging.info("Game status checked")
            logging.info("Game status: " + self.game_status)
            self.winner = is_win
            return [self.game_status, self.winner]
        except Exception as e:
            logging.error("Error with setup_game " + str(e))

    def run(self):
        logging.info(self.BUFFER)

        # Set default values
        self.game_status = "Incomplete"
        winner = None
        self.setup_game()

        while self.game_status == "Incomplete" and winner is None:
            # Get the current player
            current_player = self.turns.pop(0)
            logging.info("Current player: " + str(current_player.get_identifier()))
            # Update turns to schedule the current player for another turn
            self.turns.append(current_player)
            # Get the next move and check if it is valid. If it is not, the player has 2 more goes to produce a 7
            # valid move. Otherwise, they forfeit the match.
            current_move = current_player.choose_move(self.get_current_game_state())
            invalid_moves_counter = 0
            while invalid_moves_counter <= self.max_invalid_moves and self.is_valid_move(current_move) is False:
                invalid_moves_counter += 1
                print("Invalid move. Please select another")
                current_move = current_player.choose_move(self.get_current_game_state())
            if self.is_valid_move(current_move) is True:
                self.grid[current_move] = current_player.get_identifier()
                if self.display_grid is True:
                    self.display()
                # check game status
                self.game_status, winner = self.is_end_game()
            else:
                logging.critical("Too many invalid moves in a row. You default the game")
                # Update the game status
                self.game_status = "Complete"
                winner = current_player.get_identifier()
        print("Status:", self.game_status)
        print("Winner:", winner)
        return self.game_status, winner

