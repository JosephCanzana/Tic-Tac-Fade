import pygame


class Panel:

    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"

    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"

    def __init__(
        self,
        north_h: float,
        east_w: float,
        south_h: float,
        west_w: float,
        window_size: tuple[int, int],
    ):

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

    def __str__(self):
        return (
            f"North: {self.north}\n"
            f"South: {self.south}\n"
            f"East: {self.east}\n"
            f"West: {self.west}"
        )

    def add(
        self,
        screen: pygame.Surface,
        surface: pygame.Surface,
        alignment: tuple[str, str] = ("center", "middle"),
        size_pct: float = 1.0,
        region_rect: pygame.Rect = None,
        gap: tuple[int, int] = (0, 0),
    ):
        if region_rect is None:
            region_rect = self.center

        # Resize
        surf_w, surf_h = surface.get_size()
        region_w, region_h = region_rect.size

        # Calculate max allowed size based on size_pct
        max_w = int(region_w * size_pct)
        max_h = int(region_h * size_pct)

        # Compute scale factor to fit surface inside region, preserving aspect ratio
        scale = min(max_w / surf_w, max_h / surf_h)
        new_w = int(surf_w * scale)
        new_h = int(surf_h * scale)

        surface = pygame.transform.scale(surface, (new_w, new_h))

        # Alignment logic
        x_align, y_align = alignment
        x = region_rect.x
        y = region_rect.y

        # Horizontal alignment
        match x_align:
            case "center":
                x = region_rect.x + (region_rect.width - new_w) // 2
            case "right":
                x = region_rect.right - new_w
            case "left":
                x = region_rect.x
            case _:
                try:
                    offset = int(x_align)
                except (ValueError, TypeError):
                    raise ValueError(
                        "Alignment must be 'left', 'center', 'right', or an int/str convertible to int."
                    )
                if offset < 0:
                    raise ValueError("Negative offset is not allowed")
                x = region_rect.x + offset

        # Vertical alignment
        match y_align:
            case "middle":
                y = region_rect.y + (region_rect.height - new_h) // 2
            case "top":
                y = region_rect.y
            case "bottom":
                y = region_rect.bottom - new_h
            case _:
                try:
                    offset = int(y_align)
                except (ValueError, TypeError):
                    raise ValueError(
                        "Alignment must be 'top', 'middle', 'bottom', or an int/str convertible to int."
                    )
                if offset < 0:
                    raise ValueError("Negative offset is not allowed")
                y = region_rect.y + offset

        # Gap
        wgap, hgap = gap

        abs_pos = (x + wgap, y + hgap)
        screen.blit(surface, abs_pos)

        return surface

    def resize(self, window_size):
        # Store the full window size (width, height)
        self.window_size = window_size

        # Store the percentage values (e.g., 0.1 = 10%)
        self._set_north(self._north_pct)
        self._set_south(self._south_pct)
        self._set_east(self._east_pct)
        self._set_west(self._west_pct)

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
        pl_height = window_h - north_pl_h - self.south.h

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
