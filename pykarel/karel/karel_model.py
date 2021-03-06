import json

from .beepers import Beepers
from .karel_constants import KAREL_EAST, KAREL_WEST, KAREL_NORTH, KAREL_SOUTH
from .walls import Walls


def error(txt):
    print(txt)


def log(txt):
    print(txt)


class KarelModel:
    def __init__(self):
        self.dir = KAREL_EAST
        self.karel_row = 0
        self.karel_col = 0
        self.beepers = None
        self.trays = None
        self.exits = None
        self.walls = None
        self.square_colors = None
        self.rows = 0
        self.cols = 0
        self.bag = 0

    def exit(self):
        if self.exits.exit_present(self.karel_row, self.karel_col):
            return True
        return False

    def move(self):
        new_row = self.karel_row
        new_col = self.karel_col
        if self.dir == KAREL_EAST:
            new_col += 1
        elif self.dir == KAREL_WEST:
            new_col -= 1
        elif self.dir == KAREL_NORTH:
            new_row -= 1
        elif self.dir == KAREL_SOUTH:
            new_row += 1
        if self.walls.is_move_valid(self.karel_row, self.karel_col, new_row, new_col):
            self.karel_row = new_row
            self.karel_col = new_col
            log("row: {} col: {}".format(new_row, new_col))
            return True
        else:
            error("Front is blocked")
        return False

    def turn_left(self):
        new_d = self.dir
        if self.dir == KAREL_EAST:
            new_d = KAREL_NORTH
            log("dir: {}".format(new_d))
        elif self.dir == KAREL_WEST:
            new_d = KAREL_SOUTH
            log("dir: {}".format(new_d))
        elif self.dir == KAREL_NORTH:
            new_d = KAREL_WEST
            log("dir: {}".format(new_d))
        elif self.dir == KAREL_SOUTH:
            new_d = KAREL_EAST
            log("dir: {}".format(new_d))
        else:
            error("invalid dir: {}".format(self.dir))
        self.dir = new_d

    def turn_right(self):
        new_d = self.dir
        if self.dir == KAREL_EAST:
            new_d = KAREL_SOUTH
            log("dir: {}".format(new_d))
        elif self.dir == KAREL_WEST:
            new_d = KAREL_NORTH
            log("dir: {}".format(new_d))
        elif self.dir == KAREL_NORTH:
            new_d = KAREL_EAST
            log("dir: {}".format(new_d))
        elif self.dir == KAREL_SOUTH:
            new_d = KAREL_WEST
            log("dir: {}".format(new_d))
        else:
            error("invalid dir: {}".format(self.dir))
        self.dir = new_d

    def get_direction(self):
        return self.dir

    def get_num_rows(self):
        return self.rows

    def get_num_cols(self):
        return self.cols

    def get_karel_row(self):
        return self.karel_row

    def get_karel_col(self):
        return self.karel_col

    def get_num_beepers(self, row, col):
        return self.beepers.get_num_beepers(row, col)

    def has_wall(self, row, col):
        return self.walls.get_wall(row, col)

    def beepers_present(self):
        return self.beepers.beeper_present(self.karel_row, self.karel_col)

    def frontIsClear(self):
        new_row = self.karel_row
        new_col = self.karel_col
        if self.dir is KAREL_EAST:
            new_col += 1
        elif self.dir is KAREL_WEST:
            new_col -= 1
        elif self.dir is KAREL_NORTH:
            new_row -= 1
        elif self.dir is KAREL_SOUTH:
            new_row += 1
        else:
            error("invalid dir: {}".format(self.dir))
        ret = self.walls.is_move_valid(self.karel_row, self.karel_col, new_row, new_col)
        return ret

    def load_world(self, world_text):
        world = json.loads(world_text)

        self.rows = world["dimension"][0]
        self.cols = world["dimension"][1]

        self.beepers = Beepers(self.rows, self.cols)
        self.walls = Walls(self.rows, self.cols)

        self.dir = KAREL_EAST

        for beeper in world["beepers"]:
            self.beepers.put_beeper(beeper[0], beeper[1])

        for wall in world["walls"]:
            self.walls.add_wall(wall[0], wall[1])
