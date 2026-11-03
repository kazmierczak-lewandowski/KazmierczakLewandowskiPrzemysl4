import pygame
import time
import ctypes
from lab3.sensor import sensor_init, read_sensor

vl, dev = sensor_init()
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VL6180X Distance Visualization")
font = pygame.font.SysFont("Arial", 36)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    try:
        time.sleep(0.5)
        distance = read_sensor(vl, dev)[0]
    except Exception:
        distance = 255
    radius = max(10, 250 - distance)
    color = (255 - distance, 100, distance)

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, color, (WIDTH//2, HEIGHT//2), radius)
    text = font.render(f"{distance} mm", True, (255, 255, 255))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 50))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()