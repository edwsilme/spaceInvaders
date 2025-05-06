import math

def is_collision(obj1, obj2):
    return obj1.get_rect().colliderect(obj2.get_rect())