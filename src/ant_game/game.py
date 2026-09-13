import pygame


_PG_LMB = 1

class AntGame:
    _window_width: int
    _window_height: int
    
    _blocks_in_width: int
    _blocks_in_height: int
    
    _block_size: int
    
    _screen: pygame.surface.Surface
    _clock: pygame.time._clock
    
    _running: bool = True
    
    _fps: float = 60
    
    _background_color: int
    
    _grid_line_color: int
    
    # --- Ant --- #
    # (x, y)
    _ant_pos: list[int, int] = [0, 0]
    _ant_color: int
    
    _camera_offset: list[int, int]
    
    _on_blocks: set[tuple[int, int]] = {}
    
    def __init__(
        self,
        width: int = 20,
        height: int = 20,
        pixel_size: int = 20,
        grid_line_color: int = 0xaba9ad,
        background_color: int = 0x0e0c10,
        ant_color: int = 0xffffff
    ):
        pygame.init()
        
        self._blocks_in_width = width
        self._blocks_in_height = height
        self._block_size = pixel_size
        
        self._window_width  = self._blocks_in_width * self._block_size
        self._window_height = self._blocks_in_height * self._block_size
        
        self._screen = pygame.display.set_mode((self._window_width, self._window_height))
        self._clock = pygame.time.Clock()
        
        self._background_color = background_color
        
        self._grid_line_color = grid_line_color
        
        self._ant_color = ant_color
        
        self._camera_offset = [
            -int(self._window_width / 2 - self._block_size / 2),
            -int(self._window_height / 2 - self._block_size / 2)
        ]
    
    
    def _handle_events(self):
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


    def _draw_grid_lines(self):
        # vertical lines
        for x_factor in range(1, self._blocks_in_width + 1):
            x = x_factor * self._block_size - self._camera_offset[0] % self._block_size
            pygame.draw.aaline(self._screen, self._grid_line_color, (x, 0), (x, self._window_height))
        
        # horizontal lines
        for y_factor in range(1, self._blocks_in_width + 1):
            y = y_factor * self._block_size - self._camera_offset[1] % self._block_size
            pygame.draw.aaline(self._screen, self._grid_line_color, (0, y), (self._window_width, y))


    def _draw_ant(self):
        pygame.draw.rect(
            self._screen,
            self._ant_color,
            (
                self._ant_pos[0] * self._block_size - self._camera_offset[0],
                self._ant_pos[1] * self._block_size - self._camera_offset[1],
                self._block_size,
                self._block_size
            )
        )
    
    
    def run(self):
        while self._running:
            self._handle_events()
            
            # fill the background
            self._screen.fill(self._background_color)
            
            self._draw_grid_lines()
            
            self._draw_ant()
            
            
            pygame.display.flip()
            self._clock.tick(self._fps)
        
        