import math
import pygame
from os import getcwd
from .game_controller import Controller


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

        self.last_room_id = "0"

        self.velocity = pygame.Vector2()
        self.speed = 10

    def check_collisions(self, sprite_group: pygame.sprite.Group):
        # Handle horizontal movement first
        self.rect.x += self.velocity.x
        collision = pygame.sprite.spritecollideany(self, sprite_group)
        if collision:
            if self.velocity.x > 0:
                self.rect.right = collision.rect.left
            elif self.velocity.x < 0:
                self.rect.left = collision.rect.right
            self.velocity.x = 0

        # Handle vertical movement separately
        self.rect.y += self.velocity.y
        collision = pygame.sprite.spritecollideany(self, sprite_group)
        if collision:
            if self.velocity.y > 0:
                self.rect.bottom = collision.rect.top
            elif self.velocity.y < 0:
                self.rect.top = collision.rect.bottom
            self.velocity.y = 0


    def move_and_collide(self, screen: pygame.Surface, controller: Controller, collision_group: pygame.sprite.Group):

        self.check_collisions(collision_group)
        self.rect.topleft += self.velocity
        if self.rect.x < 0:
            self.rect.x = screen.get_width() - SPRITE_SIZE[0]
            if controller.screen_id[-1] == "4":
                controller.screen_id = self.last_room_id
                #removes the last value in last id so it now can return back.
                self.last_room_id = self.last_room_id[:-1]
            else:
                self.last_room_id = controller.screen_id
                controller.screen_id += "2"

        elif self.rect.x > screen.get_width() - SPRITE_SIZE[0]:
            self.rect.x = 0
            if controller.screen_id[-1] == "2":
                controller.screen_id = self.last_room_id
                self.last_room_id = self.last_room_id[:-1]

            else:
                self.last_room_id = controller.screen_id
                controller.screen_id += "4"

        elif self.rect.y < 0:
            self.rect.y = screen.get_height() - SPRITE_SIZE[1]
            if controller.screen_id[-1] == "3":
                controller.screen_id = self.last_room_id
                self.last_room_id = self.last_room_id[:-1]

            else:
                self.last_room_id = controller.screen_id
                controller.screen_id += "1"
        elif self.rect.y > screen.get_height() - SPRITE_SIZE[1]:
            self.rect.y = 0
            if controller.screen_id[-1] == "1":
                controller.screen_id = self.last_room_id
                self.last_room_id = self.last_room_id[:-1]

            else:
                self.last_room_id = controller.screen_id
                controller.screen_id += "3"



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
