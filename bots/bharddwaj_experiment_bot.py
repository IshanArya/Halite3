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
turn = 0
while True:
    turn += 1
    game.update_frame()
    me = game.me
    game_map = game.game_map

    position_based_dict = {}
    halite_amount_based_dict = {}
    command_queue = []
    #list_of_information = []
    key_counter = 0
    iterations_for_below = 0 #delete this later
    for i in range(0,width):
        for j in range(0,height):
            iterations_for_below += 1
            list_of_information = []
            some_position = Position(i,j)
            list_of_information.append(game_map[some_position].halite_amount)
            if game_map[some_position].is_occupied:
                enemy_ship_id = game_map[some_position].ship.id
                for aship in me.get_ships():
                    if aship.id != enemy_ship_id:
                        list_of_information.append(enemy_ship_id) # if that position has a 1 there exists an enemy ship id
                        #number_of_enemy_ships += 1
            position_based_dict[str(some_position)] = list_of_information
            halite_amount_based_dict[key_counter] = [some_position] + list_of_information
            key_counter += 1 #had to use this as opposed to halite amount because one key cannot have more than one point
    list_of_ship_vision = [] #this is to fix issue delete later
    for ship in me.get_ships():
        ship_specific_list = [] #this info is specific to positions in a radius around the ship
        logging.info("Looping among friendly ships has begun")
        counter = 0 #see how many positions i get from the loop
        counter2 = 0 #this is a secondary counter for counting the if statements
        for i in range(0,6):
            for j in range(0,6):
                position_relative_to_ship_one = Position(i,j) + ship.position
                counter += 1
                position_relative_to_ship_two = Position(i,-j) + ship.position
                counter += 1
                position_relative_to_ship_three = Position(-i,j) + ship.position
                counter+=1
                position_relative_to_ship_four = Position(-i,-j) + ship.position
                counter+=1
                if not (i == 0 and j == 0):
                    counter2+= 1
                    list_of_ship_vision.append(position_relative_to_ship_one)
                    list_of_ship_vision.append(position_relative_to_ship_two)
                    list_of_ship_vision.append(position_relative_to_ship_three)
                    list_of_ship_vision.append(position_relative_to_ship_four)
                    for i in halite_amount_based_dict:
                        temp_list = []
                        if position_relative_to_ship_one == halite_amount_based_dict[i][0]:
                            #temp_list.append(position_relative_to_ship_one) #Position
                            temp_list.append((position_relative_to_ship_one,halite_amount_based_dict[i][1])) #append the halite amount
                            if len(halite_amount_based_dict[i]) > 2: #doing this to check to see if there is an enemy ship
                                the_list =halite_amount_based_dict[i]
                                temp_list.append(the_list[2]) # 0 1 2 the enemy ship thing would be the third item
                        temp_list2 = []
                        if position_relative_to_ship_two == halite_amount_based_dict[i][0]:
                            temp_list2.append((position_relative_to_ship_two,halite_amount_based_dict[i][1]))
                            if len(halite_amount_based_dict[i]) > 2:
                                the_list =halite_amount_based_dict[i]
                                temp_list2.append(the_list[2])
                        temp_list3 = []
                        if position_relative_to_ship_three == halite_amount_based_dict[i][0]:
                            temp_list3.append((position_relative_to_ship_three,halite_amount_based_dict[i][1]))
                            if len(halite_amount_based_dict[i]) > 2:
                                the_list =halite_amount_based_dict[i]
                                temp_list3.append(the_list[2])
                        temp_list4 = []
                        if position_relative_to_ship_four == halite_amount_based_dict[i][0]:
                            temp_list4.append((position_relative_to_ship_four,halite_amount_based_dict[i][1]))
                            if len(halite_amount_based_dict[i]) > 2:
                                the_list =halite_amount_based_dict[i]
                                temp_list4.append(the_list[2])
                        if not temp_list == []:
                            ship_specific_list.append(temp_list)
                        if not temp_list2 == []:
                            ship_specific_list.append(temp_list2)
                        if not temp_list3 == []:
                            ship_specific_list.append(temp_list3)
                        if not temp_list4 == []:
                            ship_specific_list.append(temp_list4)
                else:
                    counter2 += 1
                    if not ship.position in list_of_ship_vision: #adding this decreased the length from 51 to 25 for some reason
                        list_of_ship_vision.append(ship.position)
                        some_list = []
                        some_list.append((ship.position,game_map[ship.position].halite_amount))
                        ship_specific_list.append(some_list)
        #delete this loop later
        num_positions_in_dict = 0
        not_in_dict = []
        for i in list_of_ship_vision:
            for j in halite_amount_based_dict:
                if i == halite_amount_based_dict[j][0]:
                    num_positions_in_dict  += 1

                else:
                    not_in_dict.append(halite_amount_based_dict[j][0])


        logging.info(f'Length of Dictionary: {len(halite_amount_based_dict)}')
        logging.info(f"Width: {width}")
        logging.info(f"height: {height}")
        logging.info(f"iterations_for_below: {iterations_for_below} ")
        logging.info(f"Ship Specific List: {ship_specific_list}")
        logging.info(f"counter: {counter}")
        logging.info(f"counter2: {counter2}")
        logging.info(f"Length of the list: {len(ship_specific_list)}")
        logging.info(f"Length of Ship Vision: {len(list_of_ship_vision)} ")
        logging.info(f"Length of Halite Dict: {len(halite_amount_based_dict)} ")
        logging.info(f"Num Positions: {num_positions_in_dict}")
        logging.info(f"length of not in dict {len(not_in_dict)}")
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())
        logging.info("Ship has just been spawned")


    game.end_turn(command_queue)
