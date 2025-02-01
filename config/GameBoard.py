import random
import pygame
import os
import sys
from gamechanges.GoldFlag import GoldFlag
from gamechanges.QuizMine import QuizMine

CELL_SIZE = 30
MINE = 10
MINE_OPEN = 20
FLAG_MINE = (10, 15)
CLOSED = -1
QUIZES = {
    '2 * 2': '4'
}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (200, 200, 200)

# экран
size = 10 * CELL_SIZE, 10 * CELL_SIZE
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('image', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[CLOSED for _ in range(width)] for _ in range(height)]
        pygame.display.set_mode((width * CELL_SIZE, height * CELL_SIZE+90))

    @property
    def getSize(self):
        return pygame.display.get_window_size()

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE+90, CELL_SIZE, CELL_SIZE)

                if self.board[y][x] == CLOSED:
                    color = GREY
                elif self.board[y][x] == MINE or self.board[y][x] == FLAG_MINE[0]:
                    color = GREY
                elif self.board[y][x] == MINE_OPEN:
                    color = RED
                else:
                    color = WHITE

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

                if self.board[y][x] not in [CLOSED, MINE, MINE_OPEN, FLAG_MINE] and self.board[y][x] > 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(self.board[y][x]), True, BLACK)
                    screen.blit(text, (x * CELL_SIZE + 10, y * CELL_SIZE + 95))
                elif self.board[y][x] in [FLAG_MINE[1]] and self.board[y][x] > 0:
                    fon = pygame.transform.scale(load_image('flag.jpg'), (CELL_SIZE, CELL_SIZE))
                    screen.blit(fon, (x * CELL_SIZE + 10, y * CELL_SIZE + 95))


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

    def open_flag_cell(self,x,y):
        self.board[y][x] = FLAG_MINE

    def _count_mines(self, x, y):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.board[ny][nx] == MINE or self.board[y][x] == FLAG_MINE[0]:
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

    def _is_mine(self, x, y):
        return self.board[y][x] == MINE or self.board[y][x] == FLAG_MINE[0]

    def _reveal_all_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == MINE or self.board[y][x] == FLAG_MINE[0]:
                    self.board[y][x] = MINE_OPEN  # Убедимся, что мины останутся помеченными

    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != MINE and self.board[y][x] == CLOSED:
                    return False
        return True
        
    def gold_open(self, x, y):
        a = GoldFlag(self.width, self.height).used(x, y)
        for x, y in a:
            if self.board[x][y] != MINE:
                Minesweeper.open_cell(self, x, y)
            else:
                Minesweeper.open_flag_cell(self, x, y)

    def quiz_safe(self, x, y, quizes, answer):
        if Minesweeper._is_mine(self, x, y):
            QuizMine(quizes).used(self, random.randint(0, len(quizes)), answer)
