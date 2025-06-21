import pygame
from panel import Panel
from my_color import MyColor


def main():
    # Start
    pygame.init()

    # Game window
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Tic Tac Fade")

    # Font
    primary_font = pygame.font.SysFont("Segoi UI", size=40) 
    secondary_font = pygame.font.SysFont("Arial", size=40) 
    

    # Sprites
    board = pygame.image.load("sprites/board.png").convert_alpha()
    x_sprite = pygame.image.load("sprites/X.png").convert_alpha()
    o_sprite = pygame.image.load("sprites/O.png").convert_alpha()

    # Labels
    cs50p = secondary_font.render("This is CS50P",False ,MyColor.secondaryLabel)
    title = primary_font.render("Tic Tac Fade", False, MyColor.label)
    footer = secondary_font.render("Tic-Tac-Fade | 2025", True, MyColor.quaternaryLabel)

    player1 = primary_font.render("Player 1", True, MyColor.tertiaryLabel)
    player2 = primary_font.render("Player 2", True, MyColor.tertiaryLabel)
    score_p1 = secondary_font.render("0", True, MyColor.tertiaryLabel)
    score_p2 = secondary_font.render("0", True, MyColor.tertiaryLabel)

    # Panel class
    panel = Panel(0.1, 0.23, 0.05, 0.23, screen.get_size())

    # Clock for frame
    clock = pygame.Clock()

    running = True
    while running:
        # Background intial
        background = MyColor.primaryBackground
        screen.fill(background)

        # Get all event and update
        for event in pygame.event.get():
            # window resize
            if event.type == pygame.VIDEORESIZE:
                panel.resize(screen.get_size())

            # Window exit button clicked
            if event.type == pygame.QUIT:
                running = False

        # Adding Panel
        pygame.draw.rect(screen, rect=panel.north, color=MyColor.tertiaryBackground)
        pygame.draw.rect(screen, rect=panel.east, color=MyColor.primaryBackground)
        pygame.draw.rect(screen, rect=panel.west, color=MyColor.primaryBackground)
        pygame.draw.rect(screen, rect=panel.south, color=MyColor.tertiaryBackground)
        pygame.draw.rect(screen, rect=panel.center, color=MyColor.primaryBackground)

        # Add Sprite
        panel.add(screen, board, (panel.CENTER, panel.MIDDLE), 1, panel.center)

        panel.add(screen, cs50p, (panel.CENTER, panel.TOP), 0.3, panel.north, (0, 5))
        panel.add(screen, title, (panel.CENTER, panel.MIDDLE), 0.5, panel.north, (0, 7))

        panel.add(screen, footer, (panel.CENTER, panel.MIDDLE), 0.6, panel.south, (0, 0))

        panel.add(screen, player1, (panel.CENTER, panel.TOP), 0.5, panel.west, (0, 9))
        panel.add(screen, score_p1, (panel.CENTER, panel.BOTTOM), 0.1, panel.west, (0, -3))

        panel.add(screen, player2, (panel.CENTER, panel.TOP), 0.5, panel.east, (0, 9))
        panel.add(screen, score_p2, (panel.CENTER, panel.BOTTOM), 0.1, panel.east, (0, -3))


        # Update display
        pygame.display.update()
        #  Frame Rate
        clock.tick(60)

    # Game Exit
    pygame.quit()

if __name__ == "__main__":
    main()
