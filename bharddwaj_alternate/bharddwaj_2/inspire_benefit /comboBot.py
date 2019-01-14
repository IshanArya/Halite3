import random
import hlt
from hlt import constants
from hlt.positionals import Position, Direction
import logging

game = hlt.Game()
# game.update_frame()
me = game.me
game_map = game.game_map

haliteReserve = constants.SHIP_COST
haliteNeededToSearch = max(game_map.averageHaliteAmount, game_map.medianHaliteAmount)
minimumDistanceBetweenDropPoints = 17
radiusOfDropPoint = 4
shipInfo = {}
navigatingShips = []
percentHaliteToSpawn = .4
endGame = False



def getClosestDropPointAdjacentCell(ship):
    closestDropPointPosition = findClosestDropPointPosition(ship.position)
    shortestDistance = 1000
    closestCell = None
    for direction in Direction.get_all_cardinals():
        target_pos = closestDropPointPosition.directional_offset(direction)
        currentDistance = game_map.calculate_distance(ship.position, target_pos)
        if currentDistance < shortestDistance:
            closestCell = target_pos
            shortestDistance = currentDistance

    return closestCell

def evaluateBestMoveForShip(ship):
    global endGame
    if ship.id not in shipInfo:
        shipInfo[ship.id] = {}
        logging.info(f"Initializing ship: {ship.id}")
        shipInfo[ship.id]["status"] = "exploring"
        assignGoal(ship)

    # BIG EDGE CASE: Check if ship has enough halite to move!!
    if ship.halite_amount < (1/constants.MOVE_COST_RATIO) * game_map[ship.position].halite_amount:
        logging.info(f"Ship {ship.id} does not have enough halite to move.")
        game_map[ship.position].booked = True
        return ship.stay_still()

    closestDropPointPosition = findClosestDropPointPosition(ship.position)
    distanceFromClosestDropPoint = game_map.calculate_distance(ship.position, closestDropPointPosition)
    turnsLeft = constants.MAX_TURNS - game.turn_number
    logging.info(f"Distance from closest drop point: {distanceFromClosestDropPoint}")
    logging.info(f"Turns left: {turnsLeft}")
    if endGame or shipInfo[ship.id]["status"] == "ending" or distanceFromClosestDropPoint + 2 > turnsLeft:
        endGame = True
        logging.info(f"End game for {ship.id}")
        shipInfo[ship.id]["status"] = "ending"
        if ship.position != closestDropPointPosition:
            shipInfo[ship.id]["goal"] = closestDropPointPosition
            if ship.position == shipInfo[ship.id]["goal"]:
                return ship.move(game_map.get_unsafe_moves(ship.position, closestDropPointPosition)[0])
            navigatingShips.append(ship)
        return None

    if shipInfo[ship.id]["status"] == "spawningDropoff":
        if validDropoffCreationPoint(ship):
            game_map[ship.position].booked = True
            haliteWallet = ship.halite_amount + game_map[ship.position].halite_amount + me.halite_amount
            if haliteWallet >= constants.DROPOFF_COST:
                logging.info(f"Turning ship {ship.id} into dropoff.")
                return createDropOffPoint(ship)
            else:
                return ship.stay_still()
        else:
            shipInfo[ship.id]["status"] = "exploring"
            del shipInfo[ship.id]["dropOffPoint"]

    if ship.halite_amount >= constants.MAX_HALITE:
        shipInfo[ship.id]["status"] = "returning"

    if shipInfo[ship.id]["status"] == "returning":
        if ship.position == findClosestDropPointPosition(ship.position):
            shipInfo[ship.id]["status"] = "exploring"
        else:
            logging.info(f"Ship {ship.id} will be returning.")
            navigatingShips.append(ship)
            return None

    # All commands if ship is exploring
    if game_map[ship.position].halite_amount >= haliteNeededToSearch:
        game_map[ship.position].booked = True
        if validDropoffCreationPoint(ship):
            haliteWallet = ship.halite_amount + game_map[ship.position].halite_amount + me.halite_amount
            if haliteWallet >= constants.DROPOFF_COST:
                logging.info(f"Turning ship {ship.id} into dropoff.")
                return createDropOffPoint(ship)
            else:
                shipInfo[ship.id]["status"] = "spawningDropoff"
                shipInfo[ship.id]["dropOffPoint"] = ship.position
        else:
            logging.info(f"Ship {ship.id} NOT @ valid drop off creation point.")
        logging.info(f"Ship {ship.id} will be staying.")
        return ship.stay_still()

    bestCell = game_map.getMostWealthyAdjacentCell(ship)
    futureDropOffs = getDropOffsToBe()
    if bestCell:
        adjacentCell = bestCell + ship.position
        if adjacentCell not in futureDropOffs and game_map[adjacentCell].halite_amount >= haliteNeededToSearch:
            game_map[adjacentCell].booked = True
            logging.info(f"Ship {ship.id} will be moving to adjacent square: {adjacentCell}")
            return ship.move(Direction.convert((bestCell.x, bestCell.y)))

    shipGoal = shipInfo[ship.id]["goal"]
    if game_map[shipGoal].halite_amount < haliteNeededToSearch:
        assignGoal(ship)
    navigatingShips.append(ship)
    return None

