import random
import hlt
from hlt import constants
from hlt.positionals import Position, Direction
import logging

game = hlt.Game()
# game.update_frame()
me = game.me
game_map = game.game_map

maxNumberOfShips = 10
haliteNeededToSearch = max(game_map.averageHaliteAmount, game_map.medianHaliteAmount)
minimumDistanceBetweenDropPoints = 15
radiusOfDropPoint = 4
reserveHaliteForDropOff = False
justCreatedDropOffs = []
shipStatus = {}
navigatingShips = []
nextWealthyCellToAssign = 0
endGame = False


# Pregame
game_map.updateGoalCells(haliteNeededToSearch, me.shipyard)
logging.info(f"Total Halite-({game_map.totalHalite})-")
logging.info(f"Width-({game_map.width})-")


# Actual Game
game.ready("Experiment One Bot")
logging.info("Reach")

logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))


logging.info(f"Wealthy Map Cells Prioritized: {me.shipyard.goalCells}")
logging.info(f"Wealthy Map Cells: {game_map.wealthyCells}")

while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map
    command_queue = []

    logging.info(f"Average Halite Amount: {game_map.averageHaliteAmount}")
    logging.info(f"Median Halite Amount: {game_map.medianHaliteAmount}")
    logging.info(f"Halite Needed to Search: {haliteNeededToSearch}")
    if game.turn_number > 50 and game.turn_number % 10 == 0:
        logging.info(f"Finding wealthy cells with at least {haliteNeededToSearch * 2} halite.")
        foundCells = game_map.updateGoalCells(haliteNeededToSearch * 2, me.shipyard)
        if foundCells:
            # logging.info(f"Wealthy Map Cells Prioritized: {me.shipyard.goalCells}")
            nextWealthyCellToAssign = 0
    # logging.info(f"Wealthy Map Cells Prioritized: {me.shipyard.goalCells}")


    # if haliteNeededToSearch >= 50:
    #     haliteNeededToSearch -= 0.3
    #     logging.info(f"Average amount of halite in map: {game_map.averageHaliteAmount}")
    # elif haliteNeededToSearch >= 10:
    #     haliteNeededToSearch -= 0.1
    haliteNeededToSearch = min(game_map.averageHaliteAmount, game_map.medianHaliteAmount)

    if game.turn_number < constants.MAX_TURNS / 3 and \
        me.halite_amount >= constants.SHIP_COST and \
        not game_map[me.shipyard].booked and \
        not reserveHaliteForDropOff:
        game_map[me.shipyard.position].booked = True;
        command_queue.append(game.me.shipyard.spawn())

    game.end_turn(command_queue)
    logging.info("I CAN PRINT AFTER GAME ENDS.")


# Enclosed methods



