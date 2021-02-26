import game
import player
import logging
logging.basicConfig(filename='tic_tac_toe.log', level=logging.DEBUG, filemode='w')

import numpy as np
GAME_RESULT_WEIGHTS = {'win': 1, 'lose': -1, 'draw': 0}
NUM_GAMES = 2

p1 = player.RandomAgent(identifier='R')
p2 = player.RandomAgent(identifier='V')#player.Human()
scores = {p1.get_identifier(): 0, p2.get_identifier(): 0}

for each in range(NUM_GAMES):
    print("Game number ", each + 1)
    g = game.Game(grid_width=3, grid_height=3, players=[p1, p2], order=np.random.choice([p1, p2], size=1)[0],
                  empty_cell=' ', num_to_win=3)

    status, winner = g.run()
    try:
        if status == "Finished":
            scores[winner] += GAME_RESULT_WEIGHTS['win']
            losers = set(scores.keys()) - set(winner)
            for loser in losers:
                scores[loser] += GAME_RESULT_WEIGHTS['lose']
        elif status == "Draw":
            for player in scores.keys():
                scores[player] += GAME_RESULT_WEIGHTS['draw']
        else:
            logging.CRITICAL("Invalid game status returned: " + str(status))
    except KeyError:
        logging.debug("Unexpected key: " + str(KeyError))



