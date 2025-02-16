import json
import random
import pygame
import os
import sys
from config.gamechanges.GoldFlag import GoldFlag
from config.GameSprites import FlagImage, GoldFlagImage, MineImage

# константы для удобства
CELL_SIZE = 30
MINE = 10
MINE_OPEN = 20
CLOSED = -1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (200, 200, 200)
BLUE = (0, 0, 255)

# экран
size = 10 * CELL_SIZE, 10 * CELL_SIZE
screen = pygame.display.set_mode(size)


# загрузка изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('image', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

group_bomb = pygame.sprite.Group()

# поле игры: зарисовка поля в зависимости от того, какое оно: пустое, мина, флаг и т.д.
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[CLOSED for _ in range(width)] for _ in range(height)]
        self.flags = [[False for _ in range(width)] for _ in range(height)]
        pygame.display.set_mode((width * CELL_SIZE, height * CELL_SIZE+120))

    # взять текущее разрешение экрана
    @property
    def getSize(self):
        return pygame.display.get_window_size()

    # установить разрешение экрана
    def set_size(self, x, y):
        screen = pygame.display.set_mode((x,y))

    # рисовка поля
    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE+120, CELL_SIZE, CELL_SIZE)

                if self.board[y][x] == CLOSED or self.board[y][x] == MINE:
                    color = GREY
                elif self.board[y][x] == MINE_OPEN:
                    color = RED
                else:
                    color = WHITE

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

                if self.board[y][x] not in [CLOSED, MINE, MINE_OPEN] and self.board[y][x] > 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(self.board[y][x]), True, BLACK)
                    screen.blit(text, (x * CELL_SIZE + 10, y * CELL_SIZE + 125))
                elif self.board[y][x] in [MINE_OPEN]:
                    img_bomb = MineImage.bomb_image
                    img_bomb = pygame.transform.scale(img_bomb, (34, 34))
                    screen.blit(img_bomb, (x * CELL_SIZE, y * CELL_SIZE + 115))
                elif self.flags[y][x]:
                    if not self.flags[y][x]:
                        color = GREY
                        pygame.draw.rect(screen, color, rect)
                    else:
                        img_flag = FlagImage.flag_image
                        img_flag = pygame.transform.scale(img_flag, (30, 33))
                        screen.blit(img_flag, (x * CELL_SIZE, y * CELL_SIZE + 115))


# класс сапера: мины, открытие клеток и т.д.
class Minesweeper(Board):
    def __init__(self, width, height, num_mines):
        super().__init__(width, height)
        self.num_mines = num_mines
        self._place_mines()

    # расположение мин
    def _place_mines(self):
        count = 0
        while count < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] != MINE:
                self.board[y][x] = MINE
                count += 1

    # открытие ячейки если закрыта и нету на нем флага
    def open_cell(self, x, y):
        if self.board[y][x] == CLOSED and not self.flags[y][x]:
            mines_count = self._count_mines(x, y)
            self.board[y][x] = mines_count


            if mines_count == 0:
                self._open_neighbours(x, y)

    # установка флага
    def set_flags(self, x, y):
        self.flags[y][x] = not self.flags[y][x]

    # счетчик мин
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

    # открытие соседних мин и если на них нету флага
    def _open_neighbours(self, x, y):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.board[ny][nx] == CLOSED and not self.flags[ny][nx]:
                        self.open_cell(nx, ny)

    # проверка на мину
    def _is_mine(self, x, y):
        return self.board[y][x] == MINE

    # открытие всех мин
    def _reveal_all_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == MINE:
                    self.board[y][x] = MINE_OPEN  # Убедимся, что мины останутся помеченными

    # проверка на победу
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
                Minesweeper.open_cell(x, y)
            else:
                Minesweeper.set_flags(x, y)
