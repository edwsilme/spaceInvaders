import pygame
from config import WIDTH, HEIGHT, LASER_SOUND, METAL_HIT_SOUND, EXPLOSION_SOUND, MOTOR_SOUND, ASTEROID_SOUND
from config import ENEMY_IMG, ENEMYA_IMG, ENEMYB_IMG
from classes.player import Player
from classes.enemy import Enemy
from classes.bullet import Bullet
from classes.utils import is_collision
from classes.asteroid import Asteroid
from classes.explosion import Explosion
from classes.enemy_bullet import EnemyBullet
import random

# Constantes de asteroides
ASTEROID_SPAWN_RATE = 90

# Listas y temporizadores
enemy_bullets = []
asteroids = []
asteroid_timer = 0
explosions = []

# Nivel y dificultad
level = 1
MAX_LEVEL = 12
base_enemy_speed = 1
enemy_speed_increment = 0.15
asteroids_enabled = False
win = False

# Diccionario de configuracion por nivel
level_features = {
    1: {"asteroids": False, "enemy_shoot": False},
    2: {"asteroids": False, "enemy_shoot": False},
    3: {"asteroids": True,  "enemy_shoot": False},
    4: {"asteroids": False,  "enemy_shoot": True},
    5: {"asteroids": True,  "enemy_shoot": False},
    6: {"asteroids": True,  "enemy_shoot": True},
    7: {"asteroids": False, "enemy_shoot": True},
    8: {"asteroids": True,  "enemy_shoot": True},
}

# Diccionario para los puntajes
ENEMY_SCORES = {
    ENEMY_IMG: 10,
    ENEMYA_IMG: 20,
    ENEMYB_IMG: 30
}
ASTEROID_SCORE = 15

# Función para mostrar pantalla de Game Over
def show_game_over(screen):
    font = pygame.font.SysFont(None, 64)
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - 160, HEIGHT // 2 - 60))

    subfont = pygame.font.SysFont(None, 32)
    restart_text = subfont.render("Presiona R para reiniciar o ESC para salir", True, (255, 255, 255))
    screen.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2 + 10))

    pygame.display.update()
    
# Función para mostrar pantalla de victoria
def show_win_screen(screen):
    font = pygame.font.SysFont(None, 64)
    text = font.render("¡HAS GANADO!", True, (0, 255, 0))
    screen.blit(text, (WIDTH // 2 - 180, HEIGHT // 2 - 60))

    subfont = pygame.font.SysFont(None, 32)
    restart_text = subfont.render("Presiona R para reiniciar o ESC para salir", True, (255, 255, 255))
    screen.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2 + 10))

    pygame.display.update()
    
# Función para reiniciar el juego
def reset_game(speed=4):
    return Player(), [Enemy() for _ in range(6)], Bullet()

# Inicialización
pygame.init()
pygame.mixer.init()

# Cargar sonidos
laser_sound = pygame.mixer.Sound(LASER_SOUND)
laser_sound.set_volume(0.1)
metal_hit_sound = pygame.mixer.Sound(METAL_HIT_SOUND)
metal_hit_sound.set_volume(0.4)
explosion_sound = pygame.mixer.Sound(EXPLOSION_SOUND)
explosion_sound.set_volume(0.1)
motor_sound = pygame.mixer.Sound(MOTOR_SOUND)
motor_sound.set_volume(0.2)

# Asignar sonidos precargados al asteroide
Asteroid.set_fall_sound(ASTEROID_SOUND)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Estado inicial del juego
player, enemies, bullet = reset_game(base_enemy_speed)
game_over = False
motor_playing = False
score = 0

# Diferentes Enemigos
def create_enemies_for_level(level, base_speed):
    level_sprites = {
        1: [ENEMY_IMG],
        2: [ENEMYA_IMG],
        3: [ENEMYB_IMG],
        4: [ENEMY_IMG],
        5: [ENEMYA_IMG],
        6: [ENEMY_IMG, ENEMYA_IMG],
        7: [ENEMYB_IMG],
        8: [ENEMYA_IMG, ENEMYB_IMG, ENEMY_IMG],
        9: [ENEMYB_IMG],
        10: [ENEMY_IMG],
        11: [ENEMYA_IMG],
        12: [ENEMYB_IMG]
    }
    
    # fallback por si se pasa el nivel máximo
    sprites = level_sprites.get(level, [ENEMY_IMG])
    enemies = []

    for i in range(10):
        speed_multiplier = 1 + ((level - 1) * enemy_speed_increment)
        sprite = random.choice(sprites)
        
        # Activa el zigzag a partir del nivel 4
        zigzag = level >= 4
        
        enemies.append(Enemy(
            speed_x = base_speed * speed_multiplier,
            image_path = sprite,
            zigzag = zigzag
        ))

    return enemies

