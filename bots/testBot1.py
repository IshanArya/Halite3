import hlt
from hlt import constants
from hlt.positionals import Position
import logging

game = hlt.Game()
me = game.me
game_map = game.game_map

maxNumberOfShips = 1
wealthyMapCells = []

# Pregame
shipyardPosition = me.shipyard.position
logging.info(f"GameMap width: {game_map.width}")
scanStartIndex = 0
scanEndIndex = game_map.width
if shipyardPosition.x < (game_map.width / 2):
    scanEndIndex /= 2
else:
    scanStartIndex = game_map.width / 2
logging.info(f"Start Index: {scanStartIndex}; End Index: {scanEndIndex}")
for i in range(int(scanStartIndex), int(scanEndIndex)):
    for j in range(game_map.height):
        currentPosition = Position(i, j)
        if game_map[currentPosition].halite_amount > constants.MAX_HALITE / 2 and not game_map[currentPosition].has_structure:
            wealthyMapCells.append(currentPosition)
logging.info(f"All wealthy cells: {wealthyMapCells}")


# Actual Game
game.ready("Inspired Detection Bot 1")

logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))



while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map

    command_queue = []

    for ship in me.get_ships():
        logging.info("For Loop has begun")
        logging.info(f"The Map Cell Ship Position: {game_map[ship.position]}")
        logging.info(f"the true position of the ship: {ship.position}")


        
    
    if len(me.get_ships()) < maxNumberOfShips and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(game.me.shipyard.spawn())

    
    game.end_turn(command_queue)