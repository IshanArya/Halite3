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

'''ship_plans = {} #keep track of plans for the ship
if os.path.exists("c{}_input.vec".format(VERSION)):
    os.remove("c{}_input.vec".format(VERSION))

if os.path.exists("c{}_out.vec".format(VERSION)):
    os.remove("c{}_out.vec".format(VERSION))'''
#logging.info(f"Width: {game_map.width}")
#logging.info(f"Height: {game_map.height}")
width = game.game_map.width
height = game.game_map.height
#some sentdex tutorial code
def key_by_value(dictionary, value):
    for k,v in dictionary.items():
        if v[0] == value:
            return k
    return -99
#usually dictionaries are accessed by their keys so this allows us to access them via their values

def fix_data(data):
    new_list = []
    last_known_idx = 0
    for i in range(HM_ENT_FEATURES):
        try:
            if i < len(data):
                last_known_idx=i
            new_list.append(data[last_known_idx])
        except:
            new_list.append(0)

    return new_list
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
    enemy_ship_positions = []
    enemy_shipyard_map_cells = []
    enemy_shipyard_positions = []
    #not sure which kind i need tbh
    number_of_enemy_ships = 0
    halite_amount_for_all_cells = []
    for i in range(int(-width/2),int(width/2)+1): #when i used -width and width + 1 here i didn't get an error for some reason
        for j in range(int(-height/2),int(height/2)+1):
            some_position = Position(i,j)
            halite_amount_for_all_cells.append(game_map[some_position].halite_amount)
            if game_map[some_position].is_occupied:
                enemy_ship_id = game_map[some_position].ship.id
                for aship in me.get_ships():
                    if aship.id != enemy_ship_id:
                        enemy_ship_ids.append(enemy_ship_id)
                        enemy_ship_positions.append(some_position)
                        number_of_enemy_ships += 1
            elif game_map[some_position].has_structure and game_map[some_position] != game_map[me.shipyard.position]:
                enemy_shipyard_map_cells.append(game_map[some_position])
                enemy_shipyard_positions.append(some_position)
    number_of_friendly_ships = len(team_ships)
    avg_halite_amount = int(sum(halite_amount_for_all_cells)/len(halite_amount_for_all_cells))
    std_halite_amount = int(np.std(halite_amount_for_all_cells))
    halite_amount_at_cells_below_average = []
    halite_amount_at_cells_above_average = [] #also if the amount is the average it will go in this list
    halite_amount_normalized_above_average = [] #normalizing to try to weight distances more heavily
    halite_amount_normalized_below_average = []
    for i in range(int(-width/2),int(width/2)+1): #when i used -width and width + 1 here i didn't get an error for some reason
        for j in range(int(-height/2),int(height/2)+1):
            some_position = Position(i,j)

            if game_map[some_position].halite_amount >= avg_halite_amount:
                halite_amount_at_cells_above_average.append((some_position,game_map[some_position].halite_amount))
                norm_value = int((game_map[some_position].halite_amount - avg_halite_amount)/std_halite_amount)
                halite_amount_normalized_above_average.append((some_position, norm_value))
            else:
                norm_value = int((game_map[some_position].halite_amount - avg_halite_amount)/abs(std_halite_amount))
                halite_amount_at_cells_below_average.append((some_position,game_map[some_position].halite_amount))
                halite_amount_normalized_below_average.append((some_position, norm_value))

    #starter python code lmao
    for ship in me.get_ships():
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        distances_to_above_average = [] #contain tuples with distance and halite amount
        distances_to_below_average = []

        enemy_distances_to_above_average = [] #list of tuples (list of eneemy ship distances from that cell, halite amount)
        enemy_distances_to_below_average = []

        above_average_final_normalized_score = [] #list of distances multiplied by the normalized score
        below_average_final_normalized_score = []

        enemy_above_average_final_normalized_score = []
        enemy_below_average_final_normalized_score = []

        for i in range(0,len(halite_amount_at_cells_above_average)):
                distance = game_map.calculate_distance(ship.position,halite_amount_at_cells_above_average[i][0])
                distances_to_above_average.append((distance,halite_amount_at_cells_above_average[i][1]))
                above_average_final_normalized_score.append(distance*halite_amount_normalized_above_average[i][1])
                #multiplying the distance with the normalized score

        for i in range(0,len(halite_amount_at_cells_below_average)):
                distance = game_map.calculate_distance(ship.position,halite_amount_at_cells_below_average[i][0])
                distances_to_below_average.append((distance,halite_amount_at_cells_below_average[i][1]))
                below_average_final_normalized_score.append(distance*halite_amount_normalized_below_average[i][1])
        #logging.info(f"Distances to above average: {distances_to_above_average}")
        #logging.info(f"Distances to below average: {distances_to_below_average}")
        below_average_cell_positions = []
        for i in range(0,len(halite_amount_at_cells_below_average)):
            below_average_cell_positions.append(halite_amount_at_cells_below_average[i][0])
        if ship.halite_amount < 900:
            if (ship.position in below_average_cell_positions or ship.position == me.shipyard.position):
                minimum_value = min(above_average_final_normalized_score)
                for i in range(0,len(above_average_final_normalized_score)):
                    if ship.halite_amount > 10*distances_to_above_average[i][0]: #this is just a ballpark i need to do that 10% calculation thing
                        if above_average_final_normalized_score[i] == minimum_value:
                            naive_direction = game_map.naive_navigate(ship,halite_amount_at_cells_above_average[i][0])
                            ship.move(naive_direction)
                            break
                    else:
                        ship.stay_still()
            else:
                ship.stay_still()
        else:
            naive_direction = game_map.naive_navigate(ship,me.shipyard.position)
            ship.move(naive_direction)
        ''' # I attempted to move the ship to location where the score i derived was less than the enemy normalized score
        list_of_lists_of_enemy = []
        for i in range(0,len(halite_amount_at_cells_above_average)):
            list_of_lists_of_enemy = []
            for j in enemy_ship_positions:
                list_of_lists_of_enemy.append(game_map.calculate_distance(j,halite_amount_at_cells_above_average[i][0]))

            enemy_distances_to_above_average.append((list_of_lists_of_enemy,halite_amount_at_cells_above_average[i][0]))
            #logging.info(f"enemy distance tester: {enemy_distances_to_above_average}")
        for i in range(0,len(halite_amount_at_cells_below_average)):
            list_of_lists_of_enemy = []
            for j in enemy_ship_positions:
                list_of_lists_of_enemy.append(game_map.calculate_distance(j,halite_amount_at_cells_below_average[i][0]))

            enemy_distances_to_below_average.append((list_of_lists_of_enemy,halite_amount_at_cells_below_average[i][0]))
            #logging.info(f"enemy distance tester: {enemy_distances_to_below_average}")
        min_enemy_above_average_final_normalized_score = [] #since there are multiple enemy ships being compared to just one of our ships,we care about the smallest normal score
        min_enemy_below_average_final_normalized_score = []
        for i in range(0,len(enemy_distances_to_above_average)):
            enemy_above_average_final_normalized_score = []
            for j in enemy_distances_to_above_average[i][0]:
                enemy_above_average_final_normalized_score.append(j*halite_amount_normalized_above_average[i][1]) #each distance multiplied by the halite amount
            min_enemy_above_average_final_normalized_score.append(min(enemy_above_average_final_normalized_score))

        #logging.info(f"enemy distance above average: {enemy_distances_to_above_average[0][0]}")
        for i in range(0,len(enemy_distances_to_below_average)):
            enemy_below_average_final_normalized_score = []
            for j in enemy_distances_to_below_average[i][0]:
                enemy_below_average_final_normalized_score.append(j*halite_amount_normalized_below_average[i][1]) #each distance multiplied by the halite amount
            min_enemy_below_average_final_normalized_score.append(min(enemy_below_average_final_normalized_score))
        below_average_cell_positions = []
        for i in range(0,len(halite_amount_at_cells_below_average)):
            below_average_cell_positions.append(halite_amount_at_cells_below_average[i][0])
        for i in range(0,len(min_enemy_above_average_final_normalized_score)): #this length should also be equal to length of ships normalized scores to above average
            if ship.position in below_average_cell_positions or ship.position == me.shipyard.position:
                if min_enemy_above_average_final_normalized_score[i] > above_average_final_normalized_score[i]:
                    naive_direction = game_map.naive_navigate(ship,halite_amount_at_cells_above_average[i][0]) #need to use this list in order to get the position of the cell
                    ship.move(naive_direction)
                    break
            else:
                ship.stay_still()
                break'''


        ''' this is the default command to move the ship
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            command_queue.append(
                ship.move(
                    random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ])))
        else:
            command_queue.append(ship.stay_still())'''

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
