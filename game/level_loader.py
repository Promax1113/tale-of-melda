import json
from os import getcwd
import pygame
from .block import Block

class LevelLoader:
    def __init__(self, path: str = "maps") -> None:
        super().__init__()
        self.path = path
    def load(self, level_id):
        with open(f"{getcwd()}/{self.path}/{level_id}.json") as f:
            level_data = json.load(f)
        return level_data
    def place_objects(self, data: dict):

        obstacles = pygame.sprite.Group()

        for obstacle in data["obstacles"]:
            obstacles.add(Block(obstacle["type"],(obstacle["x"]*48, obstacle["y"]*48)))
        
        return obstacles
