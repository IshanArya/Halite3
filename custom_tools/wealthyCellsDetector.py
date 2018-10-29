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
