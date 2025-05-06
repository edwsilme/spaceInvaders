import pygame
from config import EXPLOSION_IMG, WIDTH, HEIGHT

class Explosion:
    def __init__(self, x, y):
        self.image = pygame.image.load(EXPLOSION_IMG)
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.x = x
        self.y = y
        self.duration = 25  # Duración para mostrar la explosión
        self.frame = 0
        
        self.x = max(0, min(self.x, WIDTH - self.image.get_width()))
        self.y = max(0, min(self.y, HEIGHT - self.image.get_height()))

    def update(self):
        self.frame += 1
        if self.frame > self.duration:
            return True  # Explosión termina después de 'duration'
        return False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  # Dibuja la explosión en la pantalla