import random
import sys
import pygame
from config.GameBoard import Minesweeper, CELL_SIZE, WHITE, screen, MINE
from config.ScreenGame import startGame, endGame, levelComplite, quizScreen
from config.GameSprites import MineImage

SCOREGAME, LEVEL, WIN = 0, 1, True


def Gamelevel(game, SCOREGAME, LEVEL):
    winLevel = False
    save_quiz = True
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    x, y = event.pos
                    cell_x = x // CELL_SIZE
                    cell_y = (y // CELL_SIZE) - 3
                    if 0 <= cell_x < width and 0 <= cell_y < height:
                        if game.board[cell_y][cell_x] == -1:
                            SCOREGAME += random.randint(5, 10)
                        game.open_cell(cell_x, cell_y)

                        if game.board[cell_y][cell_x] == MINE:
                            if save_quiz:
                                quizScreen('easy')
                                continue
                            game._reveal_all_mines()
                            running = False

                elif event.button == pygame.BUTTON_RIGHT:
                    x, y = event.pos
                    cell_x = x // CELL_SIZE
                    cell_y = (y // CELL_SIZE) - 3
                    if 0 <= cell_x < width and 0 <= cell_y < height:
                        game.open_flag_cell(cell_x, cell_y)
        screen.fill(WHITE)

        if game.check_win():
            game._reveal_all_mines()
            running = False
            winLevel = True

        game.draw()

        font = pygame.font.Font(None, 36)
        text = font.render(f"Очки: {SCOREGAME}", True, 'black')
        screen.blit(text, (15, 20))

        text = font.render(f"Уровень: {LEVEL}", True, 'black')
        screen.blit(text, (15, 50))
        pygame.display.flip()

        clock.tick(60)

    pygame.time.delay(900)

    return winLevel, SCOREGAME


if __name__ == '__main__':
    pygame.init()
    running = True
    while running:
        SCOREGAME, LEVEL, WIN = 0, 1, True
        width, height = 4, 4
        _mins = random.randint(1, 2)

        startGame()
        for _ in range(5):
            config = [random.randint(1, 2), random.randint(1, 2), random.randint(2, 3)]
            width += config[0]
            height += config[1]
            _mins += config[2]

            game = Minesweeper(width, height, _mins)
            level, score = Gamelevel(game, SCOREGAME, LEVEL)
            if not level:
                WIN = False
                SCOREGAME += score
                break
            levelComplite()
            LEVEL += 1
            SCOREGAME += score

        endGame(SCOREGAME, LEVEL, WIN)
    pygame.quit()
    sys.exit()
