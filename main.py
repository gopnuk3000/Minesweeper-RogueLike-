import random
import sys
import pygame
from config.GameBoard import Minesweeper, CELL_SIZE, WHITE, screen, MINE
from config.ScreenGame import startGame, endGame, levelComplite, quizScreen
from config.GameSprites import MineImage

SCOREGAME, LEVEL, WIN = 0, 1, True


def Gamelevel(game, SCOREGAME, LEVEL, cntFlags):
    global screen

    cntFlag = 0
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
                    cell_y = (y // CELL_SIZE) - 4
                    if 0 <= cell_x < width and 0 <= cell_y < height:
                        if game.board[cell_y][cell_x] == -1 and not game.flags[cell_y][cell_x]:
                            SCOREGAME += random.randint(5, 10)
                        game.open_cell(cell_x, cell_y)

                        if game.board[cell_y][cell_x] == MINE:
                            if save_quiz:
                                size_past = game.getSize
                                bool_quest = quizScreen('easy')
                                game.set_size(size_past[0], size_past[1])
                                if bool_quest:
                                    save_quiz = False
                                    continue

                            for y in range(game.height):
                                for x in range(game.width):
                                    if game.flags[y][x]:
                                        game.flags[y][x] == False
                            game.draw()
                            game._reveal_all_mines()
                            running = False

                elif event.button == pygame.BUTTON_RIGHT:
                    x, y = event.pos
                    cell_x = x // CELL_SIZE
                    cell_y = (y // CELL_SIZE) - 4
                    if 0 <= cell_x < width and 0 <= cell_y < height:
                        game.set_flags(cell_x, cell_y)
                        if game.flags[cell_y][cell_x]:
                            if cntFlag < cntFlags:
                                cntFlag += 1
                            else:
                                game.set_flags(cell_x, cell_y)
                        else:
                            cntFlag -= 1
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

        text = font.render(f"Флагов: {cntFlag}/{cntFlags}", True, 'black')
        screen.blit(text, (15, 80))

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
            level, score = Gamelevel(game, SCOREGAME, LEVEL, _mins)
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
