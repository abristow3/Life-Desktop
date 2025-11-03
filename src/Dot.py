import pygame

class Dot:
    def __init__(self, color: str, coord_x: int, coord_y: int, radius: int, velocity_x: int, velocity_y: int, width: int = 0):
        self.color = color
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.center_coords = (self.coord_x, self.coord_y)
        self.radius = radius

        # default to 0 for a filled dot
        self.width = width

        # pixels per frame the object will move
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        # Create collision box around Dot
        self.collision_box = pygame.Rect(self.coord_x - self.radius, self.coord_y - self.radius, self.radius*2, self.radius*2)

    def update_position(self, screen_width: int, screen_height: int, dt: float) -> None:
        self.coord_x += self.velocity_x * dt
        self.coord_y += self.velocity_y * dt

        # Bounce off left and right limits
        if self.coord_x - self.radius < 0:
            self.coord_x = self.radius
            self.velocity_x *= -1
        elif self.coord_x + self.radius > screen_width:
            self.coord_x = screen_width - self.radius
            self.velocity_x *= -1
        
        if self.coord_y - self.radius < 0:
            self.coord_y = self.radius
            self.velocity_y *= -1
        elif self.coord_y + self.radius > screen_height:
            self.coord_y = screen_height - self.radius
            self.velocity_y *= -1
        
        self.center_coords = (self.coord_x, self.coord_y)
        self.collision_box.topleft = (self.coord_x - self.radius, self.coord_y - self.radius)

    def detect_collision(self, other_object):
        # Vector between centers
        dx = other_object.coord_x - self.coord_x
        dy = other_object.coord_y - self.coord_y
        distance = (dx**2 + dy**2) ** 0.5

        # Minimum distance for no overlap
        min_distance = self.radius + other_object.radius

        if distance < min_distance and distance != 0:
            # Normalize collision vector
            nx = dx / distance
            ny = dy / distance

            # Overlap amount
            overlap = min_distance - distance

            # Move dots apart along the collision normal
            self.coord_x -= nx * overlap / 2
            self.coord_y -= ny * overlap / 2
            other_object.coord_x += nx * overlap / 2
            other_object.coord_y += ny * overlap / 2

            # Swap velocities (simple elastic collision)
            self.velocity_x, other_object.velocity_x = other_object.velocity_x, self.velocity_x
            self.velocity_y, other_object.velocity_y = other_object.velocity_y, self.velocity_y

            # Update collision boxes
            self.collision_box.topleft = (self.coord_x - self.radius, self.coord_y - self.radius)
            other_object.collision_box.topleft = (other_object.coord_x - other_object.radius, other_object.coord_y - other_object.radius)