def assignGoal(ship):
    closestDropPoint = findClosestDropPointPosition(ship.position)
    allReservedGoals = set(filter(lambda currentShip: currentShip.id in shipInfo, me.get_ships()))
    allReservedGoals.remove(ship)
    allReservedGoals = set(map(lambda currentShip: shipInfo[currentShip.id]["goal"], allReservedGoals))

    shipGoal = game_map.getGoalCell(closestDropPoint, allReservedGoals)
    shipInfo[ship.id]["goal"] = shipGoal
    logging.info(f"New goal of ship {ship.id}: {shipGoal}")

def findClosestDropPointPosition(position):
    dropPoints = set(map(lambda dropoff: dropoff.position, me.get_dropoffs()))
    dropPoints.update(getDropOffsToBe())
    closestDropPoint = me.shipyard.position
    distance = game_map.calculate_distance(closestDropPoint, position)
    for dropPoint in dropPoints:
        distanceToDropPoint = game_map.calculate_distance(dropPoint, position)
        if(distanceToDropPoint < distance):
            closestDropPoint = dropPoint
            distance = distanceToDropPoint

    return closestDropPoint

def validDropoffCreationPoint(ship):
    if game.turn_number > constants.MAX_TURNS / 1.5:
        return False
    closestDropPointPosition = findClosestDropPointPosition(ship.position)
    if(game_map.calculate_distance(closestDropPointPosition, ship.position) < minimumDistanceBetweenDropPoints):
        return False

    totalHaliteAround = game_map.getTotalHaliteAroundAPoint(ship.position, radiusOfDropPoint)
    dropOffHaliteThreshhold = haliteNeededToSearch * 90
    logging.info(f"DropOff Threshold Halite: {dropOffHaliteThreshhold}")
    logging.info(f"Total Halite Around: {totalHaliteAround}")
    if totalHaliteAround < dropOffHaliteThreshhold:
        return False

    return True

def createDropOffPoint(ship):
    global reserveHaliteForDropOff
    reserveHaliteForDropOff = False
    me.halite_amount -= constants.DROPOFF_COST
    return ship.make_dropoff()

def getDropOffsToBe():
    dropOffsToBe = []
    for shipId in shipInfo:
        if "dropOffPoint" in shipInfo[shipId]:
            dropOffsToBe.append(shipInfo[shipId]["dropOffPoint"])

    return dropOffsToBe

def purgeShipInfo(ships):
    ships = set(map(lambda ship: ship.id, ships))
    for shipId in list(shipInfo.keys()):
        if shipId not in ships:
            del shipInfo[shipId]

# Pregame
game_map.updateGoalCells(haliteNeededToSearch, me.shipyard)
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

    # if haliteNeededToSearch >= 50:
    #     haliteNeededToSearch -= 0.3
    #     logging.info(f"Average amount of halite in map: {game_map.averageHaliteAmount}")
    # elif haliteNeededToSearch >= 10:
    #     haliteNeededToSearch -= 0.1
    haliteNeededToSearch = min(game_map.averageHaliteAmount, game_map.medianHaliteAmount)

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
        destination = shipInfo[ship.id]["goal"]
        if shipInfo[ship.id]["status"] == "returning":
            destination = findClosestDropPointPosition(ship.position)
        direction = game_map.intelligent_navigate(
            ship,
            destination)
        logging.info(f"Ship {ship.id} is going to be moving in direction: {direction}")
        command_queue.append(ship.move(direction))


    logging.info(f"Halite Reserve: {haliteReserve}")
    percentHaliteLeft = game_map.getPercentHaliteLeft()
    numberOfFutureDropOffs = len(getDropOffsToBe())
    if numberOfFutureDropOffs > 0:
        haliteReserve = constants.SHIP_COST + (constants.DROPOFF_COST * numberOfFutureDropOffs)
    else:
        haliteReserve = constants.SHIP_COST
    if percentHaliteLeft > percentHaliteToSpawn and game.turn_number < constants.MAX_TURNS / 1.5:
        if not game_map[me.shipyard].booked:
            if me.halite_amount >= haliteReserve:
                game_map[me.shipyard.position].booked = True;
                command_queue.append(game.me.shipyard.spawn())

    game.end_turn(command_queue)

    navigatingShips = []
    logging.info(f"Navigating Ships at the End: {navigatingShips}")
    purgeShipInfo(me.get_ships())



# Enclosed methods