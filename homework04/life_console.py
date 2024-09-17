import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.width = life.cols
        self.height = life.rows

    def draw_borders(self, screen) -> None:
        w = self.width
        h = self.height
        for b2 in range(w + 2):
            screen.addstr(0, b2, "#")
        for b2 in range(h + 2):
            screen.addch(b2, 0, "#")
        for b2 in range(w + 2):
            screen.addstr(h + 1, b2, "#")
        for b2 in range(h + 2):
            screen.addch(b2, w + 1, "#")

    def draw_grid(self, screen) -> None:
        cur = self.life.curr_generation
        w = self.width
        h = self.height
        for i in range(h):
            for j in range(w):
                if cur[i][j] == 1:
                    screen.addch(i + 1, j + 1, "+")

    def run(self) -> None:
        curses.initscr()
        stdscr = curses.newwin(1000, 1000, 0, 0)
        while self.life.is_max_generations_exceeded == False and self.life.is_changing:
            stdscr.clear()
            self.draw_borders(stdscr)
            curses.delay_output(200)
            stdscr.scrollok(True)
            self.draw_grid(stdscr)
            self.life.step()
            stdscr.refresh()


if __name__ == "__main__":
    game = GameOfLife((24, 32), True)
    ui = Console(game)
    ui.run()
