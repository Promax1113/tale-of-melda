
import os
import pygame
from .game_controller import Controller



class Bullet(pygame.sprite.Sprite):
    def __init__(self, author):
        super().__init__()

        self.author = author

        # box.png is a placeholder
        self.img = pygame.image.load(f"{os.getcwd()}/game_data/sprites/player/projectile.png")
        self.img = pygame.transform.scale(self.img, (32, 32))
        self.rect = self.img.get_rect()
        self.rect.center = self.author.rect.center
        self.direction = self.author.direction
        if self.direction == 1:
            self.rect.y -= 24
        elif self.direction == 2:
            self.rect.x -= 24
        elif self.direction == 3:
            self.rect.y += 24
        elif self.direction == 4:
            self.rect.x += 24


        self.speed = self.author.speed + 10

    def draw_and_move(self, game_controller: Controller, screen: pygame.Surface):
        if self.direction == 1:
            self.rect.y -= self.speed
        elif self.direction == 2:
            self.rect.x -= self.speed
        elif self.direction == 3:
            self.rect.y += self.speed
        elif self.direction == 4:
            self.rect.x += self.speed

        # add width and height of image so it doesnt kill itself before the projectile is off the screen.
        if (self.rect.x < 0 or self.rect.x > screen.get_width() + self.img.get_width() or
            self.rect.y < 0 or self.rect.y > screen.get_height() + self.img.get_height()):
            self.kill()  # remove from any sprite group
        if pygame.sprite.spritecollideany(self, game_controller.obstacle_list):
            self.kill()


        screen.blit(self.img, (self.rect.x, self.rect.y))
