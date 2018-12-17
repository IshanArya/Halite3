# import sklearn
import numpy as np
import hlt
import secrets
from hlt.positionals import Position,Direction
from hlt import constants
import logging
import random
import os
import math
import time


game = hlt.Game()
game.ready("bharddwaj-experiment-bot")
logging.info("bharddwaj-experiment-bot")
width = game.game_map.width
height = game.game_map.height

TOTAL_TURNS = 50
SAVE_THRESHHOLD = 4300
MAX_SHIPS = 1
RADIUS = 16
direction_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]

training_data = []
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
        for i in range(-RADIUS,RADIUS+1):
            for j in range(-RADIUS,RADIUS+1):
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
                list_of_information.append([halite_amount,enemy_ship,enemy_dropoff]) #i didn't put the new position because cv2 didnt work
                enemy_ship = 0 #reset the value to neutral
                enemy_dropoff = 0 #reset
            logging.info(list_of_information)
            choice = secrets.choice(range(len(direction_order)))
            training_data.append([list_of_information,choice])
        command_queue.append(ship.move(direction_order[choice]))
    if game.turn_number == TOTAL_TURNS:
        if me.halite_amount > SAVE_THRESHHOLD:
            np.save(f"‎⁨Macintosh HD⁩/Users⁩/bharddwajvemulapalli⁩/⁨Documents/Halite_project⁩/Halite3_Python3_MacOS⁩/Halite3⁩/mlstuff⁩/training_data/{me.halite_amount}-{int(time.time()*1000)}.npy",training_data)
    if len(me.get_ships()) < MAX_SHIPS :
        command_queue.append(me.shipyard.spawn())
        logging.info("Ship has just been spawned")


    game.end_turn(command_queue)
