import json
from os import getcwd
import pygame
from .block import Block
from .interactable import Chest, Interactable


class LevelLoader:
    def __init__(self, path: str = "maps") -> None:
        super().__init__()
        self.path = path

    def load(self, level_id) -> dict:
        # print(f"{getcwd()}/{self.path}/{level_id.x}_{level_id.y}.json")
        with open(f"{getcwd()}/{self.path}/{level_id.x}_{level_id.y}.json") as f:
            level_data = json.load(f)
            return level_data

    def place_interactables(self, data: dict, controller):
        objects = pygame.sprite.Group()
        for object in data:
            if object["type"] == "chest":
                objects.add(
                    Chest(
                        controller,
                        object["type"],
                        (object["x"] * 48, object["y"] * 48),
                        object["contents"],
                        object["trap"],
                        object["id"],
                    )
                )
            else:
                objects.add(
                    Interactable(
                        object["type"],
                        (object["x"] * 48, object["y"] * 48),
                        object["contents"],
                        object["id"],
                    )
                )

        return objects

    def place_obstacles(self, data: dict):

        obstacles = pygame.sprite.Group()

        for obstacle in data:
            if obstacle["width"] > 1 or obstacle["height"] > 1:
                for i in range(1, obstacle["width"] + 1):
                    for j in range(0, obstacle["height"]):
                        obstacles.add(
                            Block(
                                obstacle["type"],
                                (
                                    i * 48 + obstacle["x"] * 48,
                                    j * 48 + obstacle["y"] * 48,
                                ),
                            )
                        )
            else:
                obstacles.add(
                    Block(obstacle["type"], (obstacle["x"] * 48, obstacle["y"] * 48))
                )

        return obstacles

    @staticmethod
    def load_background(level_id):
        return pygame.image.load(
            f"{getcwd()}/game_data/sprites/backgrounds/{level_id.x}_{level_id.y}.png"
        )
