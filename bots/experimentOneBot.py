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
haliteNeededToSearch = 100
shipStatus = {}
navigatingShips = []
wealthyMapCells = []
nextWealthyCellToAssign = 0
endGame = False



def getClosestShipyardAdjacentCell(ship):
    shortestDistance = 1000
    closestCell = None
    for direction in Direction.get_all_cardinals():
        target_pos = me.shipyard.position.directional_offset(direction)
        currentDistance = game_map.calculate_distance(ship.position, target_pos)
        if currentDistance < shortestDistance:
            closestCell = target_pos
            shortestDistance = currentDistance
    
    return closestCell

def evaluateBestMoveForShip(ship):
    global nextWealthyCellToAssign, endGame
    if ship.id not in shipStatus:
        shipStatus[ship.id] = {}
        shipStatus[ship.id]["movement"] = "exploring"
        logging.info(f"shipStatus Object: {shipStatus}")
        shipStatus[ship.id]["wealthCellObjective"] = wealthyMapCells[(nextWealthyCellToAssign) % len(wealthyMapCells)]
        nextWealthyCellToAssign += 1
    tempGoal = shipStatus[ship.id]["wealthCellObjective"]
    logging.info(f"Ship {ship.id} is navigating towards: {tempGoal}")
    
    # BIG EDGE CASE: Check if ship has enough halite to move!!
    if ship.halite_amount < (1/constants.MOVE_COST_RATIO) * game_map[ship.position].halite_amount:
        logging.info(f"Ship {ship.id} does not have enough halite to move.")
        game_map[ship.position].booked = True
        return ship.stay_still()


    distanceFromShipyard = game_map.calculate_distance(ship.position, me.shipyard.position)
    turnsLeft = constants.MAX_TURNS - game.turn_number
    logging.info(f"Distance from shipyard: {distanceFromShipyard}")
    logging.info(f"Turns left: {turnsLeft}")
    if endGame or shipStatus[ship.id]["movement"] == "ending" or distanceFromShipyard + 2 > turnsLeft:
        endGame = True
        logging.info(f"End game for {ship.id}")
        shipStatus[ship.id]["movement"] = "ending"
        if ship.position != me.shipyard.position:
            shipStatus[ship.id]["wealthCellObjective"] = getClosestShipyardAdjacentCell(ship)
            if ship.position == shipStatus[ship.id]["wealthCellObjective"]:
                return ship.move(game_map.get_unsafe_moves(ship.position, me.shipyard.position)[0])
            navigatingShips.append(ship)
        return None
            
     
    if ship.halite_amount >= constants.MAX_HALITE:
        shipStatus[ship.id]["movement"] = "returning"

    if shipStatus[ship.id]["movement"] == "returning":
        if ship.position == me.shipyard.position:
            shipStatus[ship.id]["movement"] = "exploring"
        else:
            logging.info(f"Ship {ship.id} will be returning.")
            navigatingShips.append(ship)
            return None
    
    # All commands if ship is exploring
    if game_map[ship.position].halite_amount >= haliteNeededToSearch:
        game_map[ship.position].booked = True
        logging.info(f"Ship {ship.id} will be staying.")
        return ship.stay_still()

    bestCell = game_map.getMostWealthyAdjacentCell(ship)
    if bestCell and game_map[bestCell + ship.position].halite_amount >= haliteNeededToSearch:
        game_map[bestCell + ship.position].booked = True
        logging.info(f"Ship {ship.id} will be moving to adjacent square: {bestCell + ship.position}")
        return ship.move(Direction.convert((bestCell.x, bestCell.y)))

    if game_map[shipStatus[ship.id]["wealthCellObjective"]].halite_amount < game_map.averageHaliteAmount:
        shipStatus[ship.id]["wealthCellObjective"] = wealthyMapCells[(nextWealthyCellToAssign) % len(wealthyMapCells)]
        nextWealthyCellToAssign += 1
    navigatingShips.append(ship)
    return None


    
    
# Pregame
wealthyMapCells = game_map.getWealthyCells(200, me.shipyard.position)

logging.info(f"Total Halite-({game_map.totalHalite})-")
logging.info(f"Width-({game_map.width})-")


# Actual Game
game.ready("Experiment One Bot")
logging.info("Reach")

logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))


while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map
    logging.info(f"Average Halite Amount: {game_map.averageHaliteAmount}")
    if game.turn_number > 50 and game.turn_number % 10 == 0:
        logging.info(f"Finding wealthy cells with at least {haliteNeededToSearch * 2} halite.")
        tempWealthyMapCells = game_map.getWealthyCells(
            haliteNeededToSearch * 2, me.shipyard.position)
        if tempWealthyMapCells:
            wealthyMapCells = tempWealthyMapCells
            logging.info(f"Wealthy Map Cells Prioritized: {wealthyMapCells}")
            nextWealthyCellToAssign = 0
    else:
        logging.info(f"Wealthy Map Cells Prioritized: {wealthyMapCells}")

    command_queue = []

    if haliteNeededToSearch >= 50:
        haliteNeededToSearch -= 0.3
        logging.info(f"Average amount of halite in map: {game_map.averageHaliteAmount}")
    elif haliteNeededToSearch >= 10:
        haliteNeededToSearch -= 0.1
    # haliteNeededToSearch = game_map.averageHaliteAmount / 4

    for ship in me.get_ships():
        logging.info("For Loop has begun")
        logging.info(f"The Map Cell Ship Position: {game_map[ship.position]}")
        logging.info(f"the true position of the ship: {ship.position}")
        bestMoveForShip = evaluateBestMoveForShip(ship)
        if bestMoveForShip:
            logging.info(f"Best move for ship {ship.id} is {bestMoveForShip}")
            command_queue.append(bestMoveForShip)
    
    logging.info(f"Navigating ships: {navigatingShips}")
    for ship in navigatingShips:
        logging.info(f"Still trying to find {ship.id} a move.")
        direction = game_map.intelligent_navigate(
            ship, 
            shipStatus[ship.id]["wealthCellObjective"] if shipStatus[ship.id]["movement"] == "exploring" else me.shipyard.position)
        logging.info(f"Ship {ship.id} is going to be moving in direction: {direction}")
        command_queue.append(ship.move(direction))
    
    navigatingShips = []

    if game.turn_number < constants.MAX_TURNS / 3 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].booked:
        game_map[me.shipyard.position].booked = True;
        command_queue.append(game.me.shipyard.spawn())

    game.end_turn(command_queue)


# Enclosed methods



