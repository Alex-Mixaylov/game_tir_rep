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
        self.reset()

    def reset(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.update_scale()

    def update_scale(self):
        # Расчет расстояния до центра
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        distance = math.sqrt((self.rect.centerx - center_x) ** 2 + (self.rect.centery - center_y) ** 2)
        max_distance = math.sqrt(center_x ** 2 + center_y ** 2)

        # Расчет масштаба и яркости
        scale_factor = 1.45 - ((distance / max_distance) * (1.45 - 0.65))  # 0.65 минимальный масштаб, 1.45 максимальный
        brightness_factor = 0.85 + (
                    (distance / max_distance) * (1.15 - 0.85))  # 0.85 минимальная яркость, 1.15 максимальная

        # Применение масштаба
        new_width = int(self.original_image.get_width() * scale_factor)
        new_height = int(self.original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))

        # Применение яркости
        arr = pygame.surfarray.pixels3d(self.image)
        arr[:, :, :] = (arr * brightness_factor).clip(0, 255)
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))


# Создание экземпляра мишени
target = Target()

running = True
while running:
    screen.blit(background_image, (0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    gun_x = max(0, min(mouse_x - gun_width // 2 + 46, SCREEN_WIDTH - gun_width))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if target.rect.collidepoint(mouse_x, mouse_y):
                target.reset()
                shot_count += 1
            else:
                target.rect.center = (mouse_x, mouse_y)
                target.update_scale()

    screen.blit(target.image, target.rect)
    screen.blit(gun_image, (gun_x, SCREEN_HEIGHT - gun_height))

    text = font.render(f'Выстрелы: {shot_count}', True, (255, 255, 255))
    screen.blit(text, (10, SCREEN_HEIGHT - 50))

    pygame.display.update()

pygame.quit()
