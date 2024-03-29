#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Position
#from hlt.entity import Entity,Ship

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
game.ready("bharddwaj")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))
logging.info("this is the file with the ship counter set less than 5")
""" <<<Game Loop>>> """
ship_counter = 0

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
    shipyard_waiting_line = []
    too_many_ships = 0
    directions_chosen = []  # creating this list and gonna add a bunch of positions so other ships cant simultaneously go to the same position resulting in collision
    ship_is_full_counter = 0
    logging.info("Outside of For Loop")
    for ship in me.get_ships():
        logging.info("For Loop has begun")
        logging.info(f"Ship: {ship}")
        logging.info(game_map[ship.position].ship)
        logging.info(f"The Map Cell Ship Position: {game_map[ship.position]}")
        logging.info(f"the true position of the ship: {ship.position}")
        number_of_enemy_ships = 0
        # reduced it to [-3,3] because [-4,4] didn't work, but i then changed it back again to 4 because i see a ship is inspired when one of the two enemy ships was four cells away
        backward_range = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        for i in backward_range:  # x coordinate
            for j in backward_range:  # y coordinate
                add_on = Position(i, j)
                no_add_on = Position(0, 0)
                if add_on != no_add_on:
                    if game_map[add_on.__add__(ship.position)].is_occupied:
                        if game_map.calculate_distance(ship.position, add_on.__add__(ship.position)) <= constants.INSPIRATION_RADIUS:
                            isEnemyShip = True
                            for aship in me.get_ships():
                                if aship == (game_map[add_on.__add__(ship.position)]).ship:
                                    isEnemyShip = False

                            if isEnemyShip:
                                number_of_enemy_ships += 1
                                if number_of_enemy_ships >= 2:
                                    break

        logging.info(f"Ship ID: {ship.id}")
        logging.info(
            f"Enemy Ship Counter within the Inspired Radius: {number_of_enemy_ships}")
        if number_of_enemy_ships >= 2:
            logging.info(f"The Ship is inspired, {game.turn_number}")

        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        logging.info(f"Ship ID: {ship.id}")
        logging.info(f"Ship Halite Amount: {ship.halite_amount}")
        if ship.halite_amount > 900:
            ship_is_full_counter = 1
        if ship_is_full_counter > 0:
            naive_direction = game_map.naive_navigate(
                ship, me.shipyard.position)
            command_queue.append(ship.move(naive_direction))
            #this command alone apparently doesn't allow the ship to go into the shipyard
            logging.info(
                f"Ship is full and command_queue has appended the {naive_direction}")
            ship_is_full_counter = 0
        elif ship_is_full_counter == 0 or me.shipyard.position == ship.position:
            #if the position the ship is on has halite then the ship should stay there and collect the halite
            # changed to constant from 0
            if game_map[ship.position].halite_amount > constants.MAX_HALITE/10:
                logging.info(
                    f"Ship is collecting {game_map[ship.position].halite_amount} halite")
                command_queue.append(ship.stay_still())
            else:
                #This portion checks the surrounding cardinals and whichever one has the most halite, that's the direction the ship will go in
                # this variable is in case all positions for the max halite conditional are taken up
                all_positions_are_taken_up = 0
                surrounding_cardinals = ship.position.get_surrounding_cardinals()
                halite_amounts = []
                for cardinal_position in surrounding_cardinals:
                    if not game_map[cardinal_position].is_occupied:
                        halite_amounts.append(
                            game_map[cardinal_position].halite_amount)
                    else:
                        #Because in the next step I am selecting based on index values from order, I have to include some element as not to mess it up
                        halite_amounts.append(0)
                        #had to append 0 here because the max function wouldn't work if I appended a string
                #order is north, south, east, west
                copy_halite_amounts_list = halite_amounts.copy()
                max_halite_amount = max(halite_amounts)
                # changed this from 0 to the max halite constant condition
                if max_halite_amount > game_map[ship.position].halite_amount:
                    for i in range(0, len(halite_amounts)):
                        logging.info(
                            f"Length of halite_amounts: {len(halite_amounts)}")
                        # to see how im getting an index out of bounds error
                        logging.info(f"{i}")
                        if max_halite_amount == halite_amounts[i]:
                            #cardinal_index = i
                            if not surrounding_cardinals[i] in directions_chosen:
                                #will only go to that position if it's not in the list of directions
                                    directions_chosen.append(
                                        surrounding_cardinals[i])
                                    command_queue.append(
                                        ship.move(game_map.naive_navigate(ship, surrounding_cardinals[i])))
                                    break  # added breaks in case there are multiple 'maxes' so that way multiple commands won't be added

                            else:
                                if len(copy_halite_amounts_list) > 0:
                                    #so if the position with the max halite amount is already in the directions_chosen list
                                    del(copy_halite_amounts_list[i])
                                    #use del to remove a specific index as opposed to remove which removes the first sighting of the value in the list
                                    #we need specific index because that is the specific position that is taken
                                    max_halite_amount = max(
                                        copy_halite_amounts_list)
                                    logging.info(
                                        f"Length of copy_halite_amounts_list after deletion: {len(copy_halite_amounts_list)}")
                                    logging.info(
                                        f"Length of halite_amounts after deletion: {len(halite_amounts)}")
                                else:
                                    all_positions_are_taken_up = 1
                    logging.info(
                        f"max_halite_amount: {max_halite_amount}, the ship has moved to that direction and has collected the halite there")
                else:
                    logging.info(
                        f"Ship is collecting {game_map[ship.position].halite_amount} halite")
                    command_queue.append(ship.stay_still())

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    logging.info(
        f"this value is right above the if statement too_many_ships value: {too_many_ships}")
    if len(me.get_ships()) == 0:
        ship_counter = 0
    if game.turn_number <= 350 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied and too_many_ships == 0 and ship_counter < 11:
        logging.info("Spawning Ships")
        command_queue.append(me.shipyard.spawn())
        # using a counter because the 5th ship is just staying still for some reason
        ship_counter += 1
        logging.info(f"Current Ship Counter: {ship_counter}")

    # Send your moves back to the game environment, ending this turn.
    too_many_ships = 0
    game.end_turn(command_queue)
