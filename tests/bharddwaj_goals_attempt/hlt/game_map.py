import queue

from . import constants
from .entity import Entity, Shipyard, Ship, Dropoff
from .player import Player
from .positionals import Direction, Position
from .common import read_input



class MapCell:
    """A cell on the game map."""
    def __init__(self, position, halite_amount):
        self.position = position
        self.halite_amount = halite_amount
        self.ship = None
        self.structure = None
        self.booked = False

    @property
    def is_empty(self):
        """
        :return: Whether this cell has no ships or structures
        """
        return self.ship is None and self.structure is None

    @property
    def is_occupied(self):
        """
        :return: Whether this cell has any ships
        """
        return self.ship is not None

    @property
    def has_structure(self):
        """
        :return: Whether this cell has any structures
        """
        return self.structure is not None

    @property
    def structure_type(self):
        """
        :return: What is the structure type in this cell
        """
        return None if not self.structure else type(self.structure)

    def mark_unsafe(self, ship):
        """
        Mark this cell as unsafe (occupied) for navigation.

        Use in conjunction with GameMap.naive_navigate.
        """
        self.ship = ship

    def __eq__(self, other):
        return self.position == other.position

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'MapCell({}, halite={})'.format(self.position, self.halite_amount)


class GameMap:
    """
    The game map.

    Can be indexed by a position, or by a contained entity.
    Coordinates start at 0. Coordinates are normalized for you
    """
    def __init__(self, cells, width, height):
        self.width = width
        self.height = height
        self._cells = cells
        self._scanMap()


    def __getitem__(self, location):
        """
        Getter for position object or entity objects within the game map
        :param location: the position or entity to access in this map
        :return: the contents housing that cell or entity
        """
        if isinstance(location, Position):
            location = self.normalize(location)
            return self._cells[location.y][location.x]
        elif isinstance(location, Entity):
            return self._cells[location.position.y][location.position.x]
        return None

    def calculate_distance(self, source, target):
        """
        Compute the Manhattan distance between two locations.
        Accounts for wrap-around.
        :param source: The source from where to calculate
        :param target: The target to where calculate
        :return: The distance between these items
        """
        source = self.normalize(source)
        target = self.normalize(target)
        resulting_position = abs(source - target)
        return min(resulting_position.x, self.width - resulting_position.x) + \
            min(resulting_position.y, self.height - resulting_position.y)

    def normalize(self, position):
        """
        Normalized the position within the bounds of the toroidal map.
        i.e.: Takes a point which may or may not be within width and
        height bounds, and places it within those bounds considering
        wraparound.
        :param position: A position object.
        :return: A normalized position object fitting within the bounds of the map
        """
        return Position(position.x % self.width, position.y % self.height)

    @staticmethod
    def _get_target_direction(source, target):
        """
        Returns where in the cardinality spectrum the target is from source. e.g.: North, East; South, West; etc.
        NOTE: Ignores toroid
        :param source: The source position
        :param target: The target position
        :return: A tuple containing the target Direction. A tuple item (or both) could be None if within same coords
        """
        return (Direction.South if target.y > source.y else Direction.North if target.y < source.y else None,
                Direction.East if target.x > source.x else Direction.West if target.x < source.x else None)

    def get_unsafe_moves(self, source, destination):
        """
        Return the Direction(s) to move closer to the target point, or empty if the points are the same.
        This move mechanic does not account for collisions. The multiple directions are if both directional movements
        are viable.
        :param source: The starting position
        :param destination: The destination towards which you wish to move your object.
        :return: A list of valid (closest) Directions towards your target.
        """
        source = self.normalize(source)
        destination = self.normalize(destination)
        possible_moves = []
        distance = abs(destination - source)
        y_cardinality, x_cardinality = self._get_target_direction(source, destination)

        if distance.x != 0:
            possible_moves.append(x_cardinality if distance.x < (self.width / 2)
                                  else Direction.invert(x_cardinality))
        if distance.y != 0:
            possible_moves.append(y_cardinality if distance.y < (self.height / 2)
                                  else Direction.invert(y_cardinality))
        return possible_moves

    def naive_navigate(self, ship, destination):
        """
        Returns a singular safe move towards the destination.

        :param ship: The ship to move.
        :param destination: Ending position
        :return: A direction.
        """
        # No need to normalize destination, since get_unsafe_moves
        # does that
        for direction in self.get_unsafe_moves(ship.position, destination):
            target_pos = ship.position.directional_offset(direction)
            if not self[target_pos].is_occupied:
                self[target_pos].mark_unsafe(ship)
                return direction

        return Direction.Still

    def intelligent_navigate(self, ship, destination):
        """
        Returns a singular safe move towards the destination.
        This works in conjunction with a ship tracker that tracks whether or not ships already have a move
        WARNING: Do not use without understanding mechanics!

        :param ship: The ship to move.
        :param destination: Ending position
        :param definite: whether to hestitate about booking or not
        :return: A direction.
        """

        for direction in self.get_unsafe_moves(ship.position, destination):
            target_pos = ship.position.directional_offset(direction)
            if not self[target_pos].is_occupied and not self[target_pos].booked:
                self[target_pos].booked = True
                return direction

        for direction in self.get_unsafe_moves(ship.position, destination):
            target_pos = ship.position.directional_offset(direction)
            if not self[target_pos].booked:
                self[target_pos].booked = True
                return direction

        if not self[ship.position].booked:
            self[ship.position].booked = True
            return Direction.Still

        for direction in Direction.get_all_cardinals():
            target_pos = ship.position.directional_offset(direction)
            if not self[target_pos].booked:
                self[target_pos].booked = True
                return direction
        self[ship.position].booked = True
        return Direction.Still

    def getMostWealthyAdjacentCell(self, ship):
        maxHalite = 0
        bestCell = None

        for cardinal in ship.position.get_surrounding_cardinals():
            if not self[cardinal].is_occupied and not self[cardinal].booked:
                if self[cardinal].halite_amount > maxHalite:
                    maxHalite = self[cardinal].halite_amount
                    bestCell = cardinal

        # subtract ship.position to just get movement
        return (bestCell - ship.position) if bestCell else bestCell

    def updateGoalCells(self, wealthyMinimum, dropPoint,goalCells):
        """
        Return ordered list of wealthy cells by distance away from dropPoint

        :param wealthyMinimum: halite needed to be in list
        :param dropPoint: drop off or shipyard
        :return: True if found wealthy goal cells, False otherwise
        """
        for
        for i in range(self.width):
            for j in range(self.height):
                currentPosition = Position(i, j)
                if self[currentPosition].halite_amount > wealthyMinimum and not self[currentPosition].has_structure:
                    goalCells[ship.id] == Position(i,j)
        # logging.info(f"All wealthy cells: {goalCells}")
        goalCells.sort(key = lambda wealthyCell: ((self.calculate_distance(dropPoint.position, wealthyCell)) / self.width) - (self[wealthyCell].halite_amount / constants.MAX_HALITE))
        if goalCells:
            dropPoint.goalCells = goalCells
            return True
        return False

    def getTotalHaliteAroundAPoint(self, centerPosition, radius):
        totalHalite = 0
        for i in range(-radius, radius + 1): #x coordinate
            yCheck = radius - abs(i)
            for j in range(-yCheck, yCheck + 1): #y coordinate (+1 because the stop parameter is not included)
                checkingPosition = Position(i,j) + centerPosition
                totalHalite += self[checkingPosition].halite_amount
        return totalHalite


    def _scanMap(self):
        """
        Mark cells as safe for navigation (will re-mark unsafe cells later)
        """
        totalHaliteInMap = 0
        medianOfRows = []
        for y in range(self.height):
            medianOfRow = []
            for x in range(self.width):
                currentPosition = Position(x, y)
                self[currentPosition].ship = None
                self[currentPosition].booked = False
                totalHaliteInMap += self[currentPosition].halite_amount
                medianOfRow.append(self[currentPosition].halite_amount)
            medianOfRow.sort()
            middleOfMedianList = int(len(medianOfRow) / 2)
            median = (medianOfRow[middleOfMedianList] + medianOfRow[middleOfMedianList + 1]) / 2
            medianOfRows.append(median)
        medianOfRows.sort()
        middleOfMedianList = int(len(medianOfRows) / 2)
        self.medianHaliteAmount = (medianOfRows[middleOfMedianList] + medianOfRows[middleOfMedianList + 1]) / 2
        self.totalHalite = totalHaliteInMap
        self.averageHaliteAmount = totalHaliteInMap / (self.height * self.width)

    @staticmethod
    def _generate():
        """
        Creates a map object from the input given by the game engine
        :return: The map object
        """
        map_width, map_height = map(int, read_input().split())
        game_map = [[None for _ in range(map_width)] for _ in range(map_height)]
        for y_position in range(map_height):
            cells = read_input().split()
            for x_position in range(map_width):
                game_map[y_position][x_position] = MapCell(Position(x_position, y_position),
                                                           int(cells[x_position]))
        return GameMap(game_map, map_width, map_height)

    def _update(self):
        """
        Updates this map object from the input given by the game engine
        :return: nothing
        """

        # If stuff starts behaving weirdly,
        # put this for loop AFTER the next one
        for _ in range(int(read_input())):
            cell_x, cell_y, cell_energy = map(int, read_input().split())
            self[Position(cell_x, cell_y)].halite_amount = cell_energy

        self._scanMap()
