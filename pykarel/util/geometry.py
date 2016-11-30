class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __src__(self):
        return "({}, {})".format(self.x, self.y)

    def move(self, x, y):
        self.x = x
        self.y = y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy


class Direction:
    def __init__(self, name="EAST"):
        self.name = name

    def __src__(self):
        return self.name

    @staticmethod
    def left_from(dir):
        ret = dict(NORTH=WEST, EAST=NORTH, SOUTH=EAST, WEST=SOUTH)
        if dir not in ret:
            raise Exception("Illegal direction value: {}:".format(dir))
        return ret[dir]

    @staticmethod
    def right_from(dir):
        ret = dict(NORTH=EAST, EAST=SOUTH, SOUTH=WEST, WEST=NORTH)
        if dir not in ret:
            raise Exception("Illegal direction value: {}:".format(dir))
        return ret[dir]

    @staticmethod
    def opposite(dir):
        ret = dict(NORTH=SOUTH, EAST=WEST, SOUTH=NORTH, WEST=EAST)
        if dir not in ret:
            raise Exception("Illegal direction value: {}:".format(dir))
        return ret[dir]

NORTH = Direction("NORTH")
EAST = Direction("EAST")
SOUTH = Direction("SOUTH")
WEST = Direction("WEST")


