import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0] * self.cell_width for _ in range(self.cell_height)]
        if randomize:
            r = [0, 1]
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    grid[i][j] = random.choice(r)
        return grid

    def draw_grid(self) -> None:
        g = self.grid
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                if g[j][i] == 0:
                    pygame.draw.rect(
                        self.screen, "white", (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
                    )
                else:
                    pygame.draw.rect(
                        self.screen, "pink", (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
                    )

    def get_neighbours(self, cell: Cell) -> Cells:
        x, y = cell
        C = []
        g = self.grid
        if x != 0:
            C.append(g[x - 1][y])
        if y != 0:
            C.append(g[x][y - 1])
        if y != self.cell_width - 1:
            C.append(g[x][y + 1])
        if x != self.cell_height - 1:
            C.append(g[x + 1][y])
        if x != 0 and y != 0:
            C.append(g[x - 1][y - 1])
        if x != 0 and y != self.cell_width - 1:
            C.append(g[x - 1][y + 1])
        if x != self.cell_height - 1 and y != 0:
            C.append(g[x + 1][y - 1])
        if x != self.cell_height - 1 and y != self.cell_width - 1:
            C.append(g[x + 1][y + 1])
        return C

    def get_next_generation(self) -> Grid:
        v = [[0] * self.cell_width for _ in range(self.cell_height)]
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j] == 0:
                    if sum(self.get_neighbours((i, j))) == 3:
                        v[i][j] = 1
                    else:
                        v[i][j] = 0
                if self.grid[i][j] == 1:
                    if sum(self.get_neighbours((i, j))) == 2 or sum(self.get_neighbours((i, j))) == 3:
                        v[i][j] = 1
                    else:
                        v[i][j] = 0
        return v


if __name__ == "__main__":
    game = GameOfLife(240, 320, 20)
    game.run()
