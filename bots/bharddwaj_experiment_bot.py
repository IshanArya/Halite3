# import sklearn
import numpy as np
import hlt
from hlt.positionals import Position,Direction
from hlt import constants
import logging
import random
import os
import math
game = hlt.Game()
game.ready("bharddwaj-experiment-bot")
logging.info("bharddwaj-experiment-bot")
width = game.game_map.width
height = game.game_map.height
turn = 0
while True:
    turn += 1
    game.update_frame()
    me = game.me
    game_map = game.game_map
    halite_amount_based_dict = {}
    command_queue = []
    ''' for i in range(0,32):
            for j in range(0,32):
                if game_map[Position(i,j)].is_occupied:
                    enemy_ship = True
                    for ship in me.get_ships():
                        if ship.position == Position(i,j):
                            enemy_ship = False
                        logging.info(f"Ship Owner: {ship.owner}")
                    logging.info(f"Enemy Ship: {enemy_ship}") '''
    list_of_information = []
    enemy_ship = 0 #neutral value
    enemy_dropoff = 0
    dropoffs = list(me.get_dropoffs()) + [me.shipyard]
    for ship in me.get_ships():
        for i in range(-6,7):
            for j in range(-6,7):
                new_position = ship.position + Position(j,i)
                halite_amount = round(game_map[new_position].halite_amount/constants.MAX_HALITE,2)
                if game_map[new_position].is_occupied:
                    enemy_ship = -1 #it is an enemy ship
                    for ship in me.get_ships():
                        if ship.position == Position(i,j):
                            enemy_ship = 1 #it is not an enemy ship or in other words, it's our ship!
                if game_map[new_position].has_structure:
                    enemy_dropoff = -1 #it is an enemy ship
                    for dropoff in dropoffs:
                        if dropoff.position == Position(i,j):
                            enemy_dropoff = 1 #it is not an enemy ship or in other words, it's our dropoff!
                list_of_information.append((new_position,halite_amount,enemy_ship,enemy_dropoff))
                enemy_ship = 0 #reset the value to neutral
                enemy_dropoff = 0 #reset
        logging.info(list_of_information)
        if game.turn_number == 5:
            with open("test.txt","w") as f:
                f.write(str(list_of_information))
        np.save(f"game_play/{game.turn_number}.npy",list_of_information)
        command_queue.append(ship.move(Direction.North))
    if len(me.get_ships())<1:
        command_queue.append(me.shipyard.spawn())
        logging.info("Ship has just been spawned")


    game.end_turn(command_queue)
