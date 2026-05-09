import pygame
import random

# Initialize Pygame
pygame.init()

# Screen setup
screen_size = [600, 600]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Tim shooter 3.000")

# Colors
green = (0, 255, 0)

# Game variables
score = 0
user_x = 160
user_y = 500
lives = 5

# Number of enemies
num_enemies = 10

# Enemy positions and speeds
def random_x():
    return random.randint(0, screen_size[0] - 60)

def random_y():
    return random.randint(-300, -50)

def random_speed():
    return random.randint(1, 9)

enemy_positions = []
for _ in range(num_enemies):
    enemy_positions.append({
        'x': random_x(),
        'y': random_y(),
        'speed': random_speed()
    })

# Bullets
bullets = []
bullet_speed = 10

# explosion list
explosions = []

# Load images
def load(name):
    return pygame.image.load(name)

background = pygame.transform.scale(load('m101BW.jpg'), screen_size)
kill = pygame.transform.scale(load('Untitled_design-removebg-preview.png'), (90, 100))
user = pygame.transform.scale(load('spaceSchip.png'), (60,70))

# Draw bullet
def draw_bullet(x, y):
    pygame.draw.rect(screen, (255, 255, 255), (x + 20, y, 5, 10))

# Display score
pygame.font.init()
def display_score(score):
    font = pygame.font.SysFont('DarkmodeRegular-X35Oo.ttf', 30)
    text = font.render('Score: ' + str(score), True, green)
    screen.blit(text, [20, 10])

# Move enemies
def move_enemy(enemy):
    if enemy['y'] > 600:
        enemy['x'] = random_x()
        enemy['y'] = random_y()
        enemy['speed'] = random_speed()
        return 75
    else:
        enemy['y'] += enemy['speed']
        return 0

# Game over screen
def game_over_screen(score):
    screen.fill((0, 0, 0))
    font_big = pygame.font.SysFont('impact', 60)
    font_small = pygame.font.SysFont('impact', 25)

    shake_x = random.randint(-3, 3)
    shake_y = random.randint(-3, 3)

    text1 = font_big.render("YOU DIED", True, (180, 0, 0))
    text2 = font_small.render(f"Final Score: {score}", True, (150, 0, 0))

    screen.blit(text1, [70 + shake_x, 250 + shake_y])
    screen.blit(text2, [90, 320])

    pygame.display.update()

# Game loop
clock = pygame.time.Clock()
keep_alive = True
game_over = False

while keep_alive:

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_alive = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append({'x': user_x, 'y': user_y})

    if not game_over:

        # Player movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and user_x < screen_size[0] - 60:
            user_x += 10
        if keys[pygame.K_LEFT] and user_x > 0:
            user_x -= 10
        if keys[pygame.K_UP] and user_y > 0:
            user_y -= 10
        if keys[pygame.K_DOWN] and user_y < screen_size[1] - 60:
            user_y += 10

        # Move enemies
        for enemy in enemy_positions:
            score += move_enemy(enemy)

        # Draw background
        screen.blit(background, [0, 0])

        # Draw enemies
        for enemy in enemy_positions:
            screen.blit(kill, [enemy['x'], enemy['y']])

        # Draw player
        screen.blit(user, [user_x, user_y])

        # Move bullets
        for bullet in bullets[:]:
            draw_bullet(bullet['x'], bullet['y'])
            bullet['y'] -= bullet_speed
            if bullet['y'] < 0:
                bullets.remove(bullet)

        # Draw explosions
        for explosion in explosions[:]:
            pygame.draw.circle(screen, (255, 200, 0), (explosion['x'] + 30, explosion['y'] + 30), explosion['size'])
            pygame.draw.circle(screen, (255, 100, 0), (explosion['x'] + 30, explosion['y'] + 30), explosion['size'] - 5)

            explosion['size'] += 2

            if explosion['size'] > 30:
                explosions.remove(explosion)

        # Collision detection
        player_rect = pygame.Rect(user_x, user_y, 60, 60)

        for enemy in enemy_positions:
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], 60, 60)

            for bullet in bullets[:]:
                bullet_rect = pygame.Rect(bullet['x'] + 20, bullet['y'], 5, 10)
                if bullet_rect.colliderect(enemy_rect):

                    # CREATE EXPLOSION
                    explosions.append({'x': enemy['x'], 'y': enemy['y'], 'size': 10})

                    enemy['x'] = random_x()
                    enemy['y'] = random_y()
                    enemy['speed'] = random_speed()
                    score += 50
                    bullets.remove(bullet)

            if player_rect.colliderect(enemy_rect):
                lives -= 1
                enemy['x'] = random_x()
                enemy['y'] = random_y()
                enemy['speed'] = random_speed()

        # Display lives
        def display_lives(lives):
            font = pygame.font.SysFont('DarkmodeRegular-X35Oo.ttf', 30)
            text = font.render('Lives: ' + str(lives), True, (255, 0, 0))
            screen.blit(text, [250, 10])

        display_score(score)
        display_lives(lives)

        # Game over check
        if lives <= 0:
            game_over = True

    else:
        game_over_screen(score)

    pygame.display.update()
    clock.tick(60)

pygame.quit()