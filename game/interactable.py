import pygame, os


class Interactable(pygame.sprite.Sprite):
    def __init__(self,texture_name: str, position: tuple, contents: list) -> None:
        super().__init__()
        self.sprite_list = []
        for texture in os.listdir(f"{os.getcwd()}/game_data/sprites/map/"):
            if texture_name in texture:
                img = pygame.image.load(f"{os.getcwd()}/game_data/sprites/map/{texture}")
                self.sprite_list.append(pygame.transform.scale(img,(48,48)))
        self.rect = self.sprite_list[0].get_rect()
        self.rect.x, self.rect.y = position
        self.img = self.sprite_list[0]
        self.animation_speed = 400


        self.name = texture_name
        self.contents = contents
    def draw_to_screen(self, screen: pygame.Surface):
        screen.blit(self.img, (self.rect.x, self.rect.y))


class Chest(Interactable):
    def __init__(self, texture_name: str, position: tuple, contents: list, trap: bool = False) -> None:
        super().__init__(texture_name, position, contents)
        self.opened = False
        self.trap = trap