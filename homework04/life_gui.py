import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 20, speed: int = 10) -> None:
        super().__init__(life)
        self.width = life.cols
        self.height = life.rows
        self.cell_size = cell_size
        self.w = self.height * self.cell_size
        self.h = self.width * self.cell_size
        self.screen_size = self.h, self.w
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed
        self.paused = False
        self.mouse = False
        self.pos = -1, -1

    def draw_lines(self) -> None:
        for x in range(0, self.h, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.w))
        for y in range(0, self.w, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.h, y))

    def draw_grid(self) -> None:
        g = self.life.curr_generation
        p = self.width
        t = self.height
        for i in range(p):
            for j in range(t):
                if g[j][i] == 0:
                    pygame.draw.rect(
                        self.screen, "white", (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
                    )
                else:
                    pygame.draw.rect(
                        self.screen, "green", (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
                    )

    def run(self) -> None:
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
                elif event.type == pygame.KEYDOWN:
                    if self.paused:
                        self.paused = False
                        self.pos = -1, -1
                    else:
                        self.paused = True
                if self.paused:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.pos = event.pos
                        p = self.pos
                        c_s = self.cell_size
                        i = p[0] // c_s * c_s
                        j = p[1] // c_s * c_s
                        if self.life.curr_generation[j // c_s][i // c_s] == 0:
                            self.life.curr_generation[j // c_s][i // c_s] = 1
                            self.draw_grid()
                            self.draw_lines()
                        else:
                            self.life.curr_generation[j // c_s][i // c_s] = 0
                            self.draw_grid()
                            self.draw_lines()
                else:
                    self.draw_grid()
                    self.draw_lines()
                    self.life.step()
                    clock.tick(self.speed)
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife((240, 320), True)
    ui = GUI(game)
    ui.run()
