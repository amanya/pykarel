class Exits:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.exits = [[False for i in range(cols)] for j in range(rows)]

    def dump(self):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.exits[i][j] == True:
                    yield i, j

    def add_exit(self, row, col):
        self.exits[row][col] = True

    def exit_present(self, row, col):
        return self.exits[row][col]
