import pygame
import os
import sys

def load_image(name, color_key=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


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
