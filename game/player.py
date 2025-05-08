import math
import pygame
from os import getcwd

from .interactable import Interactable, Chest
from game.bullet import Bullet
from .game_controller import Controller

# In direction code:
# Every number represents a side of the current screen,
# up is 1, left is 2, and so on.

SPRITE_SIZE = (48,48)


class Player(pygame.sprite.Sprite):


    def __init__(self, pos: tuple, id: int) -> None:
        super().__init__()

        global SPRITE_SIZE


        self.img = pygame.image.load(f"{getcwd()}/game_data/sprites/player/player{id}.png")
        self.img = pygame.transform.scale(self.img, SPRITE_SIZE)

        self.img_angle = 0

        self.rect = self.img.get_rect()

        self.interact_rect = pygame.rect.Rect(pos[0] + 24, pos[1] + 24, 96, 96)

        self.rect.x, self.rect.y = pos


        self.velocity = pygame.Vector2()
        self.speed = 10
        self.direction = 3

        self.last_bullet_time = 0
        self.bullet_cooldown = 300

        self.interact_timeout = 200
        self.last_interact_time = 0

    def check_collisions(self, sprite_group: pygame.sprite.Group):
        # add horizontal movement first
        self.rect.x += self.velocity.x
        collision = pygame.sprite.spritecollideany(self, sprite_group)
        if collision:
            if self.velocity.x > 0:
                self.rect.right = collision.rect.left
            elif self.velocity.x < 0:
                self.rect.left = collision.rect.right
            self.velocity.x = 0

        # add vertical movement separately
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
        self.interact_rect.x = self.rect.x - 24
        self.interact_rect.y = self.rect.y - 24

        if self.rect.x < 0:
            self.rect.x = screen.get_width() - SPRITE_SIZE[0]
            controller.room.x -= 1
            # if controller.screen_id[-1] == "4":
            #     controller.screen_id = self.last_room_id
            #     #removes the last value in last id so it now can return back.
            #     self.last_room_id = self.last_room_id[:-1]
            # else:
            #     self.last_room_id = controller.screen_id
            #     controller.screen_id += "2"

        elif self.rect.x > screen.get_width() - SPRITE_SIZE[0]:
            self.rect.x = 0
            controller.room.x += 1
            # if controller.screen_id[-1] == "2":
            #     controller.screen_id = self.last_room_id
            #     self.last_room_id = self.last_room_id[:-1]

            # else:
            #     self.last_room_id = controller.screen_id
            #     controller.screen_id += "4"

        elif self.rect.y < 0:
            self.rect.y = screen.get_height() - SPRITE_SIZE[1]
            controller.room.y += 1
            # if controller.screen_id[-1] == "3":
            #     controller.screen_id = self.last_room_id
            #     self.last_room_id = self.last_room_id[:-1]

            # else:
            #     self.last_room_id = controller.screen_id
            #     controller.screen_id += "1"
        elif self.rect.y > screen.get_height() - SPRITE_SIZE[1]:
            self.rect.y = 0
            controller.room.y -= 1
            # if controller.screen_id[-1] == "1":
            #     controller.screen_id = self.last_room_id
            #     self.last_room_id = self.last_room_id[:-1]

            # else:
            #     self.last_room_id = controller.screen_id
            #     controller.screen_id += "3"



        self.velocity = pygame.math.Vector2(0,0)
    def spawn_bullet(self, controller: Controller, screen: pygame.Surface):
        bl = Bullet(self)
        controller.projectile_list.add(bl)

    def interact(self, controller: Controller):
        for obj in controller.scene_interactables:
            if self.interact_rect.colliderect(obj.rect):
                if isinstance(obj, Chest):
                    obj.start_animation(controller)
                    if obj.contents[0] == "shooting":
                        controller.set_habilities(obj.contents[0], True)
                        controller.status_text_start_time = pygame.time.get_ticks()
                        controller.status_text = f"{obj.contents[0]} unlocked, try pessing Z!"



    def get_input(self, keys, controller, screen):
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_UP]:
            self.velocity.y = self.speed * -1
            self.direction = 1
        elif keys[pygame.K_DOWN]:
            self.velocity.y = self.speed * 1
            self.direction = 3
        elif keys[pygame.K_LEFT]:
            self.velocity.x = self.speed * -1
            self.direction = 2
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed * 1
            self.direction = 4

        # This checks for if the subtraction of current time (epoch) and the last bullet time (also epoch)
        # is less than the time established as cooldown.
        if controller.habilities["shooting"]:
            if keys[pygame.K_z] and current_time - self.last_bullet_time > self.bullet_cooldown:
                self.spawn_bullet(controller, screen)
                self.last_bullet_time =  current_time
        if keys[pygame.K_x]:
            self.interact(controller)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.rect)
