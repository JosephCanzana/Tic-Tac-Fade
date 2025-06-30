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

    def create_cell_rects(self, panel: pygame.Rect, alignment: tuple=[str, str] ,gap=4):

        # Container Size: use the smaller of width/height to keep board square
        container_size = int(min(panel.height, panel.width) * 0.9)
        # Position the board in the panel using alignment
        x,y = self.determine_position((container_size, container_size), panel, alignment)
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

    def reset(self):
        # Reset to the player X
        self.current_player = self.X
        # Reset all cell coordinates
        for _, cell in self._cell_states.items():
            cell["player"] = 0
            cell["turns"] = 0


    # Logic
    def clicked(self, pos: tuple[int, int]) -> bool:
        """
        Try to mark a cell for the current player.
        Returns True if the move was successful, False otherwise.
        """
        for i, row in enumerate(self._cell_rects):
            for j, cell in enumerate(row):
                # Checks if the rectangle is pressed
                if cell.collidepoint(pos):
                    # Checks the coord if not occupied 
                    if not self._cell_states[i, j]["player"] == 0:
                        return False
                    else:
                        # Update it 
                        player = self.current_player
                        self._cell_states[i, j]["player"] = player
                        self._cell_states[i, j]["turns"] = self._TURNS
                        self.update_remaining_turns(player)
                        return True
        return False

    def change_player(self):
        self.current_player = self.O if self.current_player == self.X else self.X
    
    def update_remaining_turns(self, player: int):
        """
        The oldest move after three moves will be remove
        """
        for _, cell in self._cell_states.items():
            # To avoid reducing the move turns of other player
            if not cell["player"] == player:
                continue
            # Reduce turns
            cell["turns"] -= 1
            # If zero make that cell empty again
            if cell["turns"] == 0:
                cell["player"] = 0

    def check_win(self):
        """
        In this Tic Tac Toe variant, each player can only have three active symbols on the board.
        This function checks the currently occupied positions and compares them against all possible winning combinations.
        """
        player = self.current_player
        winning_combinations = [
            # rows
            [(0,0), (0,1), (0,2)],  
            [(1,0), (1,1), (1,2)],
            [(2,0), (2,1), (2,2)],
            # columns
            [(0,1), (1,1), (2,1)],
            [(0,0), (1,0), (2,0)],  
            [(0,2), (1,2), (2,2)],
             # diagonals
            [(0,0), (1,1), (2,2)], 
            [(0,2), (1,1), (2,0)]
        ]

        occupied_rect = []
        for key, cell in self._cell_states.items():
            # Check player symbol
            if cell["player"] == player:
                # Append the coords
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
        for i, row in enumerate(self._cell_rects):  
            for j, cell in enumerate(row):
                # Temporary variables
                player = cell_state[i, j]["player"]
                turns = cell_state[i, j]["turns"]

                # Choosing which sprite to use (1 == x, 2 == o)
                if player == 1:
                    sprite = sprite_1
                elif player == 2:
                    sprite = sprite_2
                else:
                    continue 

                sprite_copy = sprite.copy()
                if turns == 1 and player == self.current_player:
                    sprite_copy.set_alpha(100) 

                # Resize and draw
                w, h = self.responsive_size(sprite_copy.size, cell, 0.8)
                sprite_resized = pygame.transform.scale(sprite_copy, (w, h))
                x, y = self.determine_position(sprite_resized.get_size(), cell, (self.CENTER, self.MIDDLE))
                screen.blit(sprite_resized, (x, y))

