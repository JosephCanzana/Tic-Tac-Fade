import pygame
from panel import Panel

class PlayArea(Panel):
    # Board constants
    _GRID_SIZE = 3  # 3x3 grid
    _BOARD_SIZE = 0.33  # Percentage of container (not used directly)
    # Player constants
    X = 1
    O = 2
    # turns before it fade is 3 + 1 for fading
    _TURNS = 4

    # Cell state
    _cell_states = {
        (0,0): {"player": 0, "turns": 0}, (0,1): {"player": 0, "turns": 0}, (0,2): {"player": 0, "turns": 0},
        (1,0): {"player": 0, "turns": 0}, (1,1): {"player": 0, "turns": 0}, (1,2): {"player": 0, "turns": 0},
        (2,0): {"player": 0, "turns": 0}, (2,1): {"player": 0, "turns": 0}, (2,2): {"player": 0, "turns": 0},
    }


    def __init__(self):
        # Set First move
        self.current_player = self.X

    def create_cell_rects(self, panel: pygame.Rect, alignment: tuple=[int,int] ,gap=4):

        # Container Size: use the smaller of width/height to keep board square
        container_size = min(panel.height, panel.width) * 1
        # Position the board in the panel using alignment
        x,y = self.determine_position(container_size, container_size, panel, alignment)
        # Rectangle object for the board area
        self._container = pygame.Rect(x,y, container_size, container_size)

        # Calculate the top-left corner of the board
        ctnr_locx = self._container.x
        ctnr_locy = self._container.y
        # Calculate the size of each cell (accounting for gaps)
        size = (self._container.width - (self._GRID_SIZE - 1) * gap) // self._GRID_SIZE
        # Create a 2D list of pygame.Rects for each cell
        self._cell_rects = []
        for row in range(self._GRID_SIZE):
            row_rects = []
            for col in range(self._GRID_SIZE):
                x = ctnr_locx + col * (size + gap)
                y = ctnr_locy + row * (size + gap)
                row_rects.append(pygame.Rect(x, y, size, size))
            self._cell_rects.append(row_rects)

    # Logic
    def clicked(self, pos: tuple[int, int]) -> bool:
        """
        Try to mark a cell for the current player.
        Returns True if the move was successful, False otherwise.
        """
        x, y = pos
        for i, row in enumerate(self._cell_rects):
            for j, cell in enumerate(row):
                if cell.collidepoint(x, y):
                    if self._cell_states[i, j]["player"] == 0:
                        player = self.current_player
                        self._cell_states[i, j]["player"] = player
                        self._cell_states[i, j]["turns"] = self._TURNS
                        self.update_remaining_turns(player)
                        return True
                    else:
                        return False
        return False

    def change_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
    
    def update_remaining_turns(self, player: int):
        for _, cell in self._cell_states.items():
            if not cell["player"] == player:
                continue

            cell["turns"] -= 1

            if cell["turns"] == 0:
                cell["player"] = 0

    def check_win(self):
        player = self.current_player
        winning_combinations = [
            [(0,0), (0,1), (0,2)],  # rows
            [(1,0), (1,1), (1,2)],
            [(2,0), (2,1), (2,2)],
            [(0,0), (1,0), (2,0)],  # columns
            [(0,1), (1,1), (2,1)],
            [(0,2), (1,2), (2,2)],
            [(0,0), (1,1), (2,2)],  # diagonals
            [(0,2), (1,1), (2,0)]
        ]
        occupied_rect = []
        for key, cell in self._cell_states.items():
            if cell["player"] == player:
                occupied_rect.append(key)
        if occupied_rect in winning_combinations:
            return True

        

    # Unloading sprite
    def load_sprite(self, screen: pygame.Surface, sprite_1: pygame.Surface, sprite_2: pygame.Surface):
        """
        Draw X and O sprites on the board according to the cell states.
        Side effect: draws to the screen.
        """
        cell_state = self._cell_states
        for i, row in enumerate(self._cell_rects):  # row is a list of rects
            for j, cell in enumerate(row):          # cell is a Rect
                player = cell_state[i, j]["player"]
                turns = cell_state[i, j]["turns"]

                if player == 1:
                    sprite = sprite_1
                elif player == 2:
                    sprite = sprite_2
                else:
                    continue  # Skip empty cell

                # Make a copy so the original isn't affected
                sprite_copy = sprite.copy()

                # Optional transparency condition (turns == 1, for example)
                if turns == 1 and player == self.current_player:
                    sprite_copy.set_alpha(100)  # 0 = invisible, 255 = opaque

                # Resize and draw
                sprite_resized = self.responisve_size(sprite_copy, cell, 0.8)
                x, y = self.determine_position(sprite_resized.get_width(), sprite_resized.get_height(), cell, (self.CENTER, self.MIDDLE))
                screen.blit(sprite_resized, (x, y))

