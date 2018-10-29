import hlt
from hlt import constants
from hlt.positionals import Position
import logging

game = hlt.Game()
game.ready("Inspired Detection Bot 2")

logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

maxNumberOfShips = 2

while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map

    command_queue = []

    if len(me.get_ships()) < maxNumberOfShips:
        for ship in me.get_ships():
            logging.info(f"Less than {maxNumberOfShips} ships.")
            logging.info(f"The Map Cell Ship Position: {game_map[ship.position]}")
            logging.info(f"the true position of the ship: {ship.position}")

            move = game_map.naive_navigate(ship, Position(7, 6))
            command_queue.append(ship.move(move))
    else:
        logging.info(f"Have {len(me.get_ships())}  ships")
        ships = me.get_ships()
        ship0Move = game_map.naive_navigate(ships[0], Position(9, 8))
        command_queue.append(ships[0].move(ship0Move))
        ship1Move = game_map.naive_navigate(ships[1], Position(7, 6))
        command_queue.append(ships[1].move(ship1Move))
        
    
    if len(me.get_ships()) < maxNumberOfShips and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(game.me.shipyard.spawn())


    game.end_turn(command_queue)