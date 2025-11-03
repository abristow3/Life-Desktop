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

    def update_position(self, screen_width: int, screen_height: int, dt: float) -> None:
        self.coord_x, self.coord_y = self.center_coords
        self.coord_x += self.velocity_x * dt
        self.coord_y += self.velocity_y * dt

        # Bounce off left and right limits
        if self.coord_x - self.radius <= 0 or self.coord_x + self.radius >= screen_width:
            # reverse horiztontal direction
            self.velocity_x *= -1
        
        if self.coord_y - self.radius <= 0 or self.coord_y + self.radius >= screen_height:
            # reverse vertical direction
            self.velocity_y *= -1

        self.center_coords = (self.coord_x, self.coord_y)