import pygame
import random
from Circle import Circle
from Ray import Ray

# Screen & Game Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 120

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

NUM_CIRCLES = 30
NUM_RAYS = 10


def create_rays() -> list[Ray]:
    rays = []
    for _ in range(NUM_RAYS):
        speed = random.randint(30, 60)
        x_poo = random.randint(0, SCREEN_WIDTH)
        y_poo = random.randint(0, 30)
        x_term = random.randint(0, SCREEN_WIDTH)
        y_term = random.randint(500, SCREEN_HEIGHT)
        ray = Ray(color=BLUE, speed=speed, x_poo=x_poo, y_poo=y_poo,
                  x_term=x_term, y_term=y_term)
        rays.append(ray)
    return rays


def create_circles() -> list[Circle]:
    circles = []
    for _ in range(NUM_CIRCLES):
        coord_x = random.randint(0, SCREEN_WIDTH)
        coord_y = random.randint(0, SCREEN_HEIGHT)
        radius = random.randint(5, 15)
        vx = random.randint(30, 60)
        vy = random.randint(30, 60)
        circle = Circle(color=RED, coord_x=coord_x, coord_y=coord_y,
                        radius=radius, velocity_x=vx, velocity_y=vy)
        circles.append(circle)
    return circles


def run() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Life Sim")
    clock = pygame.time.Clock()

    # Create game objects
    circles = create_circles()
    rays = create_rays()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        screen.fill(WHITE)

        # --- Update positions ---
        for circle in circles:
            circle.update_position(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, dt=dt)

        for ray in rays:
            ray.update_position(dt=dt)

        # --- Handle collisions between circles ---
        for i in range(len(circles)):
            for j in range(i + 1, len(circles)):
                if circles[i].detect_collision(circles[j]):
                    circles[i].on_collision(circles[j])
                    circles[j].on_collision(circles[i])

        # --- Handle collisions between rays and circles ---
        for ray in rays:
            for circle in circles:
                if ray.detect_collision(circle):
                    ray.on_collision(circle)
                    circle.on_collision(ray)

        # --- Draw everything ---
        for circle in circles:
            circle.draw(screen)
            # Optionally show bounding box for debugging
            pygame.draw.rect(screen, PURPLE, circle.collision_box, width=1)

        for ray in rays:
            ray.draw(screen)
            pygame.draw.rect(screen, PURPLE, ray.collision_box, width=1)

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Refresh screen ---
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    run()
