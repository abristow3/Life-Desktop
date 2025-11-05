import pygame
import math
from GeometryObject import GeometryObject


class Circle(GeometryObject):
    def __init__(self, color: str, coord_x: int, coord_y: int,
                 radius: int, velocity_x: float, velocity_y: float, width: int = 0):
        super().__init__(color)
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.radius = radius
        self.width = width  # 0 = filled circle
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.update_collision_box()

    # ----------------------------------------------------------------------
    # Movement + Updates
    # ----------------------------------------------------------------------
    def update_position(self, screen_width: int, screen_height: int, dt: float) -> None:
        self.coord_x += self.velocity_x * dt
        self.coord_y += self.velocity_y * dt

        # Bounce off left/right walls
        if self.coord_x - self.radius < 0:
            self.coord_x = self.radius
            self.velocity_x *= -1
        elif self.coord_x + self.radius > screen_width:
            self.coord_x = screen_width - self.radius
            self.velocity_x *= -1

        # Bounce off top/bottom walls
        if self.coord_y - self.radius < 0:
            self.coord_y = self.radius
            self.velocity_y *= -1
        elif self.coord_y + self.radius > screen_height:
            self.coord_y = screen_height - self.radius
            self.velocity_y *= -1

        self.update_collision_box()

    def update_collision_box(self):
        self.collision_box.topleft = (self.coord_x - self.radius, self.coord_y - self.radius)
        self.collision_box.size = (self.radius * 2, self.radius * 2)

    # ----------------------------------------------------------------------
    # Rendering
    # ----------------------------------------------------------------------
    def draw(self, surface):
        pygame.draw.circle(surface, self.color,
                           (int(self.coord_x), int(self.coord_y)),
                           self.radius, self.width)

    def get_position(self):
        return (self.coord_x, self.coord_y)

    # ----------------------------------------------------------------------
    # Collision Detection
    # ----------------------------------------------------------------------
    def detect_collision(self, other_object: GeometryObject) -> bool:
        # Circle-circle collision (if other has a radius)
        if hasattr(other_object, "radius"):
            dx = other_object.coord_x - self.coord_x
            dy = other_object.coord_y - self.coord_y
            distance = math.hypot(dx, dy)
            return distance < (self.radius + other_object.radius)
        else:
            # Fallback to AABB detection (for non-circular geometry)
            return super().detect_collision(other_object)

    # ----------------------------------------------------------------------
    # Collision Response
    # ----------------------------------------------------------------------
    def on_collision(self, other_object: GeometryObject):
        if not hasattr(other_object, "radius"):
            # Only handle circle–circle collisions here
            return

        dx = other_object.coord_x - self.coord_x
        dy = other_object.coord_y - self.coord_y
        distance = math.hypot(dx, dy)

        if distance == 0:
            return  # Avoid division by zero

        min_distance = self.radius + other_object.radius

        # Only resolve if overlapping
        if distance < min_distance:
            # Normalize vector between centers
            nx = dx / distance
            ny = dy / distance

            # Overlap amount
            overlap = min_distance - distance

            # Push both circles apart equally
            self.coord_x -= nx * overlap / 2
            self.coord_y -= ny * overlap / 2
            other_object.coord_x += nx * overlap / 2
            other_object.coord_y += ny * overlap / 2

            # Swap velocities (simple elastic collision)
            self.velocity_x, other_object.velocity_x = other_object.velocity_x, self.velocity_x
            self.velocity_y, other_object.velocity_y = other_object.velocity_y, self.velocity_y

            # Update bounding boxes
            self.update_collision_box()
            other_object.update_collision_box()
