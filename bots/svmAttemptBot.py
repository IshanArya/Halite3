import sklearn
import numpy as np
import hlt
from hlt.positionals import Position,Direction
from hlt import constants
import logging
import random
import os
from collections import OrderedDict
#'/Users/bharddwajvemulapalli/Documents/Halite_project/Halite3_Python_MacOS/Halite3/replays/replay-20181028-124932-0400-1540745368-32-32.hlt',"bharddwaj"
VERSION = 1
game = hlt.Game()
game.ready(f"bharddwaj-AI-Bot{VERSION}")

ship_plans = {} #keep track of plans for the ship
if os.path.exists("c{}_input.vec".format(VERSION)):
    os.remove("c{}_input.vec".format(VERSION))

if os.path.exists("c{}_out.vec".format(VERSION)):
    os.remove("c{}_out.vec".format(VERSION))
#logging.info(f"Width: {game_map.width}")
#logging.info(f"Height: {game_map.height}")
width = game.game_map.width
height = game.game_map.height
while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []
    team_ships = me.get_ships()
    enemy_ship_ids = []
    enemy_shipyard_map_cells = []
    enemy_shipyard_positions = []
    #not sure which kind i need tbh
    number_of_enemy_ships = 0
    for i in range(-width,width+1):
        for j in range(-height,height+1):
            some_position = Position(i,j)
            if game_map[some_position].is_occupied:
                enemy_ship_id = game_map[some_position].ship.id
                for aship in me.get_ships():
                    if aship.id != enemy_ship_id:
                        enemy_ship_ids.append(enemy_ship_id)
                        number_of_enemy_ships += 1
            elif game_map[some_position].has_structure and game_map[some_position] != game_map[me.shipyard.position]:
                enemy_shipyard_map_cells.append(game_map[some_position])
                enemy_shipyard_positions.append(some_position)
    number_of_friendly_ships = len(team_ships)

    #starter python code lmao
    for ship in me.get_ships():
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            command_queue.append(
                ship.move(
                    random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ])))
        else:
            command_queue.append(ship.stay_still())

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
