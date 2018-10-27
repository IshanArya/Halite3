#!/usr/bin/env python

# Import the Halite SDK, which will let you interact with the game.
import hlt
from hlt import constants

import random
import logging


# This game object contains the initial game state.
game = hlt.Game()
# Respond with your name.
game.ready("Ishan's Awesome Bot")

max_number_of_ships = 1
ship_status = {}

while True:
    # Get the latest game state.
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn.
    command_queue = []

    for ship in me.get_ships():
        

        # End Game - navigate ship to shipyard
        distanceToShipyard = game_map.calculate_distance(ship.position, me.shipyard.position)
        if constants.MAX_TURNS - game.turn_number < distanceToShipyard + 3:
            logging.info("Ship is moving to shipyard with {} turns left.".format(constants.MAX_TURNS - game.turn_number))
            logging.info("Distance to shipyard: {}".format(distanceToShipyard))
            move = game_map.naive_navigate(ship, me.shipyard.position)
            command_queue.append(ship.move(move))
            continue

        logging.info("Ship {} has {} halite.".format(ship.id, ship.halite_amount))
        
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            command_queue.append(
                ship.move(random.choice(["n", "s", "e", "w"])))
        else:
            command_queue.append(ship.stay_still())

    # If you're on the first turn and have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though.
    if len(me.get_ships()) < max_number_of_ships and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(game.me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
    