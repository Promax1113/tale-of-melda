import pygame
import game
from game.level_loader import LevelLoader

running = True

# game setup
screen_config = game.Screen()
screen = pygame.display.set_mode((screen_config.width, screen_config.height))
ll = LevelLoader("game_data/maps")

pl = game.Player((2*64, 2*64))


clock = pygame.time.Clock()
last_id = -1

while running:
    screen.fill((12,12,12))

    if last_id != screen_config.id:
        map = ll.load(screen_config.id)
        last_id = screen_config.id
        objs = ll.place_objects(map)
    for obj in objs:
        obj.draw_to_screen(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()


    pl.get_input(keys)
    pl.move_and_collide()
    pl.draw(screen)

    pygame.display.flip()
    clock.tick(60)
