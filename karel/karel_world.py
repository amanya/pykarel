from .karel import INFINITY, INCREMENT, DECREMENT, Karel
from ..scanner.token_scanner import TokenScanner
from ..util.geometry import Point, SOUTH, NORTH, WEST, EAST


class Corner:
    nbeepers = 0
    color = None


class KarelWorld:
    DEFAULT_WIDTH = 10
    DEFAULT_HEIGHT = 10
    DEFAULT_SPEED = 0.5

    views = []
    pathname = ""

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        self.width = width
        self.height = height
        self.speed = KarelWorld.DEFAULT_SPEED
        self.karels = []
        self.map = {}
        self.bag_count = 0
        self.last_karel = None
        for x in range(1, self.width):
            for y in range(1, self.height):
                self.map[Point(x, y)] = Corner()
        for x in range(1, self.width):
            self.set_wall(Point(x, 1), SOUTH)
            self.set_wall(Point(x, self.height), NORTH)
        for y in range(1, self.height):
            self.set_wall(Point(1, y), WEST)
            self.set_wall(Point(self.width, y), EAST)

    def add_karel(self, karel):
        karel.world = self
        self.karels.append(karel)

    def remove_karel(self, karel):
        self.karels.remove(karel)
        karel.world = None

    def get_karel(self, index=0):
        return self.karels[index]

    def get_karel_count(self):
        return len(self.karels)

    def add_view(self, view):
        self.views.append(view)

    def remove_view(self, view):
        self.views.remove(view)

    def update_views(self):
        for view in self.views:
            view.repaint()

    @staticmethod
    def get_path_name():
        return KarelWorld.pathname

    @staticmethod
    def set_path_name(pathname):
        KarelWorld.pathname = pathname

    def in_bounds(self, pt):
        return 0 < pt.x <= self.width and 0 < pt.y <= self.height

    def get_beepers_on_corner(self, pt):
        return self.map[pt].nbeepers

    def set_beepers_on_corner(self, pt, n):
        if n == INCREMENT:
            if self.map[pt].numbeepers is not INFINITY:
                self.map[pt].nbeepers += 1
        elif n == DECREMENT:
            if self.map[pt].numbeepers is not INFINITY and self.map[pt].nbeepers is not 0:
                self.map[pt].nbeepers -= 1
        else:
            self.map[pt].nbeepers = n

    def check_wall(self, pt, dir):
        return self.map[pt][str(dir)]

    def set_wall(self, pt, dir, state=True):
        neighbor = Karel.adjacent_corner(pt, dir)
        if dir == NORTH:
            self.map[pt]["NORTH"] = state
            if self.in_bounds(neighbor):
                self.map[neighbor]["SOUTH"] = state
        elif dir == EAST:
            self.map[pt]["EAST"] = state
            if self.in_bounds(neighbor):
                self.map[neighbor]["WEST"] = state
        elif dir == SOUTH:
            self.map[pt]["SOUTH"] = state
            if self.in_bounds(neighbor):
                self.map[neighbor]["NORTH"] = state
        elif dir == WEST:
            self.map[pt]["WEST"] = state
            if self.in_bounds(neighbor):
                self.map[neighbor]["EAST"] = state

    def clear_wall(self, pt, dir):
        self.set_wall(pt, dir, False)

    @staticmethod
    def load(input_str):
        scanner = TokenScanner()
        scanner.ignore_whitespace = True
        scanner.ignore_comments = True
        scanner.scan_numbers_flag = True
        scanner.set_input(input_str)
        while True:
            token = scanner.next_token()
            if token == "":
                break
            if token is not ";":
                scanner.verify_token(":")
                cmd = token.lower() + "Command"
                if cmd not in globals():
                    raise Exception('Illegal map file keyword "{}"'.format(token))
                globals()[cmd](scanner)

    def dimension_command(self, scanner):
        pt = self.scan_point(scanner)
        scanner.verify_token(";")
        self.__init__(pt.x, pt.y)

    def karel_command(self, scanner):
        pt = self.scan_point(scanner)
        dir = self.scan_direction(scanner) or EAST
        nbeepers = self.scan_beeper_count(scanner)
        if nbeepers is None:
            nbeepers = self.bag_count
        scanner.verify_token(";")
        karel = Karel()
        karel.set_location(pt)
        karel.set_direction(dir)
        karel.set_beepers_in_bag(nbeepers)
        self.add_karel(karel)
        self.last_karel = karel

    def wall_command(self, scanner):
        pt = self.scan_point(scanner)
        dir = self.scan_direction(scanner)
        if not dir:
            raise Exception("Missing direction in wall command")
        scanner.verify_token(";")
        self.set_wall(pt, dir)

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def speed_command(self, scanner):
        try:
            speed = float(scanner.next_token())
        except ValueError:
            raise Exception("Illegal speed value")
        if speed < 0 or speed > 1:
            raise Exception("Illegal speed value")
        scanner.verify_token(";")
        self.speed = speed

    def beeper_command(self, scanner):
        pt = self.scan_point(scanner)
        nbeepers = self.scan_beeper_count(scanner)
        scanner.verify_token(";")
        self.set_beepers_on_corner(pt, nbeepers)

    def beeper_bag_command(self, scanner):
        self.bag_count = self.scan_beeper_count(scanner)
        scanner.verify_token(";")
        if self.last_karel:
            self.last_karel.set_beepers_in_bag(self.bag_count)

    @staticmethod
    def scan_point(scanner):
        scanner.verify_token("(")
        token = scanner.next_token()
        try:
            x = int(token)
        except ValueError:
            raise Exception("{} is not a valid integer".format(token))
        scanner.verify_token(",")
        token = scanner.next_token()
        try:
            y = int(token)
        except ValueError:
            raise Exception("{} is not a valid integer".format(token))
        scanner.verify_token(")")
        return Point(x, y)

    @staticmethod
    def scan_direction(scanner):
        token = scanner.next_token().upper()
        dir = None
        if token is "NORTH":
            dir = NORTH
        elif token is "EAST":
            dir = EAST
        elif token is "SOUTH":
            dir = SOUTH
        elif token is "WEST":
            dir = WEST
        else:
            scanner.save_token(token)
        return dir

    @staticmethod
    def scan_beeper_count(scanner):
        token = scanner.next_token().upper()
        if token in ["INFINITE", "INFINITY"]:
            nbeepers = INFINITY
        else:
            try:
                nbeepers = int(token)
            except ValueError:
                nbeepers = None
                scanner.save_token(token)
        return nbeepers

    def save(self):
        out = "Dimension: ({}, {})\n".format(self.width, self.height)
        pt = Point()
        for y in range(1, self.height):
            for x in range(1, self.width):
                if y < self.height and self.check_wall(pt, NORTH):
                    out += "Wall: {} NORTH\n".format(Point(x, y))
                if x < self.width and self.check_wall(pt, EAST):
                    out += "Wall: {} EAST\n".format(Point(x, y))
        for y in range(1, self.height):
            for x in range(1, self.width):
                nbeepers = self.get_beepers_on_corner(Point(x, y))
                if nbeepers > 0:
                    out += "Beeper: {} {}\n".format(Point(x, y), nbeepers)
        for karel in self.karels:
            out += "Karel: {} {}\n".format(karel.pt, karel.dir)
            out += "BeeperBag: {}\n".format(karel.beepers_in_bag)
        return out

