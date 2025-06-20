import pygame
from panel import Panel
from my_color import MyColor
        
def main():
    # Start
    pygame.init()

    # Game window aesthetics
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Tic Tac Fade")


    # Sprites
    board = pygame.image.load("sprites/board.png").convert_alpha()
    board = scale_image_to_window(board, screen.size)
    o_sprite = pygame.image.load("sprites/O.png").convert_alpha()
    x_sprite = pygame.image.load("sprites/X.png").convert_alpha()

    board_location = center_image_to_border(board.size, screen.get_size())

    panel = Panel(screen,0.1, 0.2, 0.05, 0.2, screen.get_size())
    print(f"Size: {screen.size}")
    print(f"Get Size: {screen.get_size()}")

    # Clock for frame
    clock = pygame.Clock()

    running = True
    while running:
        # Background intial
        background = MyColor.primaryBackground
        screen.fill(background)

        screen.blit(board,board_location)

        # Get all event and update
        for event in pygame.event.get():
            # window resize
            if event.type == pygame.VIDEORESIZE:
                board = scale_image_to_window(board, screen.get_size())
                board_location = center_image_to_border(board.size, screen.get_size())
                panel.resize(screen.get_size())


            # Window exit button clicked
            if event.type == pygame.QUIT:
                running = False


        # Adding Panel
        pygame.draw.rect(screen, rect=panel.north, color="#4C8ADBEE")
        pygame.draw.rect(screen, rect=panel.east, color="#AE00EDEF")
        pygame.draw.rect(screen, rect=panel.west, color="#EBE94DFF")
        pygame.draw.rect(screen, rect=panel.south, color="#6CEB65EE")
        pygame.draw.rect(screen, rect=panel.center, color="#474949ED")


        # Update display
        pygame.display.update()
        #  Frame Rate
        clock.tick(60)

    # Game Exit
    pygame.quit()


def scale_image_to_window(image: pygame.Surface, window_size: tuple[int, int]) -> pygame.Surface:

    # Window size minimum
    window_width, window_height = window_size
    scale_base = min(window_width, window_height)
    # Resize
    surface_size = int(scale_base * 0.90)

    return pygame.transform.scale(image, (surface_size, surface_size))
    

def center_image_to_border(surface_size: tuple[int, int],window_size: tuple[int, int]) -> tuple[int, int]:
    w_window, h_window = window_size
    w_surface, h_surface = surface_size

    location_x = (w_window - w_surface) // 2
    location_y = (h_window - h_surface) // 2

    return location_x, location_y


if __name__ == "__main__":
    main()
