import numpy as np
import time
import itertools


class Board:
    def __init__(self, n):
        if n < 4:
            raise ValueError("n must be greater than 4")

        row = [1 if x == 0 else 0 for x in range(n)]
        self.board = np.array([row for _ in range(n)])
        self.n = n
        self.iters = 1
        self.solutions = 0

    def __repr__(self):
        return str('\n'.join(['  '.join(list(map(str, line))) for line in self.board]))

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        for line in self.board:
            yield line

    def __getitem__(self, item):
        return self.board[item]

    def __setitem__(self, key, value):
        self.board[key] = value

    def check(self):
        # Return True if the test is passed and the current config is a solution, else return False
        if self.__check_diag():
            return False
        for i in range(self.n):
            for j in range(self.n):
                val = self[i][j]
                if self.__check_col(i):
                    return False
        return True

    def __check_col(self, index):
        # If there are queens, return True
        queens = 0
        for line in self:
            if line[index] == 1:
                queens += 1
        if queens > 1:
            return True
        else:
            return False

    def __check_diag(self):
        # If there are queens, return True
        all_queens_right = [ix+iy for ix, row in enumerate(self) for iy, i in enumerate(row) if i == 1]
        if len(set(all_queens_right)) < len(all_queens_right):
            return True
        else:
            all_queens_left = [ix - iy for ix, row in enumerate(self) for iy, i in enumerate(row) if i == 1]
            if len(set(all_queens_left)) < len(all_queens_right):
                return True
        return False

    def is_origin(self, row):
        if [i for i, val in enumerate(row) if val == 1][0] == 0:
            return True
        return False

    def end_state(self):
        for line in self:
            if line[-1] != 1:
                return False
        return True

    def advance_row(self, row_ind):
        row = self[row_ind]
        current_poss = [i for i, val in enumerate(row) if val == 1][0]
        if current_poss == self.n-1:
            new_poss = 0
            self.advance_row(row_ind + 1)
        else:
            new_poss = current_poss + 1
        self[row_ind][current_poss] = 0
        self[row_ind][new_poss] = 1

    def solve(self):
        runtime = time.thread_time()
        while not self.end_state():
            if self.check():
                self.solutions += 1
                print("\n")
                print(self)
            self.advance_row(0)
            self.iters += 1
        return self.solutions, self.iters, time.thread_time()-runtime

    def translate(self, positions):
        self.board = np.array([[0 for _ in range(self.n)] for _ in range(self.n)])
        for pos in positions:
            self[pos[0]][pos[1]] = 1

    def better_solve(self):
        newBoard = np.array([[1 if x == i else 0 for x in range(self.n)] for i in range(self.n)])
        all_pos = [(ix, iy) for ix, row in enumerate(newBoard) for iy, i in enumerate(row) if i == 1]
        all_poss = list(itertools.permutations(all_pos))
        runtime = time.thread_time()
        for poss in all_poss:
            self.translate(poss)
            if self.check():
                self.solutions += 1
                print("\n")
                print(self)
            self.iters += 1
        return self.solutions, self.iters, time.thread_time()-runtime


def main():
    board = Board(8)
    solutions, iters, runtime = board.better_solve()
    print(f"Ran {board.n}x{board.n} board in {runtime}\nSolutions: {solutions}\nIterations: {iters}")


if __name__ == "__main__":
    main()
