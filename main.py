import random
import sys
import pygame
from config.GameBoard import Minesweeper, CELL_SIZE, WHITE, screen, MINE
from config.ScreenGame import startGame, endGame, levelComplite, quizScreen
from config.GameSprites import MineImage

# очки, уровень, победа или нет
SCOREGAME, LEVEL, WIN = 0, 1, True
save_quiz = True

# функция уровня
def Gamelevel(game, SCOREGAME, LEVEL, cntFlags):
    global screen

    cntFlag = 0
    winLevel = False
    clock = pygame.time.Clock()
    running = True
    chance = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # октрытия ячейки или установка флага
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    x, y = event.pos
                    cell_x = x // CELL_SIZE
                    cell_y = (y // CELL_SIZE) - 4
                    if 0 <= cell_x < width and 0 <= cell_y < height:
                        if game.board[cell_y][cell_x] == -1 and not game.flags[cell_y][cell_x]:
                            if chance > random.randint(0, 100):
                                size_past = game.getSize
                                bool_quest = quizScreen('easy')
                                game.set_size(size_past[0], size_past[1])
                                if bool_quest:
                                    SCOREGAME += random.randint(5, 10)
                                    continue
                                else:
                                    game.draw()
                                    game._reveal_all_mines()
                                    running = False
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

        # прорисовка
        screen.fill(WHITE)

        if game.check_win():
            game._reveal_all_mines()
            running = False
            winLevel = True

        # отрисовка поля
        game.draw()

        # установка текста в игре
        font = pygame.font.Font(None, 36)
        text = font.render(f"Очки: {SCOREGAME}", True, 'black')
        screen.blit(text, (15, 20))

        text = font.render(f"Уровень: {LEVEL}", True, 'black')
        screen.blit(text, (15, 50))

        text = font.render(f"Флагов: {cntFlag}/{cntFlags}", True, 'black')
        screen.blit(text, (15, 80))

        pygame.display.flip()
        clock.tick(60)

    # задержка перед окончанием игры
    pygame.time.delay(900)

    return winLevel, SCOREGAME


# начало
if __name__ == '__main__':
    pygame.init()
    running = True
    while running:
        SCOREGAME, LEVEL, WIN = 0, 1, True
        width, height = 12, 12
        _mins = random.randint(1, 2)

        # заставка
        startGame()
        # 5 уровней: проходим - победа, иначе пройгрыш
        for _ in range(5):
            # генерация уровня: его усложнение
            config = [random.randint(1, 2), random.randint(1, 2), random.randint(2, 3)]
            width -= config[0]
            height -= config[1]
            _mins += config[2]

            game = Minesweeper(width, height, _mins)
            # генерация уровня: начало уровня
            level, score = Gamelevel(game, SCOREGAME, LEVEL, _mins)
            if not level:
                WIN = False
                SCOREGAME += score
                break
            # генерация уровня: прошли уровень
            levelComplite()
            LEVEL += 1
            SCOREGAME += score

        # заставка конечная
        endGame(SCOREGAME, LEVEL, WIN)
    pygame.quit()
    sys.exit()
