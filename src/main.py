import pygame
from Dot import Dot
import random

def run() -> None:
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    NUM_DOTS = 13
    dots_drawn = False
    dots = []

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Life Sim")

    # Start game loop
    running = True
    while running:
        # Fill canvas with color
        screen.fill(WHITE)

        if not dots_drawn:
            for _ in range(NUM_DOTS):
                # Randomly generate X and Y coord within screen dimesnions
                coord_x = random.randint(0,SCREEN_WIDTH)
                coord_y = random.randint(0,SCREEN_HEIGHT)
                radius = random.randint(1,15)
                x_velocity = random.randint(1,3)
                y_velocity = random.randint(1,3)

                # Create a dot object
                dot = Dot(color=RED, coord_x=coord_x, coord_y=coord_y, radius=radius, velocity_x=x_velocity, velocity_y=y_velocity)
                dots.append(dot)
            dots_drawn = True

        # Now we need to make sure to redraw dots in every frame
        for dot in dots:
            dot.update_position(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
            pygame.draw.circle(screen, dot.color, dot.center_coords, dot.radius, dot.width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # Repaint
        pygame.display.flip()
        # Control frame rate (optional, but recommended for smooth movement)
        pygame.time.Clock().tick(60) # Limits to 60 frames per second

    pygame.quit()

if __name__ == '__main__':
    run()
