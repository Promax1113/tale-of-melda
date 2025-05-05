import pygame


class Controller:
    def __init__(self, s_id: tuple = (2,0)) -> None:
        self.room: Room = Room(s_id)
        self.last_room = Room((-1, -1))
        self.debug = False

        self.projectile_list = pygame.sprite.Group()
        self.obstacle_list = pygame.sprite.Group()

class Room:
    def __init__(self, coords: tuple):
        self.x , self.y = coords

    def coords(self) -> tuple:
        return (self.x, self.y)
