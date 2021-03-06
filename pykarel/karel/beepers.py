class Beepers:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.beepers = [[0 for i in range(cols)] for j in range(rows)]

    def dump(self):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.beepers[i][j] == 1:
                    yield i, j

    def beeper_present(self, row, col):
        return self.beepers[row][col] > 0

    def num_beepers(self, row, col):
        return self.beepers[row][col]

    def put_beeper(self, row, col):
        self.beepers[row][col] += 1

    def pick_beeper(self, row, col):
        self.beepers[row][col] -= 1
