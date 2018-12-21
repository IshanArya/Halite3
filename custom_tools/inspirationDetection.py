numberOfEnemyShips = 0
for i in range(-constants.INSPIRATION_RADIUS, constants.INSPIRATION_RADIUS + 1): #x coordinate
    yCheck = constants.INSPIRATION_RADIUS - abs(i) #y values to check
    for j in range(-yCheck, yCheck + 1): #y coordinate (+1 because the stop parameter is not included)
        add_on = Position(i,j)
        if game_map[add_on + ship.position].is_occupied:
            isEnemyShip = True
            if game_map[add_on + ship.position].ship.owner == ship.owner:
                isEnemyShip = False

            if isEnemyShip:
                numberOfEnemyShips += 1
                logging.info(f"Detected ship: {(game_map[add_on + ship.position]).ship.id}")
                if numberOfEnemyShips >= 2:
                    break


logging.info(f"Enemy Ship Counter within the Inspired Radius: {numberOfEnemyShips}")
if numberOfEnemyShips >= 2:
    logging.info(f"The Ship is inspired, {game.turn_number}")
