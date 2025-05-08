import pygame


class Controller:
    def __init__(self, s_id: tuple = (2, 0)) -> None:
        self.room: Room = Room(s_id)
        self.last_room = Room((-1, -1))
        self.debug = False

        self.status_text = None
        self.status_text_start_time = 0
        self.status_text_time = 1500

        self.habilities = {"shooting": False, "sword": False}

        self.projectile_list = pygame.sprite.Group()
        self.obstacle_list = pygame.sprite.Group()
        self.scene_interactables = pygame.sprite.Group()
        self.opened_chests = []

    def set_habilities(self, name, value):
        self.habilities[name] = value
    
class Room:
    def __init__(self, coords: tuple):
        self.x, self.y = coords

    def coords(self) -> tuple:
        return (self.x, self.y)
