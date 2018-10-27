#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction
#from hlt.entity import Entity,Shipyard

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
logging.info("this is the bot that collects halite if its over 0")
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
    directions_chosen = [] #creating this list and gonna add a bunch of positions so other ships cant simultaneously go to the same position resulting in collision
    ship_is_full_counter = 0
    for ship in me.get_ships():
        logging.info("For Loop has begun")
        
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        logging.info(f"Ship Halite Amount: {ship.halite_amount}")
        if ship.halite_amount > 900:
            ship_is_full_counter = 1
        if ship_is_full_counter > 0:
            '''
            I should actually do a different conditional where if the ship is full then a counter's value will go up.
            And if that counter value goes up then these commands will take place because what's happening is there is a Loop
            because ships use halite to move leading to the else statement being triggered and when ship reaches max it triggers
            the if ship.is_full statement. using a counter should negate this loop.
            '''
            logging.info("is this condition even happening?")
            surrounding_cardinals_full_ship = ship.position.get_surrounding_cardinals()
            cardinals = []
            counter_for_positions_with_shipyard = 0
            for cardinal_position in surrounding_cardinals_full_ship:
                logging.info(f"There is a Shipyard True or False? Ans: {game_map[cardinal_position].has_structure}")
                if game_map[cardinal_position].has_structure:
                    logging.info(f"Type of structure: {game_map[cardinal_position].structure_type}")
                    logging.info(f"The structure is at position: {cardinal_position} or if that doesn't log properly it might be {game_map[cardinal_position]}")
                    #just to see if shipyard actually shows up at the present location
                    cardinals.append(cardinal_position)
                    cardinal_position_with_shipyard = cardinal_position
                    counter_for_positions_with_shipyard += 1
                else:
                    cardinals.append(cardinal_position) #gonna just add the normal cardinal position
                    #using numbers as opposed to string to see if it'll work
            logging.info(f"List of Cardinal Positions: {cardinals}")
            logging.info(f"Counter For Positions With Shipyard: {counter_for_positions_with_shipyard}")
            if counter_for_positions_with_shipyard > 0 and len(cardinals) > 0:
                if len(shipyard_waiting_line) == 0:
                    logging.info("Ship is right next to the shipyard and is about to attempt going in!!")
                    for i in range(0,len(cardinals)):
                        if cardinals[i] == cardinal_position_with_shipyard:
                            if i == 0:
                                    shipyard_waiting_line.append("ship is going into the shipyard")
                                    command_queue.append(ship.move(Direction.North))
                                    ship_is_full_counter == 0
                            elif i == 1:
                                    shipyard_waiting_line.append("ship is going into the shipyard")
                                    command_queue.append(ship.move(Direction.South))
                                    ship_is_full_counter == 0
                            elif i == 2:
                                    shipyard_waiting_line.append("ship is going into the shipyard")
                                    command_queue.append(ship.move(Direction.East))
                                    ship_is_full_counter == 0
                            elif i == 3:
                                    shipyard_waiting_line.append("ship is going into the shipyard")
                                    command_queue.append(ship.move(Direction.West))
                                    ship_is_full_counter == 0
                else:
                    logging.info("Ship is currently waiting to go into the shipyard to deposit halites")
                    command_queue.append(ship.stay_still())
            else:
                naive_direction = game_map.naive_navigate(ship, me.shipyard.position)
                command_queue.append(ship.move(naive_direction))
                #this command alone apparently doesn't allow the ship to go into the shipyard
                logging.info(f"Ship is full and command_queue has appended the {naive_direction}")
        elif ship_is_full_counter == 0 or me.shipyard.position == ship.position:
            #if the position the ship is on has halite then the ship should stay there and collect the halite
            if game_map[ship.position].halite_amount > 0: #changed to constant from 0
                logging.info(f"Ship is collecting {game_map[ship.position].halite_amount} halite")
                command_queue.append(ship.stay_still())
            else:
                #This portion checks the surrounding cardinals and whichever one has the most halite, that's the direction the ship will go in
                all_positions_are_taken_up = 0 #this variable is in case all positions for the max halite conditional are taken up
                surrounding_cardinals = ship.position.get_surrounding_cardinals()
                halite_amounts = []
                for cardinal_position in surrounding_cardinals:
                    if not game_map[cardinal_position].is_occupied:
                        halite_amounts.append(game_map[cardinal_position].halite_amount)
                    else:
                        #Because in the next step I am selecting based on index values from order, I have to include some element as not to mess it up
                        halite_amounts.append(0)
                        #had to append 0 here because the max function wouldn't work if I appended a string
                #order is north, south, east, west
                copy_halite_amounts_list = halite_amounts.copy()
                max_halite_amount = max(halite_amounts)
                if max_halite_amount != 0:
                    for i in range(0,len(halite_amounts)):
                        logging.info(f"Length of halite_amounts: {len(halite_amounts)}")
                        logging.info(f"{i}") #to see how im getting an index out of bounds error
                        if max_halite_amount == halite_amounts[i]:
                            #cardinal_index = i
                            if not surrounding_cardinals[i] in directions_chosen:
                                #will only go to that position if it's not in the list of directions
                                    directions_chosen.append(surrounding_cardinals[i])
                                    command_queue.append(ship.move(game_map.naive_navigate(ship,surrounding_cardinals[i])))
                                    break #added breaks in case there are multiple 'maxes' so that way multiple commands won't be added

                            else:
                                if len(copy_halite_amounts_list) > 0:
                                    #so if the position with the max halite amount is already in the directions_chosen list
                                    del(copy_halite_amounts_list[i])
                                    #use del to remove a specific index as opposed to remove which removes the first sighting of the value in the list
                                    #we need specific index because that is the specific position that is taken
                                    max_halite_amount = max(copy_halite_amounts_list)
                                    logging.info(f"Length of copy_halite_amounts_list after deletion: {len(copy_halite_amounts_list)}")
                                    logging.info(f"Length of halite_amounts after deletion: {len(halite_amounts)}")
                                else:
                                    all_positions_are_taken_up = 1
                    logging.info(f"max_halite_amount: {max_halite_amount}, the ship has moved to that direction and has collected the halite there")
                elif max_halite_amount == 0:
                    logging.info(f"All Positions are taken up if all_positions_are_taken_up equals one and it equals: {all_positions_are_taken_up} ")
                    logging.info(f"Because max_halite_amount: {max_halite_amount}, the ship will move to a random cardinal")
                    #have to limit the random so that ships don't go into the same block as others
                    surrounding_cardinals = ship.position.get_surrounding_cardinals()
                    possible_choices = []

                    #possible_choices_no_ships = 0
                    for cardinal_position in surrounding_cardinals:
                        #if not game_map[cardinal_position].is_occupied:
                            #only add choices where there is no ship
                            possible_choices.append(cardinal_position)
                            #possible_choices_no_ships += 1
                        #else:
                            #Because in the next step I am selecting based on index values from order, I have to include some element as not to mess it up
                            #possible_choices.append(314159)
                            #had to use int because getting type error when checking condition later on
                            #based on the choice move accordingly
                            #order is north, south, east, west
                    #logging.info(f"Possible Choices No Ships Value: {possible_choices_no_ships}")
                    #if possible_choices_no_ships > 0:
                    choice = random.randrange(0,len(possible_choices))
                    all_positions_are_taken_up_counter = 0
                    all_positions_are_taken_up_list = []
                    while (possible_choices[choice] not in surrounding_cardinals and possible_choices[choice] in directions_chosen and game_map[possible_choices[choice]].is_occupied) or all_positions_are_taken_up_counter == 0:
                        #guaranteed to get a choice that will result in the ship moving into a spot that is not occupied and a spot that another ship is not in the process of moving into
                        #if choice randomly goes through all possible locations then the loop will break
                        choice = random.randrange(0,len(possible_choices))
                        all_positions_are_taken_up_list.append(choice)

                        if 0 in all_positions_are_taken_up_list and 1 in all_positions_are_taken_up_list and 2 in all_positions_are_taken_up_list and 3 in all_positions_are_taken_up_list:
                            #there is always going to be 4 indexes
                            all_positions_are_taken_up_counter = 1

                    if all_positions_are_taken_up_counter == 0:
                        directions_chosen.append(surrounding_cardinals[possible_choices[choice]])
                        command_queue.append(ship.move(game_map.naive_navigate(ship,possible_choices[choice])))

                    #logging.info(f"Length of Possible Choices: {possible_choices}, and Random Choice: {choice}") #this is causing an error for some reason
                    elif all_positions_are_taken_up_counter == 1: #possible choices are 0 don't move the ship or spawn anymore ships just yet
                        logging.info(f"Length of Possible Choices: {possible_choices}, so the ship has decided to stay still")
                        ship.stay_still()
                        #don't want to move the ship or else it'll collide
                        too_many_ships += 1
                        logging.info(f"too_many_ships value: {too_many_ships}")
                        #using this variable so that I know not to spawn anymore ships

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    logging.info(f"this value is right above the if statement too_many_ships value: {too_many_ships}")
    if len(me.get_ships()) == 0:
        ship_counter = 0
    if game.turn_number <= 350 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied and too_many_ships == 0 and ship_counter < 4:
        logging.info("Spawning Ships")
        command_queue.append(me.shipyard.spawn())
        ship_counter += 1 #using a counter because the 5th ship is just staying still for some reason
        logging.info(f"Current Ship Counter: {ship_counter}")

    # Send your moves back to the game environment, ending this turn.
    too_many_ships = 0
    game.end_turn(command_queue)
