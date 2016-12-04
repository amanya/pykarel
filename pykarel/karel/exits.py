class Exits:
    def __init__(self, rows, cols):
        self.exits = [[False for i in range(cols)] for j in range(rows)]

    def add_exit(self, row, col):
        self.exits[row][col] = True

    def exit_present(self, row, col):
        return self.exits[row][col]
