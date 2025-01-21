import random
import sys
import pygame
from config.GameBoard import Minesweeper, CELL_SIZE, WHITE, screen, MINE
from config.ScreenGame import startGame, endGame

if __name__ == '__main__':
    pygame.init()
    width, height = 10, 10

    startGame()
    game = Minesweeper(width, height, random.randint(10, 16))

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
                    cell_y = y // CELL_SIZE
                    if 0 <= cell_x < width and 0 <= cell_y < height:
                        game.open_cell(cell_x, cell_y)

                        if game.board[cell_y][cell_x] == MINE:
                            game._reveal_all_mines()
                            running = False
                elif event.button == pygame.BUTTON_RIGHT:
                    x, y = event.pos
                    cell_x = x // CELL_SIZE
                    cell_y = y // CELL_SIZE
                    if 0 <= cell_x < width and 0 <= cell_y < height:
                        game.open_flag_cell(cell_x, cell_y)
        screen.fill(WHITE)
        game.draw()
        pygame.display.flip()

        clock.tick(60)

    pygame.time.delay(900)

    endGame()
    pygame.quit()