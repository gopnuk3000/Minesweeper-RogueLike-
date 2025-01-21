import random
import pygame

CELL_SIZE = 30
MINE = 10
CLOSED = -1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (200, 200, 200)

# экран
size = 500, 500
screen = pygame.display.set_mode(size)

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[CLOSED for _ in range(width)] for _ in range(height)]

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                if self.board[y][x] == CLOSED:
                    color = GREY
                elif self.board[y][x] == MINE:
                    color = RED
                else:
                    color = WHITE

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

                if self.board[y][x] not in [CLOSED, MINE] and self.board[y][x] > 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(self.board[y][x]), True, BLACK)
                    screen.blit(text, (x * CELL_SIZE + 10, y * CELL_SIZE + 5))


class Minesweeper(Board):
    def __init__(self, width, height, num_mines):
        super().__init__(width, height)
        self.num_mines = num_mines
        self._place_mines()

    def _place_mines(self):
        count = 0
        while count < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] != MINE:
                self.board[y][x] = MINE
                count += 1

    def open_cell(self, x, y):
        if self.board[y][x] == CLOSED:
            mines_count = self._count_mines(x, y)
            self.board[y][x] = mines_count

            if mines_count == 0:
                self._open_neighbours(x, y)

    def _count_mines(self, x, y):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.board[ny][nx] == MINE:
                        count += 1
        return count

    def _open_neighbours(self, x, y):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.board[ny][nx] == CLOSED:
                        self.open_cell(nx, ny)
