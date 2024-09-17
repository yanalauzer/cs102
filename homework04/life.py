import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0] * self.cols for _ in range(self.rows)]
        if randomize:
            r = [0, 1]
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.choice(r)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        x, y = cell
        C = []
        g = self.curr_generation
        if x != 0:
            C.append(g[x - 1][y])
        if y != 0:
            C.append(g[x][y - 1])
        if y != self.cols - 1:
            C.append(g[x][y + 1])
        if x != self.rows - 1:
            C.append(g[x + 1][y])
        if x != 0 and y != 0:
            C.append(g[x - 1][y - 1])
        if x != 0 and y != self.cols - 1:
            C.append(g[x - 1][y + 1])
        if x != self.rows - 1 and y != 0:
            C.append(g[x + 1][y - 1])
        if x != self.rows - 1 and y != self.cols - 1:
            C.append(g[x + 1][y + 1])
        return C

    def get_next_generation(self) -> Grid:
        v = [[0] * self.cols for _ in range(self.rows)]
        p = self.curr_generation
        for i in range(self.rows):
            for j in range(self.cols):
                if p[i][j] == 0:
                    if sum(self.get_neighbours((i, j))) == 3:
                        v[i][j] = 1
                    else:
                        v[i][j] = 0
                if p[i][j] == 1:
                    if sum(self.get_neighbours((i, j))) == 2 or sum(self.get_neighbours((i, j))) == 3:
                        v[i][j] = 1
                    else:
                        v[i][j] = 0
        return v

    def step(self) -> None:
        self.prev_generation = list(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.max_generations and self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        pr = self.prev_generation
        cu = self.curr_generation
        for i in range(self.rows):
            for j in range(self.cols):
                if pr[i][j] != cu[i][j]:
                    return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        f = open(filename)
        stroki = f.readlines()
        x = len(stroki)
        y = len(stroki[0]) - 1
        g = [[0] * y for _ in range(x)]
        game = GameOfLife((y, x))
        for i in range(x):
            for w in range(y):
                game.curr_generation[i][w] = int(stroki[i][w])
        return game

    def save(self, filename: pathlib.Path) -> None:
        f = open(filename, "w")
        r = self.rows
        c = self.cols
        cur = self.curr_generation
        for i in range(r):
            for g in range(c):
                f.write(str(cur[i][g]))
            f.write("\n")
