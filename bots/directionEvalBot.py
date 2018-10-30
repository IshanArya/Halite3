import hlt
from hlt import constants
from hlt.positionals import Position, Direction
import logging

game = hlt.Game()
me = game.me
game_map = game.game_map

maxNumberOfShips = 10
shipStatus = {}
wealthyMapCells = []
nextWealthyCellToAssign = 0


def findWealthyMapCells():  # populate wealthy cells list
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

def isShipInspired(ship): # check if ship is inspired
    numberOfEnemyShips = 0
    for i in range(-constants.INSPIRATION_RADIUS, constants.INSPIRATION_RADIUS + 1):  # x coordinate
        yCheck = constants.INSPIRATION_RADIUS - abs(i)  # y values to check
        # y coordinate (+1 because the stop parameter is not included)
        for j in range(-yCheck, yCheck + 1):
            add_on = Position(i, j)
            if game_map[add_on + ship.position].is_occupied:
                isEnemyShip = True
                for aship in me.get_ships():
                    if aship.id == (game_map[add_on + ship.position]).ship.id:
                        isEnemyShip = False

                if isEnemyShip:
                    numberOfEnemyShips += 1
                    if numberOfEnemyShips >= 2:
                        break
    logging.info(f"Enemy Ship Counter within the Inspired Radius: {numberOfEnemyShips}")
    if numberOfEnemyShips >= 2:
        logging.info(f"The Ship is inspired, {game.turn_number}")
        return True
    return False

def findMostWealthyAdjacentCell(ship):
    maxHalite = 0
    bestCell = None

    for cardinal in ship.position.get_surrounding_cardinals():
        if not game_map[cardinal].is_occupied:
            if game_map[cardinal].halite_amount > maxHalite:
                maxHalite = game_map[cardinal].halite_amount
                bestCell = cardinal
    

    return (bestCell - ship.position) if bestCell else bestCell # subtract ship.position to just get movement

def evaluateBestMoveForShip(ship):
    if ship.id not in shipStatus:
        global nextWealthyCellToAssign
        shipStatus[ship.id] = {}
        shipStatus[ship.id]["movement"] = "exploring"
        logging.info(f"shipStatus Object: {shipStatus}")
        shipStatus[ship.id]["wealthCellObjective"] = wealthyMapCells[(nextWealthyCellToAssign) % len(wealthyMapCells)]
        nextWealthyCellToAssign += 1
    
    if ship.halite_amount >= constants.MAX_HALITE:
        shipStatus[ship.id]["movement"] = "returning"

    if shipStatus[ship.id]["movement"] == "returning":
        if ship.position == me.shipyard.position:
            shipStatus[ship.id]["movement"] = "exploring"
        else:
            shipStatus[ship.id]["intention"] = "move"
            return ship.move(game_map.naive_navigate(ship, me.shipyard.position))
    
    # All commands if ship is exploring
    haliteNeededToSearch = constants.MAX_HALITE / 10
    if game_map[ship.position].halite_amount >= haliteNeededToSearch:
        shipStatus[ship.id]["intention"] = "stay"
        return ship.stay_still()

    shipStatus[ship.id]["intention"] = "move"
    bestCell = findMostWealthyAdjacentCell(ship)
    if bestCell and game_map[bestCell + ship.position].halite_amount >= haliteNeededToSearch:
        game_map[bestCell + ship.position].mark_unsafe(ship)
        return ship.move(Direction.convert((bestCell.x, bestCell.y)))

    return ship.move(game_map.naive_navigate(ship, shipStatus[ship.id]["wealthCellObjective"]))


    
    
# Pregame
findWealthyMapCells()


# Actual Game
game.ready("Direction Eval Bot")
logging.info("Reach")

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
        command_queue.append(evaluateBestMoveForShip(ship))

    if len(me.get_ships()) < maxNumberOfShips and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(game.me.shipyard.spawn())

    game.end_turn(command_queue)


# Enclosed methods



