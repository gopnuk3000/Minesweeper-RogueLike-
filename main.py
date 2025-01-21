import random
import pygame
from config.GameBoard import Minesweeper, CELL_SIZE, WHITE, screen, size

if __name__ == '__main__':
    pygame.init()
    width, height = 10, 15
    game = Minesweeper(10, 15, random.randint(10, 16))

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                cell_x = x // CELL_SIZE
                cell_y = y // CELL_SIZE
                if 0 <= cell_x < width and 0 <= cell_y < height:
                    game.open_cell(cell_x, cell_y)
        screen.fill(WHITE)
        game.draw()
        pygame.display.flip()

        clock.tick(60)
    pygame.quit()
