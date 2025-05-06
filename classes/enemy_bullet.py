import pygame
from config import ENEMY_BULLET_IMG

class EnemyBullet:
    def __init__(self, x, y):
        self.image = pygame.image.load(ENEMY_BULLET_IMG)
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.x = x + 15
        self.y = y
        self.speed = 6
        self.state = "fire"

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.y > 600

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))