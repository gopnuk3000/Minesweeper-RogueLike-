import sys

import pygame
from config.GameBoard import size, load_image, screen

def startGame():
    intro_text = ["Сапер рогалик", "",
                  "Открывайте клетки, и не попадитесь на мины",
                  "с каждым уровнем все сложнее и сложнее,",
                  "Удачи!"]

    fon = pygame.transform.scale(load_image('fon.png'), (size[0], size[1]))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)