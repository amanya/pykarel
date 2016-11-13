class Walls:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.top_walls = [[0 for i in range(cols)] for j in range(rows)]
        self.right_walls = [[0 for i in range(cols)] for j in range(rows)]

    def add_top_wall(self, row, col):
        self.top_walls[row][col] = 1

    def add_right_wall(self, row, col):
        self.right_walls[row][col] = 1

    def top_wall(self, row, col):
        return self.top_walls[row][col] != 1

    def right_wall(self, row, col):
        return self.right_walls[row][col] != 1

    def is_move_valid(self, start_r, start_c, end_r, end_c):
        if end_c < 0 or end_c >= self.cols:
            return False
        if end_r < 0 or end_r >= self.rows:
            return False

        d_row = abs(end_r - start_r)
        d_col = abs(end_c - start_c)
        if d_row + d_col != 1:
            return False

        if start_c + 1 == end_c and self.right_walls[end_r][end_c]:
            return False
        if start_c - 1 == end_c and that.right_walls[end_r][end_c]:
            return False
        if start_r + 1 == end_r and that.top_walls[end_r][end_c]:
            return False
        if start_r - 1 == end_r and that.top_walls[end_r][end_c]:
            return False

        return True
