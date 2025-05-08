import pygame, os


class Interactable(pygame.sprite.Sprite):
    def __init__(
        self, texture_name: str, position: tuple, contents: list, _id: int
    ) -> None:
        super().__init__()
        self.sprite_list = {}
        for texture in os.listdir(f"{os.getcwd()}/game_data/sprites/map/"):
            if texture_name in texture:
                img = pygame.image.load(
                    f"{os.getcwd()}/game_data/sprites/map/{texture}"
                )
                texture = texture.split(".")[0]
                self.sprite_list[texture.split("_")[1]] = pygame.transform.scale(
                    img, (48, 48)
                )
        self.rect = self.sprite_list["0"].get_rect()
        self.rect.x, self.rect.y = position
        self.img = self.sprite_list["0"]
        self.animation_speed = 400

        self.is_animating = False

        self.id = _id

        self.name = texture_name
        self.contents = contents

    def draw_to_screen(self, screen: pygame.Surface):
        screen.blit(self.img, (self.rect.x, self.rect.y))


class Chest(Interactable):
    def __init__(
        self,
        controller,
        texture_name: str,
        position: tuple,
        contents: list,
        trap: bool = False,
        _id: int = None,
    ) -> None:
        super().__init__(texture_name, position, contents, _id)
        self.opened = False
        self.trap = trap

        if self.id in controller.opened_chests:
            self.is_animating = False
            self.img = self.sprite_list[str(len(self.sprite_list) - 2)]
            return

    def start_animation(self, controller):

        if not self.opened and not self.is_animating:

            self.animation_start_time: int = pygame.time.get_ticks()
            self.is_animating = True
            self.current_time = 0
            if self.id in controller.opened_chests:
                self.is_animating = False
                self.img = self.sprite_list[str(len(self.sprite_list) - 2)]
                return
            controller.opened_chests.append(self.id)

    def update(self):
        if self.is_animating:
            elapsed = pygame.time.get_ticks() - self.animation_start_time
            if elapsed > self.animation_speed:
                self.is_animating = False
                if self.trap:
                    self.img = self.sprite_list[str(len(self.sprite_list) - 1)]
                else:
                    self.img = self.sprite_list[str(len(self.sprite_list) - 2)]

            else:
                # this gets the current progress of animation, in time and ranging from 0 to 1
                frame_progress = elapsed / self.animation_speed

                # converts the frame progess percentage into a number that is the index of the frame that should be shown
                if self.trap:
                    # sets the frame to the correct index, from 0 to max number o frames and uses min to not go over index
                    frame_index = min(
                        int(frame_progress * len(self.sprite_list)),
                        len(self.sprite_list) - 1
                    )
                else:
                    frame_index = min(
                        int(frame_progress * (len(self.sprite_list) - 1)),
                        len(self.sprite_list) - 2
                    )

                # set img to the index
                self.img = self.sprite_list[str(frame_index)]
