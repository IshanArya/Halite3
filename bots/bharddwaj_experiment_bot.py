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
    command_queue = []
    #list_of_information = []
    for i in range(int(-width/2),int(width/2)+1): #when i used -width and width + 1 here i didn't get an error for some reason
        for j in range(int(-height/2),int(height/2)+1):
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
    for ship in me.get_ships():
        ship_specific_list = [] #this info is specific to positions in a radius around the ship
        logging.info("Looping among friendly ships has begun")
        counter = 0 #see how many positions i get from the loop
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
                logging.info(f"{str(position_relative_to_ship_one)}")
                for i in position_based_dict:
                    temp_list = []
                    if str(position_relative_to_ship_one) == i[0]:
                        temp_list.append(position_relative_to_ship_one) #Position
                        temp_list.append(position_based_dict[i][0]) #append the halite amount
                        if len(halite_amount_for_all_cells[i]) > 1: #doing this to check to see if there is an enemy ship
                            the_list =position_based_dict[i]
                            temp_list.append(the_list[1])
                    temp_list2 = []
                    if str(position_relative_to_ship_two) ==i[0]:
                        temp_list2.append(position_relative_to_ship_two)
                        temp_list2.append(position_based_dict[i][0])
                        if len(halite_amount_for_all_cells[i]) > 1:
                            the_list =position_based_dict[i]
                            temp_list2.append(the_list[1])
                    temp_list3 = []
                    if str(position_relative_to_ship_three) ==i[0]:
                        temp_list3.append(position_relative_to_ship_three)
                        temp_list3.append(position_based_dict[i][0])
                        if len(halite_amount_for_all_cells[i]) > 1:
                            the_list =position_based_dict[i]
                            temp_list3.append(the_list[1])
                    temp_list4 = []
                    if str(position_relative_to_ship_four) == i[0]:
                        temp_list4.append(position_relative_to_ship_four)
                        temp_list4.append(position_based_dict[i][0])
                        if len(halite_amount_for_all_cells[i]) > 1:
                            the_list =position_based_dict[i]
                            temp_list4.append(the_list[1])
                    if not temp_list == []:
                        ship_specific_list.append(temp_list)
                    if not temp_list2 == []:
                        ship_specific_list.append(temp_list2)
                    if not temp_list3 == []:
                        ship_specific_list.append(temp_list3)
                    if not temp_list4 == []:
                        ship_specific_list.append(temp_list4)
        logging.info(f"Dictionary: {halite_amount_for_all_cells}")
        logging.info(f'Length of Dictionary: {len(halite_amount_for_all_cells)}')
        logging.info(f"Ship Specific List: {ship_specific_list}")
        logging.info(f"counter: {counter}")
        logging.info(f"Length of the list: {len(ship_specific_list)}")
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())
        logging.info("Ship has just been spawned")


    game.end_turn(command_queue)
