from pygame import Surface



class Screen(Surface):
    def __init__(self, size: tuple = (800, 600), screen_id: str = "0") -> None:
        self.id: str = screen_id
        self.width, self.height = size
