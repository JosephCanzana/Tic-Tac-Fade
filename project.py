import pygame
from panel import Panel
from playarea import PlayArea
from my_color import MyColor

running = True
game_state = "start"
player = {
    1 : {"name": "Player 1",
         "player_symbol": 1,
         "score": 0},
    2 : {"name": "Player 2",
         "player_symbol": 2,
         "score": 0}
}
winner = player[1]

def init_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Tic Tac Fade")

    fonts = {
        "primary": pygame.font.Font("fonts/VT323.ttf", size=40),
        "secondary": pygame.font.Font("fonts/VCR_OSD.ttf", size=40),
    }

    sprites = {
        "board": pygame.image.load("sprites/board.png").convert_alpha(),
        "x": pygame.image.load("sprites/X.png").convert_alpha(),
        "o": pygame.image.load("sprites/O.png").convert_alpha(),
        "trophy": pygame.image.load("sprites/trophy.png").convert_alpha(),
    }

    labels = {
        "start" : {
            "title": fonts["primary"].render("Tic Tac Toe!?", False, MyColor.label),
            "cs50p": fonts["primary"].render("This is CS50P!!!", False, MyColor.indigo),
            "start_btn": fonts["primary"].render("Press me to start!", False, MyColor.blue),
            "start": fonts["primary"].render("Get your friend!", False, MyColor.orange)
            },
        "game" : {
            "cs50p": fonts["secondary"].render("This is CS50P", True, MyColor.secondaryLabel),
            "title": fonts["primary"].render("Tic Tac Fade", True, MyColor.label),
            "player1": fonts["primary"].render("Player 1", True, MyColor.label),
            "player2": fonts["primary"].render("Player 2", True, MyColor.label),
        },
        "result" : {
            "game_result": fonts["primary"].render("Game Result", False, MyColor.green),
            "win": fonts["primary"].render("Win", False, MyColor.blue),
            "lose": fonts["primary"].render("Lose", False, MyColor.pink),
            "cs50p": fonts["secondary"].render("This is CS50P!!!", False, MyColor.label),
            "again": fonts["primary"].render("Play again", False, MyColor.purple),
            "quit": fonts["secondary"].render("Leave", False, MyColor.orange),
            "reset": fonts["secondary"].render("Reset", False, MyColor.indigo)
        }
    }

    return screen, fonts, sprites, labels


def main():
    global running
    screen, fonts, sprites, labels = init_game()

    footer = fonts["secondary"].render("Tic-Tac-Fade | 2025", True, MyColor.tertiaryLabel)

    # Panel class
    panel = Panel(0.1, 0.23, 0.05, 0.23, screen.get_size())
    # Play area initialization
    play_area = PlayArea()
    # Clock for frame
    clock = pygame.Clock()

    while running:
        # Game state
        if game_state == "start":
            draw_start_screen(screen, panel, sprites, labels["start"])
        elif game_state == "game":
            draw_game_screen(screen, panel, play_area, fonts, sprites, labels["game"])
        else:
            draw_result_screen(screen, panel, fonts, sprites, labels["result"],)
        
        # Footer
        panel.draw(
            screen, MyColor.tertiaryBackground,
            MyColor.primaryBackground,
            MyColor.tertiaryBackground,
            MyColor.primaryBackground,
            MyColor.primaryBackground
        )
        panel.add(screen, footer, 0.4, panel.south, gap=(0, 2))
        clock.tick(60)

    # Game Exit
    pygame.quit()


def draw_game_screen(screen: pygame.Surface,
                    panel: Panel,
                    play_area: PlayArea,
                    fonts: dict,
                    sprites: dict,
                    labels: dict):
    global running
    global game_state
    global winner

    score = {
        "p1": fonts["secondary"].render(str(player[1]["score"]), True, MyColor.blue),
        "p2": fonts["secondary"].render(str(player[2]["score"]), True, MyColor.purple)
        }

    # Playing Board rectangles
    play_area.create_cell_rects(panel.center, (panel.CENTER, panel.MIDDLE), 6)

    for event in pygame.event.get():

        if event.type == pygame.VIDEORESIZE:
            panel.resize(screen.get_size())

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Cursor inside the board rectangles
            if play_area.clicked(event.pos):
                # Check board statesto see if winner exist
                if play_area.check_win():
                    if play_area.current_player == player[1]["player_symbol"]:
                        winner = set_winner(player[1])
                    else:
                        winner = winner = set_winner(player[2])

                    # Player symbol swap
                    player[1]["player_symbol"] = switch_player_symbol(player[1]["player_symbol"])
                    player[2]["player_symbol"] = switch_player_symbol(player[2]["player_symbol"])

                    # reset the play area
                    play_area.reset()

                    # Game state to result
                    game_state = "result"
                # Next player
                else:
                    play_area.change_player()

        if event.type == pygame.QUIT:
            running = False

    # Add sprite and label
    panel.add(screen, sprites["board"], 0.9, panel.center)
    panel.add(screen, labels["cs50p"], 0.3, panel.north, (panel.CENTER, panel.TOP), (0, 5))
    panel.add(screen, labels["title"], 0.5, panel.north, gap=(0, 7))
    panel.add(screen, labels["player1"], 0.6, panel.west, (panel.CENTER, panel.TOP), (0, 9))
    panel.add(screen, score["p1"], 0.1, panel.west, (panel.CENTER, panel.BOTTOM), (0, -3))
    panel.add(screen, labels["player2"], 0.6, panel.east, (panel.CENTER, panel.TOP), (0, 9))
    panel.add(screen, score["p2"], 0.1, panel.east, (panel.CENTER, panel.BOTTOM), (0, -3))
    # Show what is th eplayer symbol
    if player[1]["player_symbol"] == 1:
        panel.add(screen, panel.fade_sprite_copy(sprites["x"], 130), 0.35, panel.west, (panel.CENTER, panel.MIDDLE), (0, 0))
        panel.add(screen, panel.fade_sprite_copy(sprites["o"], 130), 0.35, panel.east, (panel.CENTER, panel.MIDDLE), (0, 0))
    else:
        panel.add(screen, panel.fade_sprite_copy(sprites["o"], 130), 0.35, panel.west, (panel.CENTER, panel.MIDDLE), (0, 0))
        panel.add(screen, panel.fade_sprite_copy(sprites["x"], 130), 0.35, panel.east, (panel.CENTER, panel.MIDDLE), (0, 0))

    # Passing the sprite to play area
    play_area.load_sprite(screen, sprites["x"], sprites["o"])
    pygame.display.flip()


