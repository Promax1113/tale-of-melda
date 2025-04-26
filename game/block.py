import os

import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, type: str, pos: tuple):
        super().__init__()
        path = f"{os.getcwd()}/game_data/sprites/map/"
        textures: dict = {}
        for texture in os.listdir(path):
            if os.path.isfile(path + texture):
                img = pygame.transform.scale(pygame.image.load(f"{path}{texture}"), (48,48))
                textures[texture.split(".")[0]] = img
        self.img = textures[type]
        self.rect = self.img.get_rect()
        self.rect.x ,self.rect.y = pos
    def draw_to_screen(self, screen: pygame.Surface):
        screen.blit(self.img, (self.rect.x, self.rect.y))
        