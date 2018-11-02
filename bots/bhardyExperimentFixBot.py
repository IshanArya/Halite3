import numpy as np
import hlt
from hlt.positionals import Position,Direction
from hlt import constants
import logging
import random
import os
from collections import OrderedDict
game = hlt.Game()
game.ready("Bhardy Bot")
logging.info("bharddwaj-experiment-bot")
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
    halite_amount_at_cells_below_average = [] #tuple (position, halite amount)
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
        logging.info("is this loop happening")
        ship_is_full_counter = 0
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        distances_to_above_average = [] #contain tuples with distance and halite amount
        distances_to_below_average = []

        distances_and_positions_above_average = [] #contains tuples with distance and position
        distances_and_positions_below_average = []

        enemy_distances_to_above_average = [] #list of tuples (list of eneemy ship distances from that cell, halite amount)
        enemy_distances_to_below_average = []

        above_average_final_normalized_score = [] #list of distances multiplied by the normalized score
        below_average_final_normalized_score = []

        enemy_above_average_final_normalized_score = []
        enemy_below_average_final_normalized_score = []

        for i in range(0,len(halite_amount_at_cells_above_average)):
                distance = game_map.calculate_distance(ship.position,halite_amount_at_cells_above_average[i][0])
                distances_to_above_average.append((distance,halite_amount_at_cells_above_average[i][1]))
                distances_and_positions_above_average.append((distance,halite_amount_at_cells_above_average[i][0]))
                above_average_final_normalized_score.append(distance*halite_amount_normalized_above_average[i][1])
                #multiplying the distance with the normalized score

        for i in range(0,len(halite_amount_at_cells_below_average)):
                distance = game_map.calculate_distance(ship.position,halite_amount_at_cells_below_average[i][0])
                distances_to_below_average.append((distance,halite_amount_at_cells_below_average[i][1]))
                distances_and_positions_below_average.append((distance,halite_amount_at_cells_below_average[i][0]))
                below_average_final_normalized_score.append(distance*halite_amount_normalized_below_average[i][1])
        #logging.info(f"Distances to above average: {distances_to_above_average}")
        #logging.info(f"Distances to below average: {distances_to_below_average}")
        if ship.halite_amount > 900:
            ship_is_full_counter = 1
        if ship_is_full_counter > 0 and not ship.position == me.shipyard.position:
            naive_direction = game_map.intelligent_navigate(ship, me.shipyard.position,True)
            command_queue.append(ship.move(naive_direction))
            #this command alone apparently doesn't allow the ship to go into the shipyard
            logging.info(f"Ship is full and command_queue has appended the {naive_direction}")
            ship_is_full_counter = 0
        else:
            logging.info("entered the else statement")
            below_average_cell_positions = []
            for i in range(0,len(halite_amount_at_cells_below_average)):
                below_average_cell_positions.append(halite_amount_at_cells_below_average[i][0])
            if ship.position in below_average_cell_positions or ship.position == me.shipyard.position:
                if (1/(constants.MOVE_COST_RATIO))*game_map[ship.position].halite_amount <= ship.halite_amount or ship.position == me.shipyard.position: #did this as an exception if the ship is in the shipyard
                    minimum_value = distances_and_positions_above_average[0][0]
                    position_to_travel = distances_and_positions_above_average[0][1]
                    for i in range(0, len(distances_and_positions_above_average)):
                        if minimum_value > distances_and_positions_above_average[i][0]:
                            minimum_value = distances_and_positions_above_average[i][0]
                            position_to_travel =  distances_and_positions_above_average[i][1]
                    naive_direction = game_map.intelligent_navigate(ship,position_to_travel,True)
                    logging.info(f"Ship is moving in the intelligent direction with {position_to_travel}")
                    logging.info(
                        f"Direction: {naive_direction}")
                    command_queue.append(ship.move(naive_direction))
                else: #if not enough halite to move
                    logging.info("Ship is staying still because it cannot move")
                    command_queue.append(ship.stay_still())
            else:
                logging.info("Ship is in an above average halite cell so it is collecting halite")
                command_queue.append(ship.stay_still())


    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())
        logging.info("Ship has just been spawned")

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
