import pygame, sys, math

# --- 1. CONSTANTS (Jupiter is locked at 0,0 to simplify math) ---
G_M = 1.266e8 # Jupiter's Gravity constant * Mass combined
ROCHE, JUP_RAD = 120000.0, 69911.0

class Ship:
    def __init__(self):
        # Spawning far to the left to force a wide, sweeping orbital arc
        self.x, self.y = -350000.0, -50000.0
        
        # Carefully calculated vector to hit a periapsis of exactly 115,822 km
        self.vx, self.vy = 12.0, 16.0
        self.fuel = 1200.0
        
        # Point the nose exactly along the velocity vector
        self.angle = math.degrees(math.atan2(16.0, 12.0)) 
        self.trail = []

# --- 2. SETUP ---
pygame.init()
screen = pygame.display.set_mode((900, 700))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier", 24, True)
state, ship = "CLICK TO START", Ship()

# --- 3. MAIN LOOP ---
while True:
    screen.fill((10, 10, 20)) # Wipe screen black
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()
        # Click anywhere on screen to start or restart
        if e.type == pygame.MOUSEBUTTONDOWN:
            if state != "PLAYING": state, ship = "PLAYING", Ship()

    if state == "PLAYING":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: ship.angle -= 3
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: ship.angle += 3
        
        thrusting = (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and ship.fuel > 0
        if thrusting: ship.fuel -= 1
        
        # --- PHYSICS ENGINE (10 sub-steps per frame) ---
        for _ in range(10):
            if thrusting:
                rad = math.radians(ship.angle)
                ship.vx += math.cos(rad) * 0.005 * 0.5
                ship.vy += math.sin(rad) * 0.005 * 0.5
            
            # Simple Pythagorean theorem to find distance to Jupiter at (0,0)
            dist = math.sqrt(ship.x**2 + ship.y**2)
            if dist > 0: # Apply Gravity
                accel = G_M / (dist**2)
                ship.vx -= accel * (ship.x / dist) * 0.5
                ship.vy -= accel * (ship.y / dist) * 0.5
                
            ship.x += ship.vx * 0.5
            ship.y += ship.vy * 0.5
            
            # Check Death Conditions
            if dist < JUP_RAD: state = "CRASHED INTO PLANET"
            elif dist < ROCHE: state = "CRUSHED BY ROCHE LIMIT"
        
        # Record trail
        if pygame.time.get_ticks() % 5 == 0:
            ship.trail.append((ship.x, ship.y))
            if len(ship.trail) > 100: ship.trail.pop(0)

        # Win Condition: Left the 900x700 screen (1 pixel = 1200 km)
        sx, sy = 450 + ship.x / 1200, 350 + ship.y / 1200
        if not (0 < sx < 900 and 0 < sy < 700): state = "SYSTEM ESCAPED!"

    # --- 4. DRAWING ---
    pygame.draw.circle(screen, (80, 20, 20), (450, 350), int(ROCHE / 1200), 1) # Roche
    pygame.draw.circle(screen, (200, 150, 100), (450, 350), int(JUP_RAD / 1200)) # Jupiter
    
    if len(ship.trail) > 1: # Draw Trail
        pts = [(450 + tx/1200, 350 + ty/1200) for tx, ty in ship.trail]
        pygame.draw.lines(screen, (50, 80, 50), False, pts, 2)
        
    if state != "CLICK TO START": # Draw Ship
        sx, sy = 450 + ship.x / 1200, 350 + ship.y / 1200
        pygame.draw.circle(screen, (0, 255, 100), (int(sx), int(sy)), 4)
        rad = math.radians(ship.angle)
        pygame.draw.line(screen, (50, 150, 50), (sx, sy), (sx + math.cos(rad)*20, sy + math.sin(rad)*20), 2)
        
        if state == "PLAYING" and thrusting: # Draw Engine Flame
            pygame.draw.line(screen, (255, 150, 0), (sx, sy), (sx - math.cos(rad)*15, sy - math.sin(rad)*15), 4)

    # Draw UI text
    screen.blit(font.render(f"STATUS: {state} | FUEL: {int(ship.fuel)}", True, (200, 200, 200)), (20, 20))
    
    pygame.display.flip()
    clock.tick(60)