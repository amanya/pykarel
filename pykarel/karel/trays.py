class Tray:
    def __init__(self, capacity, required, initial_beepers):
        self.capacity = capacity
        self.required = required
        self.num_beepers = initial_beepers

    def put_beeper(self):
        if self.num_beepers > self.capacity:
            raise Exception("Tray is full")
        self.num_beepers += 1

    def pick_beeper(self):
        if not self.num_beepers:
            raise Exception("Tray is empty")
        self.num_beepers -= 1

class Trays:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.trays = [[None for i in range(cols)] for j in range(rows)]

    def dump(self):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.trays[i][j] != None:
                    tray = self.trays[i][j]
                    yield i, j, tray.capacity, tray.required, tray.num_beepers

    def add_tray(self, row, col, capacity, required, initial_beepers):
        self.trays[row][col] = Tray(capacity, required, initial_beepers)

    def tray_present(self, row, col):
        if self.trays[row][col]:
            return True
        else:
            return False

    def tray_is_full(self, row, col):
        tray = self.trays[row][col]
        if not tray:
            raise Exception("Not tray in cell")
        return tray.capacity == tray.num_beepers

    def tray_is_empty(self, row, col):
        tray = self.trays[row][col]
        if not tray:
            raise Exception("Not tray in cell")
        return tray.num_beepers == 0

    def tray_is_complete(self, row, col):
        tray = self.trays[row][col]
        if not tray:
            raise Exception("Not tray in cell")
        return tray.num_beepers == tray.required

    def put_beeper(self, row, col):
        if not self.trays[row][col]:
            raise Exception("Not tray in cell")
        self.trays[row][col].put_beeper()

    def pick_beeper(self, row, col):
        if not self.trays[row][col]:
            raise Exception("Not tray in cell")
        self.trays[row][col].pick_beeper()
