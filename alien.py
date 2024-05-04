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

gun_image = pygame.image.load("img/gun.png")
gun_width = 250
gun_height = 140

background_image = pygame.image.load("img/fon.png")

# Создание шрифта
font = pygame.font.Font("font/calibri.ttf", 30)

# Переменная для подсчета выстрелов
shot_count = 0

# Класс для спрайта мишени
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("img/target.png").convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.center_in_place()  # Размещаем мишень в центре при старте игры

    def center_in_place(self):
        # Размещение мишени в центре экрана
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.rect.center = (center_x, center_y)
        self.update_scale()

    def reset(self):
        # Рандомная позиция мишени после попадания
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.update_scale()

    def update_scale(self):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        distance = math.sqrt((self.rect.centerx - center_x) ** 2 + (self.rect.centery - center_y) ** 2)
        max_distance = math.sqrt(center_x**2 + center_y**2)
        scale_factor = 1.85 - 1.15 * (distance / max_distance)  # Scaling from 50% to 175%

        new_width = int(self.original_image.get_width() * scale_factor)
        new_height = int(self.original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))

# Создание экземпляра мишени
target = Target()

# Функция для создания радиального градиента
def create_radial_gradient(surface, center_color, outer_color):
    center_x, center_y = surface.get_size()[0] // 2, surface.get_size()[1] // 2
    max_distance = math.sqrt(center_x**2 + center_y**2)
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            distance = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
            ratio = distance / max_distance
            r = int(outer_color[0] * ratio + center_color[0] * (1 - ratio))
            g = int(outer_color[1] * ratio + center_color[1] * (1 - ratio))
            b = int(outer_color[2] * ratio + center_color[2] * (1 - ratio))
            surface.set_at((x, y), (r, g, b))

# Создаем градиентный фон
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
create_radial_gradient(background, (255, 255, 255), (0, 0, 0))

# Игровой цикл
running = True
while running:
    screen.blit(background, (0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    gun_x = max(0, min(mouse_x - gun_width // 2 + 46, SCREEN_WIDTH - gun_width))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if target.rect.collidepoint(mouse_x, mouse_y):
                target.reset()
                shot_count += 1

    screen.blit(background_image, (0, 0))
    screen.blit(target.image, target.rect)
    screen.blit(gun_image, (gun_x, SCREEN_HEIGHT - gun_height))

    text = font.render(f'Выстрелы: {shot_count}', True, (255, 255, 255))
    screen.blit(text, (10, SCREEN_HEIGHT - 50))

    pygame.display.update()

pygame.quit()
