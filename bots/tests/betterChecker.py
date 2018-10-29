number_of_enemy_ships = 0;
for i in range(1,5):
    logging.info(f"The Map Cell Ship Position: {game_map[ship.position]}")
    logging.info(f"the true position of the ship: {ship.position}")
    zero = Position(0,i)
    one = Position(0,-i)
    two = Position(i,0)
    three = Position(-i,0)
    #logging.info(f"The Ship Position added to a tuple: {game_map[zero.__add__(ship.position)]}")
    #logging.info(f"The Ship Position added to a tuple: {game_map[one.__add__(ship.position)]}")
    #logging.info(f"The Ship Position added to a tuple: {game_map[two.__add__(ship.position)]}")
    #logging.info(f"The Ship Position added to a tuple: {game_map[three.__add__(ship.position)]}")
    #logging.info(f"the game map.ship thing: {game_map[zero.__add__(ship.position)].ship}")
    
    # if number_of_enemy_ships >= 2:
    #     break

    if game_map[zero.__add__(ship.position)].is_occupied:
        isEnemyShip = True
        for aship in me.get_ships():
            if aship == (game_map[zero.__add__(ship.position)]).ship:
                isEnemyShip = False
        if isEnemyShip:
            number_of_enemy_ships += 1

    elif (game_map[one.__add__(ship.position)]).is_occupied:
        isEnemyShip = True
        for aship in me.get_ships():
            if aship == (game_map[one.__add__(ship.position)]).ship:
                isEnemyShip = False
        if isEnemyShip:
            number_of_enemy_ships += 1

    elif (game_map[two.__add__(ship.position)]).is_occupied:
        isEnemyShip = True
        for aship in me.get_ships():
            if aship == (game_map[two.__add__(ship.position)]).ship:
                isEnemyShip = False
        if isEnemyShip:
            number_of_enemy_ships += 1

    elif (game_map[three.__add__(ship.position)]).is_occupied:
        isEnemyShip = True
        for aship in me.get_ships():
            if aship == (game_map[three.__add__(ship.position)]).ship:
                isEnemyShip = False
        if isEnemyShip:
            number_of_enemy_ships += 1

logging.info(f"Enemy Ship Counter within the Inspired Radius: {number_of_enemy_ships}")