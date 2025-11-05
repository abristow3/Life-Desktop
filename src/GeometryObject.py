from abc import ABC, abstractmethod
from typing import Tuple
import pygame

class GeometryObject(ABC):
    def __init__(self, color: str):
        self.color = color
        self.collision_box = pygame.Rect(0, 0, 0, 0)
    
    @abstractmethod
    def update_position(self, *args, **kwargs):
        pass

    @abstractmethod
    def update_collision_box(self):
        pass

    @staticmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def get_position(self) -> Tuple[float, float]:
        pass

    def detect_collision(self, other: "GeometryObject") -> bool:
        return self.collision_box.colliderect(other.collision_box)
    
    def on_collision(self, other: "GeometryObject"):
        pass
