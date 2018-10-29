import hlt
from hlt import constants
from hlt.positionals import Position
import logging

game = hlt.Game()
game.ready("Inspired Detection Bot 1")

logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

maxNumberOfShips = 1
ships = {}

while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map

    command_queue = []

    for ship in me.get_ships():
        logging.info("For Loop has begun")
        logging.info(f"The Map Cell Ship Position: {game_map[ship.position]}")
        logging.info(f"the true position of the ship: {ship.position}")

        move = game_map.naive_navigate(ship, Position(7, 5))
        command_queue.append(ship.move(move))
        number_of_enemy_ships = 0
        for i in range(-constants.INSPIRATION_RADIUS, constants.INSPIRATION_RADIUS + 1): #x coordinate
            yCheck = constants.INSPIRATION_RADIUS - abs(i) #y values to check
            for j in range(-yCheck, yCheck + 1): #y coordinate (+1 because the stop parameter is not included)
                add_on = Position(i,j)
                if game_map[add_on + ship.position].is_occupied:
                    isEnemyShip = True
                    for aship in me.get_ships():
                        if aship.id == (game_map[add_on + ship.position]).ship.id:
                            isEnemyShip = False

                    if isEnemyShip:
                        number_of_enemy_ships += 1
                        logging.info(f"Detected ship: {(game_map[add_on + ship.position]).ship.id}")
                        if number_of_enemy_ships >= 2:
                            break


        logging.info(f"Ship ID: {ship.id}")
        logging.info(f"Enemy Ship Counter within the Inspired Radius: {number_of_enemy_ships}")
        if number_of_enemy_ships >= 2:
            logging.info(f"The Ship is inspired, {game.turn_number}")
        
    
    if len(me.get_ships()) < maxNumberOfShips and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(game.me.shipyard.spawn())

    
    game.end_turn(command_queue)