def draw_start_screen(screen: pygame.Surface,
                    panel: Panel,
                    sprites: dict,
                    labels: dict):
    global running
    global game_state

    # Sprite with rectangle
    start_rect = panel.add_sprite_rect(screen, labels["start_btn"], 0.8, panel.center, (panel.CENTER, panel.BOTTOM), (0,-25))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                game_state = "game"

        if event.type == pygame.VIDEORESIZE:
            panel.resize(screen.get_size())

        if event.type == pygame.QUIT:
            running = False

    # Sprites
    panel.add(screen, labels["title"], 1, panel.north, (panel.CENTER, panel.TOP))
    panel.add(screen, labels["cs50p"], 0.5, panel.center, (panel.CENTER, panel.TOP), (0, 20))
    panel.add(screen, sprites["board"], 0.5, panel.center, (panel.CENTER, panel.MIDDLE), (0, 0))
    panel.add(screen, sprites["o"], 0.5, panel.east, (panel.CENTER, panel.MIDDLE), (0, 0))
    panel.add(screen, sprites["x"], 0.5, panel.west, (panel.CENTER, panel.MIDDLE), (0, 0))
    pygame.display.flip()
    

def draw_result_screen(screen: pygame.Surface, 
                       panel: Panel, 
                       fonts: dict, 
                       sprites: dict, 
                       labels: dict):
    
    # Global variables
    global running
    global game_state
    global player
    global winner

    score = {
        "score1": fonts["primary"].render(str(player[1]["score"]), False, MyColor.label),
        "score2": fonts["primary"].render(str(player[2]["score"]), False, MyColor.label),
        }

    again = panel.add_sprite_rect(screen, labels["again"], 0.5, panel.center, (panel.CENTER, panel.MIDDLE), (0,40))
    reset = panel.add_sprite_rect(screen, labels["reset"], 0.2, panel.center, (panel.CENTER, panel.BOTTOM), (0,-90))
    quit = panel.add_sprite_rect(screen, labels["quit"], 0.2, panel.center, (panel.CENTER, panel.BOTTOM), (0,-40))

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            panel.resize(screen.get_size())

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if again.collidepoint(pos):
                game_state = "game"
            elif reset.collidepoint(pos):
                player_reset(player[1])
                player_reset(player[2])
                game_state = "start"
            elif quit.collidepoint(pos):
                running = False

        if event.type == pygame.QUIT:
            running = False


    panel.add(screen, labels["game_result"], 0.8, panel.north, (panel.CENTER, panel.MIDDLE), (0, 0))
    panel.add(screen, score["score1"], 0.3, panel.west, (panel.CENTER, panel.BOTTOM), (0, 0))
    panel.add(screen, score["score2"], 0.3, panel.east, (panel.CENTER, panel.BOTTOM), (0, 0))
    panel.add(screen, panel.fade_sprite_copy(sprites["trophy"], 170), 0.3, panel.center, (panel.CENTER, panel.TOP), (0, -10))
    if winner == player[1]:
        panel.add(screen, labels["lose"], 0.9, panel.east, (panel.CENTER, panel.TOP), (0, 0))
        panel.add(screen, labels["win"], 0.75, panel.west, (panel.CENTER, panel.TOP), (0, 0))
    else:
        panel.add(screen, labels["lose"], 0.9, panel.west, (panel.CENTER, panel.TOP), (0, 0))
        panel.add(screen, labels["win"], 0.75, panel.east, (panel.CENTER, panel.TOP), (0, 0))
 
    pygame.display.flip()


def switch_player_symbol(current):
    return 2 if current == 1 else 1


def player_reset(player):
    player["score"] = 0
    player["player_symbol"] = 1


def set_winner(player):
    player["score"] += 1
    return player


if __name__ == "__main__":
    main()
