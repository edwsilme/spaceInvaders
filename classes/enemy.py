import pygame
import random
from config import ENEMY_IMG

class Enemy:
    def __init__(self, speed_x=2, image_path=None, zigzag=False):
        
        self.image_path = image_path if image_path else ENEMY_IMG
        
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 150)
        self.speed_x = speed_x
        self.original_speed = speed_x
        self.speed_y = 40    
        
        # Zigzag controlado
        self.zigzag = zigzag
        self.change_interval = random.randint(30, 60)
        self.direction_change_counter = 0

    def move(self):        
        self.x += self.speed_x
        
        # Rebote horizontal en los bordes
        if self.x <= 0 or self.x >= 760:
            self.speed_x *= -1
            self.y += self.speed_y
        
        if self.zigzag:
            self.direction_change_counter += 1
            if self.direction_change_counter >= self.change_interval:
                self.speed_x *= -1
                self.y += self.speed_y
                self.direction_change_counter = 0
                self.change_interval = random.randint(30, 60)
        
        self.x = max(0, min(760, self.x))

    def reset_position(self):
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 150)
        #self.speed_x = self.original_speed
        self.speed_x = abs(self.speed_x)
        self.direction_change_counter = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))