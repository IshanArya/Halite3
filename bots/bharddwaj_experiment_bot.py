# import sklearn
import numpy as np
import hlt
from hlt.positionals import Position,Direction
from hlt import constants
import logging
import random
import os
from collections import OrderedDict
game = hlt.Game()
game.ready("bharddwaj-experiment-bot")
logging.info("bharddwaj-experiment-bot")
width = game.game_map.width
height = game.game_map.height

while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map
    halite_amount_for_all_cells = {}
    #list_of_information = []
    for i in range(int(-width/2),int(width/2)+1): #when i used -width and width + 1 here i didn't get an error for some reason
        for j in range(int(-height/2),int(height/2)+1):
            some_position = Position(i,j)
            halite_amount_for_all_cells[game_map[some_position].halite_amount] = some_position
    for ship in me.get_ships():
        logging.info("Looping among friendly ships has begun")
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())
        logging.info("Ship has just been spawned")
    game.end_turn(command_queue)
