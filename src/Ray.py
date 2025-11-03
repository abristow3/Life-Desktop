import math

class Ray:
    def __init__(self, speed: float, color: str, x_poo:int, y_poo: int, x_term:int, y_term:int):
        # Physical Properties
        self.speed = speed
        self.color = color
        self.thickness = 3

        # Starting coordinates
        self.x_poo = x_poo
        self.y_poo = y_poo

        # Ending coords
        self.x_term = x_term
        self.y_term = y_term

        # Calculate direction vector
        distance = math.sqrt((self.x_term - self.x_poo)**2 + (self.y_term - self.y_poo)**2)
        self.dx = (self.x_term - self.x_poo) / distance
        self.dy = (self.y_term - self.y_poo) / distance

        # Fixed ray length
        self.length = 10

        # Angle (optional)
        self.angle = math.degrees(math.atan2(self.dy, self.dx))

    def update_position(self, dt: float) -> None:
        self.x_poo += self.dx * self.speed * dt
        self.y_poo += self.dy * self.speed * dt

        self.x_term = self.x_poo + self.dx * self.length
        self.y_term = self.y_poo + self.dy * self.length



