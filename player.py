"""
Code for the different types of player or agents
"""
import numpy as np
import utils
import logging


class Player:
    def __init__(self, identifier='R'):
        self.identifier = identifier  # The identifier for this player in the grid

    def get_identifier(self):
        return self.identifier


class RandomAgent(Player):
    def __init__(self, identifier='R'):
        self.identifier = identifier

    @staticmethod
    def choose_move(params):
        """
        Return a random valid move
        """
        logging.debug("Test: params; " + str(params))
        available_moves = utils.available_moves(params['grid'], params['empty_cell'])
        logging.debug("Test: available_moves: " + str(available_moves))
        return np.random.choice(available_moves, size=1)[0]


class Human(Player):
    def __init__(self, identifier='H'):
        self.identifier = identifier

    @staticmethod
    def choose_move(params):
        width = params['width']
        user_move = input("Please enter your move - row number, column number e.g. 1,1\n")
        # Extract out the row and column numbers
        tmp = user_move.replace(" ", "").split(",")
        # Convert it into a cell index for the grid when it is squashed into a 1-D array
        return int(tmp[0]) * width + int(tmp[1])

