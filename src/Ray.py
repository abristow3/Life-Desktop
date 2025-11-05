import math
import pygame
from GeometryObject import GeometryObject


class Ray(GeometryObject):
    def __init__(self, speed: float, color: str,
                 x_poo: int, y_poo: int, x_term: int, y_term: int):
        super().__init__(color)
        self.speed = speed
        self.thickness = 3

        # Starting point (tail)
        self.x_poo = x_poo
        self.y_poo = y_poo

        # Target point (head)
        self.x_term = x_term
        self.y_term = y_term

        # Calculate normalized direction vector
        distance = math.hypot(self.x_term - self.x_poo, self.y_term - self.y_poo)
        self.dx = (self.x_term - self.x_poo) / distance
        self.dy = (self.y_term - self.y_poo) / distance

        # Fixed ray length
        self.length = 10

        # Store angle (optional, useful for rotation)
        self.angle = math.degrees(math.atan2(self.dy, self.dx))

        self.update_collision_box()

    # ----------------------------------------------------------------------
    # Movement + Updates
    # ----------------------------------------------------------------------
    def update_position(self, dt: float) -> None:
        self.x_poo += self.dx * self.speed * dt
        self.y_poo += self.dy * self.speed * dt
        self.x_term = self.x_poo + self.dx * self.length
        self.y_term = self.y_poo + self.dy * self.length
        self.update_collision_box()

    def update_collision_box(self):
        min_x = min(self.x_poo, self.x_term)
        min_y = min(self.y_poo, self.y_term)
        width = abs(self.x_term - self.x_poo)
        height = abs(self.y_term - self.y_poo)
        # Slight padding to ensure thin lines register collisions visually
        self.collision_box = pygame.Rect(min_x, min_y, max(1, width), max(1, height))

    # ----------------------------------------------------------------------
    # Rendering
    # ----------------------------------------------------------------------
    def draw(self, surface):
        pygame.draw.line(surface, self.color,
                         (int(self.x_poo), int(self.y_poo)),
                         (int(self.x_term), int(self.y_term)),
                         self.thickness)

    def get_position(self):
        return (self.x_poo, self.y_poo)

    # ----------------------------------------------------------------------
    # Collision Detection
    # ----------------------------------------------------------------------
    def detect_collision(self, other_object: GeometryObject) -> bool:
        # Circle–Ray collision
        if hasattr(other_object, "radius"):
            return self._circle_ray_collision(other_object)
        else:
            # Fallback to AABB detection
            return super().detect_collision(other_object)

    def _circle_ray_collision(self, circle_obj) -> bool:
        cx, cy = circle_obj.coord_x, circle_obj.coord_y
        radius = circle_obj.radius

        # Ray origin and direction
        ox, oy = self.x_poo, self.y_poo
        dx, dy = self.dx, self.dy

        # Vector from ray origin to circle center
        fx = cx - ox
        fy = cy - oy

        # Project vector onto ray direction
        t = fx * dx + fy * dy

        # If the closest point is behind the ray origin, ignore
        if t < 0:
            return False

        # Find the closest point on the ray
        closest_x = ox + dx * t
        closest_y = oy + dy * t

        # Compute distance from circle center to that closest point
        dist_sq = (closest_x - cx)**2 + (closest_y - cy)**2

        return dist_sq <= radius**2

    # ----------------------------------------------------------------------
    # Collision Response
    # ----------------------------------------------------------------------
    def on_collision(self, other_object: GeometryObject):
        # Example: Stop moving when hitting something
        # You can override or expand this behavior
        self.speed = 0
