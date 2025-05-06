import pygame
from config import PLAYER_IMG, WIDTH

class Player:
    def __init__(self):
        self.image = pygame.image.load(PLAYER_IMG)
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.x = 370
        self.y = 500
        self.speed = 5
        self.x_change = 0

    def move(self):
        self.x += self.x_change
        self.x = max(0, min(self.x, WIDTH - 48))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))