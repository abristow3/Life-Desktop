import pygame
from Dot import Dot
from Ray import Ray
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 120
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
NUM_DOTS = 13
NUM_RAYS = 30

def create_rays() -> list:
    rays = []

    for _ in range(NUM_RAYS):
        speed = random.randint(30,60)
        x_poo = random.randint(0, SCREEN_WIDTH)
        y_poo = random.randint(0, 30)
        x_term = random.randint(0, SCREEN_WIDTH)
        y_term = random.randint(500, SCREEN_HEIGHT)

        ray = Ray(color=BLUE, speed=speed, x_poo=x_poo, y_poo=y_poo, x_term=x_term, y_term=y_term)
        rays.append(ray)
    
    return rays

def create_dots() -> list:
    dots = []
    for _ in range(NUM_DOTS):
        # Randomly generate X and Y coord within screen dimesnions
        coord_x = random.randint(0,SCREEN_WIDTH)
        coord_y = random.randint(0,SCREEN_HEIGHT)
        radius = random.randint(1,15)
        x_velocity = random.randint(30,60)
        y_velocity = random.randint(30,60)

        # Create a dot object
        dot = Dot(color=RED, coord_x=coord_x, coord_y=coord_y, radius=radius, velocity_x=x_velocity, velocity_y=y_velocity)
        dots.append(dot)

    return dots


def run() -> None:
    dots = []
    dots = create_dots()
    rays = []
    rays = create_rays()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Life Sim")
    clock = pygame.time.Clock()

    # Start game loop
    running = True
    while running:
        # delta time since last frame changes based on FPS to maintain stable object speed
        dt = clock.tick(FPS) / 1000 
        
        # Fill canvas with color
        screen.fill(WHITE)

        # Now we need to make sure to redraw dots in every frame
        for dot in dots:
            dot.update_position(dt=dt, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
            pygame.draw.circle(screen, dot.color, dot.center_coords, dot.radius, dot.width)

        for ray in rays:
            ray.update_position(dt=dt)
            pygame.draw.line(screen, ray.color, (ray.x_poo, ray.y_poo), (ray.x_term, ray.y_term), ray.thickness)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # Repaint entire screen at once
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    run()
