from typing import Literal

type Color = int


class Ant:
    x: int
    y: int
    _direction: Literal[0, 1, 2, 3] = 0 # UP, RIGHT, DOWN, LEFT
    color: Color
    
    def __init__(self, x: int = 0, y: int = 0, color: Color = 0xc070ff) -> None:
        self.x = x
        self.y = y
        self.color = color
    
    def turn_right(self) -> None:
        self._direction = (self._direction + 1) % 4
    
    def turn_left(self) -> None:
        self._direction = (self._direction + 3) % 4
    
    def move_forward(self) -> None:
        if (self._direction == 0):
            self.y -= 1
        elif (self._direction == 1):
            self.x += 1
        elif (self._direction == 2):
            self.y += 1
        else:
            self.x -= 1
    
    def get_pos(self) -> tuple[int, int]:
        return (self.x, self.y)