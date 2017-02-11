class Walls:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.walls = [[0 for i in range(cols)] for j in range(rows)]

    def dump(self):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.walls[i][j] == 1:
                    yield i, j

    def add_wall(self, row, col):
        self.walls[row][col] = 1

    def get_wall(self, row, col):
        return self.walls[row][col] != 1

    def is_move_valid(self, start_r, start_c, end_r, end_c):
        print(start_r, start_c, end_r, end_c)
        if end_c < 0 or end_c >= self.cols:
            return False
        if end_r < 0 or end_r >= self.rows:
            return False

        d_row = abs(end_r - start_r)
        d_col = abs(end_c - start_c)
        if d_row + d_col != 1:
            return False

        if start_c + 1 == end_c and self.walls[end_r][end_c] == 1:
            return False
        if start_c - 1 == end_c and self.walls[end_r][end_c] == 1:
            return False
        if start_r + 1 == end_r and self.walls[end_r][end_c] == 1:
            return False
        if start_r - 1 == end_r and self.walls[end_r][end_c] == 1:
            return False

        return True


