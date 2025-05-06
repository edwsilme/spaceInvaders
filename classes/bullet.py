import pygame
from config import BULLET_IMG

class Bullet:
    def __init__(self):
        self.image = pygame.image.load(BULLET_IMG)
        self.image = pygame.transform.scale(self.image, (12, 12))
        self.x = 0
        self.y = 480
        self.speed_y = 10
        self.state = "ready"
        
    def fire(self, player_x):
        if self.state == "ready":
            self.x = player_x + 18
            self.y = 480
            self.state = "fire"

    def move(self):
        if self.state == "fire":
            self.y -= self.speed_y
            if self.y <= 0:
                self.state = "ready"
                self.y = 480

    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, (self.x, self.y))
            
    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))