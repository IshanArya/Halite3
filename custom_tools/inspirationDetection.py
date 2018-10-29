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


logging.info(f"Enemy Ship Counter within the Inspired Radius: {number_of_enemy_ships}")
if number_of_enemy_ships >= 2:
    logging.info(f"The Ship is inspired, {game.turn_number}")