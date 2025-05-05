import pygame
import game

pygame.init()

running = True

# game setup

screen = pygame.display.set_mode((800, 600))
controller = game.Controller()

ll = game.LevelLoader("game_data/maps")

pl = game.Player((6*64, 5*64))

pl.speed = 5

font = pygame.font.Font("game_data/fonts/Pixeled.ttf", 24)


clock = pygame.time.Clock()


while running:
    screen.fill((12,12,12))
    id_text = font.render(f"Room: ({controller.room.x}, {controller.room.y})", False, (24,24,24,))
    if controller.last_room.coords() != controller.room.coords():
        controller.last_room.x, controller.last_room.y = controller.room.coords()

        map = ll.load(controller.room)

        bg = ll.load_background(controller.room)
        objs = ll.place_objects(map)
        controller.obstacle_list = objs


    screen.blit(bg, (0,0))

    for obj in objs:
        if controller.debug:
            pygame.draw.rect(screen, (255,255,255), obj.rect)
        obj.draw_to_screen(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_q:
                controller.debug = not controller.debug

    keys = pygame.key.get_pressed()

    pl.get_input(keys, controller, screen)
    pl.move_and_collide(screen, controller, objs)
    pl.draw(screen)
    for projectile in controller.projectile_list:
        projectile.draw_and_move(controller, screen)
    if controller.debug:
        pygame.draw.rect(screen, (255,0,0), pl.rect)
        screen.blit(id_text, (20, 500))


    pygame.display.flip()
    clock.tick(60)
