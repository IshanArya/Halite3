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
    if game_map[zero.__add__(ship.position)].is_occupied:
        friend_ship_counter_zero = 0
        for aship in me.get_ships():
            if not game_map[aship.position] == (game_map[zero.__add__(ship.position)]):
                friend_ship_counter_zero += 1
            if friend_ship_counter_zero == len(me.get_ships()): #if every one of our ships does not occupy
                enemy_ship_counter += 1
    elif (game_map[one.__add__(ship.position)]).is_occupied:
        friend_ship_counter_one = 0
        for aship in me.get_ships():
            if not game_map[aship.position] == (game_map[one.__add__(ship.position)]):
                friend_ship_counter_one += 1
            if friend_ship_counter_one == len(me.get_ships()):
                enemy_ship_counter += 1
    elif (game_map[two.__add__(ship.position)]).is_occupied:
        friend_ship_counter_two = 0
        for aship in me.get_ships():
            if not game_map[aship.position] == (game_map[two.__add__(ship.position)]):
                friend_ship_counter_two += 1
            if friend_ship_counter_two == len(me.get_ships()):
                enemy_ship_counter += 1
    elif (game_map[three.__add__(ship.position)]).is_occupied:
        friend_ship_counter_three = 0
        for aship in me.get_ships():
            if not game_map[aship.position] == (game_map[three.__add__(ship.position)]):
                friend_ship_counter_three += 1
            if friend_ship_counter_three == len(me.get_ships()):
                enemy_ship_counter += 1