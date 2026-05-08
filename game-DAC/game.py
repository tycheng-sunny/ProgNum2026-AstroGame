# main.py
import random
import io
import urllib.request
import pygame
from Entities.Playercode import player
from Entities.AsteroidCode import Asteroid

pygame.init()

class Game:
    def __init__(self):
        self.screen_width = 1080
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("AsteroidGame")
        self.clock = pygame.time.Clock()

        # --- Fondo de galaxias NASA ---
        galaxy_urls = [
            "https://science.nasa.gov/wp-content/uploads/2023/09/stsci-01g8jzq6gwxhex15pyy60wdrsk-2.png",   # Cartwheel Galaxy
            "https://science.nasa.gov/wp-content/uploads/2023/09/hubble-3.png",                              # Hubble Ultra Deep Field
            "https://science.nasa.gov/wp-content/uploads/2023/09/427020main-pia12832-c.jpg",                 # Andromeda (WISE)
            "https://science.nasa.gov/wp-content/uploads/2023/09/ssc2006-02a-0.jpg",                         # Milky Way Center
            "https://science.nasa.gov/wp-content/uploads/2023/09/m31-layered-uv-and-optical.jpg",            # Andromeda UV
        ]
        self.bg_images = []
        for url in galaxy_urls:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                data = urllib.request.urlopen(req, timeout=5).read()
                img = pygame.image.load(io.BytesIO(data)).convert()
                img = pygame.transform.scale(img, (self.screen_width, self.screen_height))
                self.bg_images.append(img)
            except Exception as e:
                print(f"No se pudo cargar imagen: {url} — {e}")

        self.bg_index = 0          # imagen de fondo actual
        self.bg_next = 1 % max(len(self.bg_images), 1)
        self.bg_alpha = 0          # 0=totalmente bg_index, 255=totalmente bg_next
        self.bg_fade_speed = 1     # velocidad de fade (por frame)
        self.bg_hold_frames = 300  # frames que se mantiene cada imagen (~5s a 60fps)
        self.bg_hold_counter = 0

        self.player = player(
            pos=[self.screen_width / 2, self.screen_height * 0.8],
            size=(50, 50),
            screen_width=self.screen_width,
            screen_height=self.screen_height
        )
        self.asteroids = []
        self.max_ambient_asteroids = 40
        for _ in range(self.max_ambient_asteroids):
            self.asteroids.append(Asteroid(self.screen_width, None))

        self.running = True
        self.player_health = 300
        self.belt_count = 0          # contador de belts recogidos

        self.beltsize = 60  # tamaño del belt en pantalla y collision box

        self.item_spawned = False
        self.item_collected = False
        self.item_spawn_time = 0
        self.item_pos = [0, 0]
        self.item_size = (self.beltsize, self.beltsize)
        self.start_time = pygame.time.get_ticks()
        self.ring_spawned = False

        
        self.belt_image = pygame.transform.scale((pygame.image.load("belt.png")), self.item_size
        )

    def spawn_item(self):
        if not self.item_spawned and (pygame.time.get_ticks() - self.start_time) > 10000:
            self.item_spawned = True
            self.item_pos = [
                random.randint(0, self.screen_width - self.item_size[0]),
                random.randint(0, self.screen_height - self.item_size[1])
            ]

    def spawn_asteroid_ring(self):
        if self.item_collected and not self.ring_spawned and \
                (pygame.time.get_ticks() - self.item_spawn_time) > 8000:

            ring_count = 36
            radius = 500
            target_pos = self.player.pos.copy()

            for i in range(ring_count):
                angle = i * (360 / ring_count)
                offset = pygame.math.Vector2(radius, 0).rotate(angle)
                spawn_pos = [target_pos[0] + offset.x, target_pos[1] + offset.y]

                asteroid = Asteroid(
                    screen_width=self.screen_width,
                    target_pos=target_pos,
                    spawn_pos=spawn_pos
                )
                self.asteroids.append(asteroid)

            self.ring_spawned = True

    def run(self):
        font = pygame.font.SysFont(None, 36)

        while self.running:
            # Fondo: fade entre galaxias
            if self.bg_images:
                self.bg_hold_counter += 1
                if self.bg_hold_counter >= self.bg_hold_frames:
                    self.bg_alpha = min(255, self.bg_alpha + self.bg_fade_speed)
                    if self.bg_alpha >= 255:
                        self.bg_index = self.bg_next
                        self.bg_next = (self.bg_next + 1) % len(self.bg_images)
                        self.bg_alpha = 0
                        self.bg_hold_counter = 0
                self.screen.blit(self.bg_images[self.bg_index], (0, 0))
                if self.bg_alpha > 0 and len(self.bg_images) > 1:
                    overlay = self.bg_images[self.bg_next].copy()
                    overlay.set_alpha(self.bg_alpha)
                    self.screen.blit(overlay, (0, 0))
                # Oscurecer el fondo para que los sprites se vean bien
                dark = pygame.Surface((self.screen_width, self.screen_height))
                dark.set_alpha(140)
                dark.fill((0, 0, 0))
                self.screen.blit(dark, (0, 0))
            else:
                self.screen.fill((0, 0, 0))
            self.player.movement(5)

            self.spawn_item()
            self.spawn_asteroid_ring()

            for asteroid in self.asteroids:
                asteroid.update(self.screen_width, self.screen_height)

            # Colisiones con asteroides
            for asteroid in self.asteroids[:]:
                if self.player.check_collision(asteroid):
                    self.player_health -= 10
                    if self.player_health <= 0:
                        self.running = False
                    self.asteroids.remove(asteroid)
                    continue

                if asteroid.is_ring_asteroid and (
                    asteroid.pos[1] > self.screen_height + 50 or
                    asteroid.pos[1] < -50 or
                    asteroid.pos[0] < -50 or
                    asteroid.pos[0] > self.screen_width + 50
                ):
                    self.asteroids.remove(asteroid)

            # Recoger belt
            if self.item_spawned and not self.item_collected:
                item_rect = pygame.Rect(self.item_pos[0], self.item_pos[1], *self.item_size)
                player_rect = pygame.Rect(self.player.pos[0], self.player.pos[1], *self.player.size)
                if item_rect.colliderect(player_rect):
                    self.item_collected = True
                    self.item_spawn_time = pygame.time.get_ticks()
                    self.belt_count += 1

            # Respawnear belt 10s después de ser recogido
            if self.item_collected and (pygame.time.get_ticks() - self.item_spawn_time) > 10000:
                self.item_collected = False
                self.ring_spawned = False  # permitir nuevo anillo en el siguiente belt
                self.item_pos = [
                    random.randint(0, self.screen_width - self.item_size[0]),
                    random.randint(0, self.screen_height - self.item_size[1])
                ]

            # Dibujar
            self.player.draw(self.screen)
            for asteroid in self.asteroids:
                asteroid.draw(self.screen)

            if self.item_spawned and not self.item_collected:
                self.screen.blit(self.belt_image, (int(self.item_pos[0]), int(self.item_pos[1])))

            # HUD
            health_text = font.render(f"Health: {self.player_health}", True, (255, 255, 255))
            belt_text  = font.render(f"Belts: {self.belt_count}", True, (255, 200, 0))
            self.screen.blit(health_text, (10, 10))
            self.screen.blit(belt_text,   (10, 45))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
    pygame.quit()