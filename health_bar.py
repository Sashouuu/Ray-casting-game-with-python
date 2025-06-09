import pygame as pg

def draw_health_bar(screen, health):
    bar_width = 200
    bar_height = 20
    x,y = 10, 10
    fill = int(bar_width * (health /100))
    color = (255 - int(2.55 * health), int(2.55 * health), 0) # red to green
    pg.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
    pg.draw.rect(screen, color, (x, y, fill, bar_height))