import pygame

class Panel:
    def __init__(self, screen: pygame.display,north_h: float, east_w: float, south_h: float, west_w: float, window_size: tuple[int,int]):

        if north_h + south_h > 1 or west_w + east_w > 1:
            raise ValueError(
                "The sum of north and south heights, or west and east widths, must not exceed 1. "
                f"Got north_h + south_h = {north_h + south_h}, west_w + east_w = {west_w + east_w}."
            )
        
        self._north_pct = north_h
        self._east_pct = east_w
        self._west_pct = west_w
        self._south_pct = south_h

        # Store the full window size (width, height)
        self.window_size = window_size

        # Store the percentage values (e.g., 0.1 = 10%)
        self._set_north(north_h)
        self._set_south(south_h)
        self._set_east(east_w)
        self._set_west(west_w)

        return


    def __str__(self):
        return (
            f"North: {self.north}\n"
            f"South: {self.south}\n"
            f"East: {self.east}\n"
            f"West: {self.west}"
        )

    def resize(self, window_size):
        # Store the full window size (width, height)
        self.window_size = window_size

        # Store the percentage values (e.g., 0.1 = 10%)
        self._set_north(self._north_pct)
        self._set_south(self._south_pct)
        self._set_east(self._east_pct)
        self._set_west(self._west_pct)
        return

    def add(self, region_rect: pygame.Rect, surface: pygame.Surface, position: tuple[int, int]):
        ...
        

    # NORTH
    @property
    def north(self):
        return self._north

    def _set_north(self, h_pct):
        w, h = self.window_size
        height = h * h_pct
        self._north = pygame.Rect(0, 0, w, height)

    # SOUTH
    @property
    def south(self):
        return self._south
    
    def _set_south(self, h_pct):
        w, h = self.window_size
        height = h * h_pct
        y_pos = h - height
        self._south = pygame.Rect(0, y_pos, w, height)

    # WEST
    @property
    def west(self):
        return self._west
    
    def _set_west(self, w_pct):
        # Size
        window_w, window_h = self.window_size
        north_pl_h = self.north.height

        # panel width and height
        pl_width = window_w * w_pct
        pl_height = window_h - north_pl_h
        
        # location of y is at the top of the north panel size
        self._west = pygame.Rect(0, north_pl_h, pl_width, pl_height)
    
    # EAST
    @property
    def east(self):
        return self._east

    def _set_east(self, w_pct):
        # Size
        window_w, pl_height = self.window_size
        north_pl_h = self.north.height
        south_pl_h = self.south.height
        
        pl_width = window_w * w_pct
        # the height is fix to window height
        pl_height -= north_pl_h + south_pl_h
        # Making the location of x in oposite side
        x_pos = window_w - pl_width

        # Locating the panel at the top of north panel
        self._east = pygame.Rect(x_pos, north_pl_h, pl_width, pl_height)

    @property
    def center(self):
        window_w, window_h = self.window_size
        north_h = self.north.height
        south_h = self.south.height
        west_w = self.west.width
        east_w = self.east.width

        x = west_w
        y = north_h
        width = window_w - west_w - east_w
        height = window_h - north_h - south_h

        return pygame.Rect(x, y, width, height)
        

