import random
from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15):
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param coord:
    :return:
    """
    thechoice = ["up", "right"]
    i, j = coord[0], coord[1]
    route = random.choice(thechoice)
    if route == "up":
        if i != 1:
            grid[i - 1][j] = " "
        elif j + 2 != len(grid[0]):
            grid[i][j + 1] = " "
    else:
        if j + 2 != len(grid[0]):
            grid[i][j + 1] = " "
        elif i != 1:
            grid[i - 1][j] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

grid = create_grid(rows, cols)
empty_cells = []
for x, row in enumerate(grid):
    for y, _ in enumerate(row):
        if x % 2 != 0 and y % 2 != 0:
            grid[x][y] = " "
            empty_cells.append((x, y))

# 1. выбрать любую клетку
# 2. выбрать направление: наверх или направо.
# Если в выбранном направлении следующая клетка лежит за границами поля,
# выбрать второе возможное направление
# 3. перейти в следующую клетку, сносим между клетками стену
# 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

for i in empty_cells:
    grid = remove_wall(grid, i)

# генерация входа и выхода
if random_exit:
    x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
    y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
    y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
else:
    x_in, y_in = 0, cols - 2
    x_out, y_out = rows - 1, 1

grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """

    list1 = []
    for x, row in enumerate(grid):
        if "X" in row:
            for y, _ in enumerate(row):
                if grid[x][y] == "X":
                    list1.append((x, y))
    return list1


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
:param grid:
    :param k:
    :return:
    """
    cells = []
    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if grid[i][j] == k:
                cells.append([i, j])
    for q in range(len(cells)):
        x, y = cells[q][0], cells[q][1]
        if y != 0 and grid[x][y - 1] == " ":
            grid[x][y - 1] = k + 1
        elif y != 0 and grid[x][y - 1] == 0:
            grid[x][y - 1] = k + 1
        if x != 0 and grid[x - 1][y] == " ":
            grid[x - 1][y] = k + 1
        elif x != 0 and grid[x - 1][y] == 0:
            grid[x - 1][y] = k + 1
        if y != len(grid) - 1 and grid[x][y + 1] == " ":
            grid[x][y + 1] = k + 1
        elif y != len(grid) - 1 and grid[x][y + 1] == 0:
            grid[x][y + 1] = k + 1
        if x != len(grid) - 1 and grid[x + 1][y] == " ":
            grid[x + 1][y] = k + 1
        elif x != len(grid) - 1 and grid[x + 1][y] == 0:
            grid[x + 1][y] = k + 1
    return grid