"""
Collection of useful functions
"""
import numpy as np


def available_moves(grid, empty):
    """
    Return the location of any empty cells on the grid i.e. valid moves
    """
    return np.where(grid == empty)[0]