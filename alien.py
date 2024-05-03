import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A L I E N")
icon = pygame.image.load("img/tir.jpg")
pygame.display.set_icon(icon)

target_image = pygame.image.load("img/target.png")
target_width = 175
target_height = 200
target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(0, SCREEN_HEIGHT - target_height)

gun_image = pygame.image.load("img/gun.png")
gun_width = 250
gun_height = 140

# Создание шрифта
font = pygame.font.Font("font/calibri.ttf", 30)

# Переменная для подсчета выстрелов
shot_count = 0

# Функция для создания радиального градиента с более мягким затемнением
def create_radial_gradient(surface, center_color, outer_color, power=0.45):
    center_x, center_y = surface.get_size()[0] // 2, surface.get_size()[1] // 2
    max_distance = math.sqrt(center_x**2 + center_y**2)

    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            distance = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
            ratio = (distance / max_distance) ** power
            r = int((outer_color[0] * ratio + center_color[0] * (1 - ratio)))
            g = int((outer_color[1] * ratio + center_color[1] * (1 - ratio)))
            b = int((outer_color[2] * ratio + center_color[2] * (1 - ratio)))
            surface.set_at((x, y), (r, g, b))

# Создаем градиентный фон
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
create_radial_gradient(background, (255, 255, 255), (0, 0, 0))

running = True
while running:
    screen.blit(background, (0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    gun_x = max(0, min(mouse_x - gun_width // 2, SCREEN_WIDTH - gun_width))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(0, SCREEN_HEIGHT - target_height)
                shot_count += 1

    screen.blit(target_image, (target_x, target_y))
    screen.blit(gun_image, (gun_x, SCREEN_HEIGHT - gun_height))

    # Рендеринг текста для отображения количества выстрелов, после всех объектов
    text = font.render(f'Выстрелы: {shot_count}', True, (255, 255, 255))
    screen.blit(text, (10, SCREEN_HEIGHT - 50))

    pygame.display.update()

pygame.quit()
