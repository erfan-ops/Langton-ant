import pygame
import math
from typing import Literal


type Block = tuple[int, int]
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


class AntGame:
    _window_width: int
    _window_height: int
    
    _blocks_in_width: float
    _blocks_in_height: float
    
    _block_size: int
    
    _screen: pygame.surface.Surface
    _clock: pygame.time.Clock
    
    _running: bool = True
    
    _fps: float = 120
    
    _grid_line_color: Color
    
    _camera_offset: list[int]
    
    _on_blocks: set[Block] = set()
    
    _min_x_block: int
    _max_x_block: int
    _min_y_block: int
    _max_y_block: int
    
    _zoom_factor: float = 1.1
    _ant: Ant
    
    _mode: str
    _colors: list[Color]
    
    _block_stages: dict[tuple[int, int], int] = {}
    
    _step_interval: float
    
    _paused: bool = True
    
    def __init__(
        self,
        width: int = 600,
        height: int = 600,
        pixel_size: int = 20,
        grid_line_color: Color = 0xaba9ad,
        ant_color: Color = 0xffffff,
        colors: list[Color] = [0x262428, 0xfdfbff],
        mode: str = "LR",
        step_interval: float = 16
    ) -> None:
        pygame.init()
        
        self._window_width  = width
        self._window_height = height
        
        self._block_size = pixel_size
        self._blocks_in_width = self._window_width / self._block_size
        self._blocks_in_height = self._window_height / self._block_size
        
        self._screen = pygame.display.set_mode((self._window_width, self._window_height))
        self._clock = pygame.time.Clock()
        
        self._grid_line_color = grid_line_color
        
        self._ant = Ant(color=ant_color)
        
        self._camera_offset = [
            -int(self._window_width / 2 - self._block_size / 2),
            -int(self._window_height / 2 - self._block_size / 2)
        ]
        
        self._colors = colors if len(colors) >= 2 else [0x262428, 0xfdfbff] # use defualt colors if colors are invalid
        
        self._mode = mode
        
        self._step_interval = step_interval
        
        self._update_drawing_region()
    
    
    def _update_block_size(self, new_size: float) -> None:
        self._block_size = new_size
        self._blocks_in_width = self._window_width / self._block_size
        self._blocks_in_height = self._window_height / self._block_size
    
    
    def _zoom(self, zoom: float, mouse_pos: tuple[int, int]) -> None:
        mouse_x, mouse_y = mouse_pos

        world_x = (mouse_x + self._camera_offset[0]) / self._block_size
        world_y = (mouse_y + self._camera_offset[1]) / self._block_size

        self._update_block_size(self._block_size * self._zoom_factor ** zoom)

        self._camera_offset[0] = world_x * self._block_size - mouse_x
        self._camera_offset[1] = world_y * self._block_size - mouse_y
    
    
    def _update_drawing_region(self) -> None:
        self._min_x_block = int(math.floor(self._camera_offset[0] / self._block_size))
        self._max_x_block = int(math.ceil(self._min_x_block + self._blocks_in_width)) + 1
        
        self._min_y_block = int(math.floor(self._camera_offset[1] / self._block_size))
        self._max_y_block = int(math.ceil(self._min_y_block + self._blocks_in_height)) + 1
    
    
    def _reset(self):
        self._ant = Ant(color=self._ant.color)
        self._on_blocks.clear()
        self._block_stages.clear()
        self._paused = True
        
        self._camera_offset = [
            -int(self._window_width / 2 - self._block_size / 2),
            -int(self._window_height / 2 - self._block_size / 2)
        ]
    
    
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            # Window events
            if event.type == pygame.QUIT:
                self._running = False
            
            # Keyboard events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n and self._paused:
                    self._paused = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                elif event.key == pygame.K_SPACE:
                    self._paused = not self._paused
                elif event.key == pygame.K_n:
                    self._paused = True
                elif event.key == pygame.K_RIGHT:
                    self._ant_step()
                elif event.key == pygame.K_r:
                    self._reset()
            
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
                mouse_pos = event.pos

                self._zoom(scroll_value, mouse_pos)
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
        if self._ant.x < self._min_x_block or self._ant.x > self._max_x_block or self._ant.y < self._min_y_block or self._ant.y > self._max_y_block:
            return
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
    
    
    def _extract_rgb(self, color: Color) -> tuple[int, int, int]:
        b = color & 0xff
        g = (color >> 8) & 0xff
        r = (color >> 16) & 0xff
        
        return (r, g, b)
    
    
    def _interpolate_color(self, stage: int) -> Color:
        if len(self._mode) == 2:
            return self._colors[-1]
        
        t = (stage+1) / (len(self._mode)-1)
        
        if t <= 0:
            return self._colors[0]
        elif t >= 1:
            return self._colors[-1]
        
        scaled = t * (len(self._colors)-1);
        index = int(scaled);
        local_t = scaled - index;
        
        c1 = self._colors[index]
        c2 = self._colors[index + 1]
        
        r1, g1, b1 = self._extract_rgb(c1)
        r2, g2, b2 = self._extract_rgb(c2)
        
        
        # r1*(1-t) + r2*(t)
        # r1 - r1t + r2t
        # r1 + r2t - r1t
        # r1 + t(r2 - r1)
        
        r_out = int((r2 - r1) * local_t + r1)
        g_out = int((g2 - g1) * local_t + g1)
        b_out = int((b2 - b1) * local_t + b1)
        
        return (r_out << 16) + (g_out << 8) + b_out

    
    def _draw_blocks(self) -> None:
        for x_block in range(self._min_x_block, self._max_x_block):
            for y_block in range(self._min_y_block, self._max_y_block):
                if self._is_on((x_block, y_block)):
                    x = x_block * self._block_size - self._camera_offset[0]
                    y = y_block * self._block_size - self._camera_offset[1]
                    stage = self._block_stages[(x_block, y_block)]
                    color = self._interpolate_color(stage)
                    pygame.draw.rect(self._screen, color, (x, y, math.ceil(self._block_size), math.ceil(self._block_size)))
    
    
    def _update_block(self, xy: Block) -> None:
        if self._is_on(xy) and self._block_stages[xy] < len(self._mode)-2:
            self._block_stages[xy] = self._block_stages[xy] + 1
        elif self._is_on(xy):
            self._on_blocks.remove(xy)
            self._block_stages.pop(xy)
        else:
            self._on_blocks.add(xy)
            self._block_stages[xy] = 0
    
    
    def _ant_step(self):
        if not self._is_on(self._ant.get_pos()):
            mode_index = 0
        else:
            mode_index = self._block_stages[self._ant.get_pos()] + 1
        
        if self._mode[mode_index] == 'R':
            self._ant.turn_right()
        else:
            self._ant.turn_left()
        
        self._update_block(self._ant.get_pos())
        self._ant.move_forward()
    
    
    def run(self) -> None:
        then = pygame.time.get_ticks()
        while self._running:
            now = pygame.time.get_ticks()
            
            self._handle_events()
            
            # fill the background
            self._screen.fill(self._colors[0])
            
            self._draw_blocks()
            self._draw_ant()
            # self._draw_grid_lines()
            
            if self._paused:
                then = now
            else:
                step_diff = now - then
                if step_diff > self._step_interval:
                    number_of_steps = int(step_diff / self._step_interval)
                    for _ in range(number_of_steps):
                        self._ant_step()
                    
                    then += self._step_interval * number_of_steps
            
            
            pygame.display.flip()
            self._clock.tick(self._fps)
        
        