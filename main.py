import pygame
import game

pygame.init()

running = True

# game setup

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tale of Melda")
controller = game.Controller()

ll = game.LevelLoader("game_data/maps")

pl = game.Player((6*64, 5*64), id=0)

pl.speed = 10

font = pygame.font.Font("game_data/fonts/Pixeled.ttf", 24)


clock = pygame.time.Clock()


while running:
    screen.fill((12,12,12))
    id_text = font.render(f"Room: ({controller.room.x}, {controller.room.y})", False, (24,24,24,))
    status_text = font.render(controller.status_text, True, (255, 255, 255), (0,0,0))
    if controller.last_room.coords() != controller.room.coords():
        controller.last_room.x, controller.last_room.y = controller.room.coords()

        bg_map = ll.load(controller.room)

        bg = ll.load_background(controller.room)
        interactables = ll.place_interactables(bg_map["interactables"], controller)
        controller.scene_interactables = interactables

        obstacles = ll.place_obstacles(bg_map["obstacles"])
        controller.obstacle_list = obstacles


    screen.blit(bg, (0,0))

    for obj in obstacles:
        if controller.debug:
            pygame.draw.rect(screen, (255,255,255), obj.rect)
        obj.draw_to_screen(screen)

    for obj in controller.scene_interactables:
        obj.draw_to_screen(screen)
        obj.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_q:
                controller.debug = not controller.debug

    keys = pygame.key.get_pressed()
    if not pygame.time.get_ticks() - controller.status_text_start_time > controller.status_text_time:
        screen.blit(status_text, (20, 20))

    pl.get_input(keys, controller, screen)
    pl.move_and_collide(screen, controller, obstacles)
    pl.draw(screen)
    for projectile in controller.projectile_list:
        projectile.draw_and_move(controller, screen)
    if controller.debug:
        pygame.draw.rect(screen, (0,0,255), pl.interact_rect)
        pygame.draw.rect(screen, (255,0,0), pl.rect)

        screen.blit(id_text, (20, 500))


    pygame.display.flip()
    clock.tick(60)
