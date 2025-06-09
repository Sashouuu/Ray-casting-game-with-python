import pygame as pg
import sys

def draw_text(surface, text, size, x, y, center=True):
    font = pg.font.SysFont("Arial", size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def main_menu():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Pycasting Maze - Menu")

    clock = pg.time.Clock()
    title_font = pg.font.SysFont("Arial", 64)
    button_font = pg.font.SysFont("Arial", 36)

    start_button = pg.Rect(300, 250, 200, 60)
    quit_button = pg.Rect(300, 350, 200, 60)

    while True:
        screen.fill((0, 0, 0))
        draw_text(screen, "Pycasting Maze", 64, 400, 100)

        # Buttons
        mouse_pos = pg.mouse.get_pos()
        for rect, text in [(start_button, "Start Game"), (quit_button, "Quit")]:
            color = (100, 100, 255) if rect.collidepoint(mouse_pos) else (80, 80, 80)
            pg.draw.rect(screen, color, rect)
            draw_text(screen, text, 36, rect.centerx, rect.centery)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    return True
                elif quit_button.collidepoint(mouse_pos):
                    pg.quit()
                    sys.exit()

        pg.display.flip()
        clock.tick(60)
