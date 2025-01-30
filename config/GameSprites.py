import pygame
from GameBoard import load_image


class MineImage(pygame.sprite.Sprite):
    bomb_image = load_image('bomb.png')
    boom_image = load_image('boom.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = self.bomb_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.image = self.boom_image


class FlagImage(pygame.sprite.Sprite):
    flag_image = load_image('flag.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = self.flag_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class GoldFlagImage(pygame.sprite.Sprite):
    # анимированный спрайт
    gold_flag_image = load_image('goldflag.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = self.gold_flag_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass
