import pygame
import random
from config import ASTEROID_IMG, WIDTH

class Asteroid:
    
    _fall_sound_file = None
    _sound_loaded = False
    
    @classmethod
    def set_fall_sound(cls, sound_path):
        cls._fall_sound_file = sound_path
        cls._sound_loaded = False
    
    def __init__(self):
        self.image = pygame.image.load(ASTEROID_IMG)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.x = random.randint(0, WIDTH - 32)
        self.y = -32
        self.speed_y = random.randint(3, 7)
        
        self.hit_points = 3  # Contador de vidas
                
        # Manejo seguro del sonido
        if not Asteroid._sound_loaded and Asteroid._fall_sound_file:
            try:
                Asteroid._fall_sound = pygame.mixer.Sound(Asteroid._fall_sound_file)
                Asteroid._fall_sound.set_volume(0.2)
                Asteroid._sound_loaded = True
            except pygame.error as e:
                print("No cargó sonido del asteroide:", e)
                Asteroid._fall_sound = None
                Asteroid._sound_loaded = False

        self.fall_channel = None
        if Asteroid._sound_loaded and Asteroid._fall_sound:
            self.fall_channel = Asteroid._fall_sound.play(-1)
            
    def take_hit(self):
            self.hit_points -= 1
            return self.hit_points <= 0

    def move(self):
        self.y += self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
    def off_screen(self):
        return self.y > 600
        
    def stop_sound(self):
        if self.fall_channel:
            self.fall_channel.stop()

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))