# Cargar configuración inicial del nivel
features = level_features.get(level, {"asteroids": True, "enemy_shoot": True})

running = True
while running:
    screen.fill((0, 0, 0))  # fondo negro

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if game_over:
            # teclas R o ESC en modo Game Over
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    level = 1
                    #asteroids_enabled = False
                    features = level_features.get(level, {"asteroids": True, "enemy_shoot": True})
                    win = False
                    #player, enemies, bullet = reset_game(base_enemy_speed)
                    score = 0
                    player, enemies, bullet = reset_game()
                    for asteroid in asteroids:
                        asteroid.stop_sound()
                    asteroids.clear()
                    game_over = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
            continue

        # Movimiento jugador
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -player.speed
            if event.key == pygame.K_RIGHT:
                player.x_change = player.speed
            if event.key == pygame.K_SPACE:
                if bullet.state == "ready":
                    bullet.fire(player.x)
                    laser_sound.play()

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.x_change = 0

    if not game_over:
        
        player.move()
        bullet.move()
        
        if player.x_change != 0 and not motor_playing:
            motor_sound.play(-1)
            motor_playing = True
        elif player.x_change == 0 and motor_playing:
            motor_sound.stop()
            motor_playing = False

        for enemy in enemies:
            enemy.move()
            
            # Disparan solo desde nivel 3
            if features["enemy_shoot"]:
                if abs(enemy.x - player.x) < 40 and random.randint(0, 100) < 2:
                    enemy_bullets.append(EnemyBullet(enemy.x, enemy.y))
            
            # colisiona con el jugador
            if is_collision(enemy, player) or enemy.y > 440:
                explosion_sound.play()
                explosions.append(Explosion(player.x, player.y))
                game_over = True
                break
            
            # Colisión con la bala
            if is_collision(enemy, bullet) and bullet.state == "fire":
                bullet.state = "ready"
                bullet.y = 500
                #enemy.reset_position()
                explosion_sound.play()
                explosions.append(Explosion(enemy.x, enemy.y))
                enemies.remove(enemy)                
                score += ENEMY_SCORES.get(enemy.image_path, 10) # Sumar puntos
                break
            
            enemy.draw(screen)

        bullet.draw(screen)
        player.draw(screen)
        
        # Balas de enemigos
        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.move()
            enemy_bullet.draw(screen)

            if enemy_bullet.off_screen():
                enemy_bullets.remove(enemy_bullet)
            elif is_collision(enemy_bullet, player):
                explosion_sound.play()
                explosions.append(Explosion(player.x, player.y))
                enemy_bullets.remove(enemy_bullet)
                game_over = True
            
        # Spawner de asteroides
        if features["asteroids"]:
            asteroid_timer += 1
            
            if asteroid_timer >= ASTEROID_SPAWN_RATE:
                asteroid_timer = 0
                asteroids.append(Asteroid())                

            # Movimiento y colisión de asteroides
            for asteroid in asteroids[:]:
                asteroid.move()
                asteroid.draw(screen)                
                               
                if is_collision(asteroid, bullet) and bullet.state == "fire":
                    bullet.state = "ready"
                    bullet.y = 500
                    metal_hit_sound.play()
                    #asteroid.stop_sound()
                    #asteroids.remove(asteroid)
                    
                    if asteroid.take_hit():
                        asteroid.stop_sound()
                        metal_hit_sound.stop()
                        explosion_sound.play()                    
                        explosions.append(Explosion(asteroid.x, asteroid.y))
                        asteroids.remove(asteroid)
                        score += ASTEROID_SCORE # Sumar puntos por destruir asteroide
                        
                elif is_collision(asteroid, player):
                    asteroid.stop_sound()
                    explosion_sound.play()
                    asteroids.remove(asteroid)
                    explosions.append(Explosion(player.x, player.y))
                    game_over = True
                    break
                
        for explosion in explosions[:]:
            if explosion.update():
                explosions.remove(explosion)
            else:
                explosion.draw(screen)
                
        if not enemies:
            if level < MAX_LEVEL:
                level += 1
                features = level_features.get(level, {"asteroids": True, "enemy_shoot": True})
                enemies = create_enemies_for_level(level, base_enemy_speed)
            else:
                win = True
                game_over = True
            
        # Mostrar nivel en pantalla
        font = pygame.font.SysFont(None, 36)
        level_text = font.render(f"Nivel: {level}", True, (255, 255, 255))
        screen.blit(level_text, (10, 10))
        
    if game_over:
        if win:
            show_win_screen(screen)
        else:
            show_game_over(screen)       
    
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()