import math
import pygame
from os import getcwd

SPRITE_SIZE = (48,48)


class Player(pygame.sprite.Sprite):


    def __init__(self, pos: tuple) -> None:
        super().__init__()
        
        global SPRITE_SIZE

        self.img = pygame.image.load(f"{getcwd()}/game_data/sprites/player/player.png")
        self.img = pygame.transform.scale(self.img, SPRITE_SIZE)

        self.img_angle = 0

        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = pos

        self.velocity = pygame.Vector2()
        self.speed = 10

    def move_and_collide(self):
        self.rect.topleft += self.velocity
        self.velocity = pygame.math.Vector2(0,0)
        
    def get_input(self, keys):

        if keys[pygame.K_UP]:
            self.velocity.y = self.speed * -1
        elif keys[pygame.K_DOWN]:
            self.velocity.y = self.speed * 1
        elif keys[pygame.K_LEFT]:
            self.velocity.x = self.speed * -1
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed * 1

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.rect)
