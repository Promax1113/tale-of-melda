
import os
import pygame
from .game_controller import Controller



class Bullet:
    def __init__(self, author):
        self.author = author

        # box.png is a placeholder
        self.img = pygame.image.load(f"{os.getcwd()}/game_data/sprites/map/box.png")
        self.x, self.y = author.rect.x, author.rect.y


        self.speed = 5

    def draw_and_move(self, game_controller: Controller, screen: pygame.Surface):
        if self.author.direction == 1 or self.author.direction == 3:
            self.y += self.speed
        screen.blit(self.img, (self.x, self.y))
