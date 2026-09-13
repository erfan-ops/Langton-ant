import pygame
import math
from typing import Literal


type Block = tuple[int, int]


_PG_LMB = 1


class Ant:
    x: int
    y: int
    _direction: Literal[0, 1, 2, 3] = 0
    color: int
    
    def __init__(self, x: int = 0, y: int = 0, color: int = 0xc070ff) -> None:
        self.x = x
        self.y = y
        self.color = color
    
    def turn_right(self) -> None:
        self._direction = (self._direction + 1) % 4
    
    def turn_left(self) -> None:
        self._direction = (self._direction + 3) % 4
    
    def move_forward(self) -> None:
        if (self._direction == 0):
            self.y += 1
        elif (self._direction == 1):
            self.x += 1
        elif (self._direction == 2):
            self.y -= 1
        else:
            self.x -= 1
    
    def get_pos(self) -> tuple[int, int]:
        return (self.x, self.y)


class AntGame:
    _window_width: int
    _window_height: int
    
    _blocks_in_width: float
    _blocks_in_height: float
    
    _block_size: int
    
    _screen: pygame.surface.Surface
    _clock: pygame.time._clock
    
    _running: bool = True
    
    _fps: float = 60
    
    _background_color: int
    _grid_line_color: int
    _on_block_color: int
    
    _camera_offset: list[int]
    
    _on_blocks: set[Block] = set()
    
    _min_x_block: int
    _max_x_block: int
    _min_y_block: int
    _max_y_block: int
    
    _zoom_factor: float = 1.1
    _ant: Ant
    
    # _mode = "LLRRRLRLRLLR"
    # _colors = (0xff0000, 0x00ff00, 0x0000ff, 0xff00ff, 0xffff00, 0x00ffff, 0xffffff, 0x9000ff, 0x7f7f7f, 0x402000, 0xc070ff, 0x008000)
    
    def __init__(
        self,
        width: int = 600,
        height: int = 600,
        pixel_size: int = 20,
        grid_line_color: int = 0xaba9ad,
        background_color: int = 0x0e0c10,
        ant_color: int = 0xffffff,
        on_block_color: int = 0xffffd0
    ) -> None:
        pygame.init()
        
        self._window_width  = width
        self._window_height = height
        
        self._block_size = pixel_size
        self._blocks_in_width = self._window_width / self._block_size
        self._blocks_in_height = self._window_height / self._block_size
        
        self._screen = pygame.display.set_mode((self._window_width, self._window_height))
        self._clock = pygame.time.Clock()
        
        self._background_color = background_color
        
        self._grid_line_color = grid_line_color
        
        self._ant = Ant(color=ant_color)
        
        self._camera_offset = [
            -int(self._window_width / 2 - self._block_size / 2),
            -int(self._window_height / 2 - self._block_size / 2)
        ]
        
        self._update_drawing_region()

        self._on_block_color = on_block_color
    
    
    def _update_block_size(self, new_size: float) -> None:
        self._block_size = new_size
        self._blocks_in_width = self._window_width / self._block_size
        self._blocks_in_height = self._window_height / self._block_size
    
    
    def _zoom_in(self, zoom: float) -> None:
        zoom_amount = self._zoom_factor ** zoom
        self._update_block_size(self._block_size * zoom_amount)
    
    def _zoom_out(self, zoom: float) -> None:
        zoom_amount = self._zoom_factor ** zoom
        self._update_block_size(self._block_size / zoom_amount)
    
    
    def _update_drawing_region(self) -> None:
        self._min_x_block = int(math.floor(self._camera_offset[0] / self._block_size))
        self._max_x_block = int(math.ceil(self._min_x_block + self._blocks_in_width)) + 1
        
        self._min_y_block = int(math.floor(self._camera_offset[1] / self._block_size))
        self._max_y_block = int(math.ceil(self._min_y_block + self._blocks_in_height)) + 1
    
    
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            # Window events
            if event.type == pygame.QUIT:
                self._running = False
            
            # Keyboard events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
            
            # Mouse events
            elif event.type == pygame.MOUSEMOTION:
                # Check if the left mouse button is down
                if event.buttons[0]:
                    # Move camera
                    self._camera_offset[0] -= event.rel[0]
                    self._camera_offset[1] -= event.rel[1]
                    
                    self._update_drawing_region()
            
            elif event.type == pygame.MOUSEWHEEL:
                scroll_value = event.precise_y
                if scroll_value > 0:
                    self._zoom_in(scroll_value)
                else:
                    self._zoom_out(abs(scroll_value))
                self._update_drawing_region()


    def _draw_grid_lines(self) -> None:
        # vertical lines
        for x_factor in range(1, int(self._blocks_in_width + 1)):
            x = x_factor * self._block_size - self._camera_offset[0] % self._block_size
            pygame.draw.aaline(self._screen, self._grid_line_color, (x, 0), (x, self._window_height))
        
        # horizontal lines
        for y_factor in range(1, int(self._blocks_in_height + 1)):
            y = y_factor * self._block_size - self._camera_offset[1] % self._block_size
            pygame.draw.aaline(self._screen, self._grid_line_color, (0, y), (self._window_width, y))


    def _draw_ant(self) -> None:
        pygame.draw.rect(
            self._screen,
            self._ant.color,
            (
                self._ant.x * self._block_size - self._camera_offset[0],
                self._ant.y * self._block_size - self._camera_offset[1],
                math.ceil(self._block_size),
                math.ceil(self._block_size)
            )
        )
    
    
    def _is_on(self, xy: Block) -> bool:
        return xy in self._on_blocks
    
    
    def _draw_blocks(self) -> None:
        for x_block in range(self._min_x_block, self._max_x_block):
            for y_block in range(self._min_y_block, self._max_y_block):
                if self._is_on((x_block, y_block)):
                    x = x_block * self._block_size - self._camera_offset[0]
                    y = y_block * self._block_size - self._camera_offset[1]
                    pygame.draw.rect(self._screen, self._on_block_color, (x, y, math.ceil(self._block_size), math.ceil(self._block_size)))
    
    
    def _invert_block(self, xy: Block) -> None:
        if self._is_on(xy):
            self._on_blocks.remove(xy)
        else:
            self._on_blocks.add(xy)
    
    
    def _ant_step(self):
        if self._is_on(self._ant.get_pos()):
            self._ant.turn_right()
        else:
            self._ant.turn_left()
        
        self._invert_block(self._ant.get_pos())
        self._ant.move_forward()
    
    
    def run(self) -> None:
        while self._running:
            self._handle_events()
            
            # fill the background
            self._screen.fill(self._background_color)
            
            self._draw_blocks()
            self._draw_ant()
            # self._draw_grid_lines()
            
            self._ant_step()
            
            
            pygame.display.flip()
            self._clock.tick(self._fps)
        
        