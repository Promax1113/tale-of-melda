import pygame
import game

pygame.init()

running = True

# game setup

screen = pygame.display.set_mode((800, 600))
controller = game.Controller("0")

ll = game.LevelLoader("game_data/maps")

pl = game.Player((2*64, 2*64))

pl.speed = 5

font = pygame.font.Font("game_data/fonts/Pixeled.ttf", 24)


clock = pygame.time.Clock()
last_id = -1

while running:
    screen.fill((12,12,12))
    id_text = font.render(f"Room: {controller.screen_id}", False, (24,24,24,))

    if last_id != controller.screen_id:
        map = ll.load(controller.screen_id)
        last_id = controller.screen_id
        bg = ll.load_background(controller.screen_id)
        objs = ll.place_objects(map)
    screen.blit(bg, (0,0))

    for obj in objs:
        obj.draw_to_screen(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    pl.get_input(keys)
    pl.move_and_collide(screen, controller)
    pl.draw(screen)
    screen.blit(id_text, (20, 20))
    pygame.display.flip()
    clock.tick(60)
