#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction,Position

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyPythonBot")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map
    width = game_map.width
    height = game_map.height
    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []
    info_halite = []
    #reset
    for ship in me.get_ships():
        logging.info(f'my ship: {ship.owner}')
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        myowner = ship.owner
        for i in range(0, height + 1):
            for j in range(0, width + 1):
                new_position = Position(j,i)

                myowner = ship.owner
                if game_map[new_position].is_occupied:
                    enemy_ship = -1 #it is an enemy ship
                    if game_map[new_position].ship.owner == myowner:
                        enemy_ship = 1 #it is not an enemy ship or in other words, it's our ship!

                if game_map[new_position].has_structure:
                    enemy_dropoff = -1 #it is an enemy ship
                    logging.info(f"structure owner: {game_map[new_position].structure.owner}")
                    if game_map[new_position].structure.owner == myowner:
                        enemy_dropoff = 1
                         #it is not an enemy ship or in other words, it's our dropoff!
                        info_halite.append((new_position,game_map[new_position].halite_amount,enemy_ship,enemy_dropoff)) #i didn't put the new position because cv2 didnt work
                        enemy_ship = 0 #reset the value to neutral
                        enemy_dropoff = 0

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
