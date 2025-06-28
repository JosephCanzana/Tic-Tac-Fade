import pygame
from panel import Panel
from playarea import PlayArea
from my_color import MyColor

running = True
game_state = "start"
player1 = {"name": "Player 1", "player_symbol": 1, "score": 0}
player2 = {"name": "Player 2", "player_symbol": 2, "score": 0}
winner = player1

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
    }

    return screen, fonts, sprites

def labels(fonts):
    return {
        "cs50p": fonts["secondary"].render("This is CS50P", True, MyColor.secondaryLabel),
        "title": fonts["primary"].render("Tic Tac Fade", True, MyColor.label),
        "footer": fonts["secondary"].render("Tic-Tac-Fade | 2025", True, MyColor.tertiaryLabel),
        "player1": fonts["primary"].render("Player 1", True, MyColor.label),
        "player2": fonts["primary"].render("Player 2", True, MyColor.label),
        "score_p1": fonts["secondary"].render("0", True, MyColor.blue),
        "score_p2": fonts["secondary"].render("0", True, MyColor.purple),
    }


def main():
    global running

    screen, fonts, sprites = init_game()
    labels_dict = labels(fonts)

    # Panel class
    panel = Panel(0.1, 0.23, 0.05, 0.23, screen.get_size())
    # Play area initialization
    play_area = PlayArea()
    # Clock for frame
    clock = pygame.Clock()

    while running:
        if game_state == "start":
            draw_start_screen(screen, panel, clock)
        elif game_state == "game":
            draw_game_screen(screen, panel, play_area, labels_dict, sprites, clock)
        else:
            draw_result_screen(screen, panel, play_area, clock)
        panel.draw(
            screen, MyColor.tertiaryBackground,
            MyColor.primaryBackground,
            MyColor.primaryBackground,
            MyColor.tertiaryBackground,
            MyColor.primaryBackground
        )
        panel.add(screen, labels_dict["footer"], 0.4, panel.south, gap=(0, 2))

    # Game Exit
    pygame.quit()

def draw_game_screen(screen, panel, play_area, labels, sprites, clock):
    global running
    global game_state
    global winner
    score_font = pygame.font.Font("fonts/VCR_OSD.ttf", size=40)

    score = {
        "p1": score_font.render(str(player1["score"]), True, MyColor.blue),
        "p2": score_font.render(str(player2["score"]), True, MyColor.purple)
        }

    play_area.create_cell_rects(panel.center, (panel.CENTER, panel.MIDDLE), 6)

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            panel.resize(screen.get_size())
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_area.clicked(event.pos):
                if play_area.check_win():
                    if play_area.current_player == player1["player_symbol"]:
                        player1["score"] += 1
                        winner = player1
                    else:
                        player2["score"] += 1
                        winner = player2
                    player1["player_symbol"] = 2 if player1["player_symbol"] == 1 else 1
                    player2["player_symbol"] = 1 if player2["player_symbol"] == 1 else 2
                    play_area.reset()
                    game_state = "result"
                
                play_area.change_player()
        if event.type == pygame.QUIT:
            running = False

    panel.add(screen, sprites["board"], 0.9, panel.center)
    panel.add(screen, labels["cs50p"], 0.3, panel.north, (panel.CENTER, panel.TOP), (0, 5))
    panel.add(screen, labels["title"], 0.5, panel.north, gap=(0, 7))
    panel.add(screen, labels["player1"], 0.6, panel.west, (panel.CENTER, panel.TOP), (0, 9))
    panel.add(screen, score["p1"], 0.1, panel.west, (panel.CENTER, panel.BOTTOM), (0, -3))
    panel.add(screen, labels["player2"], 0.6, panel.east, (panel.CENTER, panel.TOP), (0, 9))
    panel.add(screen, score["p2"], 0.1, panel.east, (panel.CENTER, panel.BOTTOM), (0, -3))
    play_area.load_sprite(screen, sprites["x"], sprites["o"])
    pygame.display.flip()
    clock.tick(60)

def draw_start_screen(screen, panel, clock):
    global running
    global game_state
    font = pygame.font.Font("fonts/VT323.ttf", size=40)
    labels ={
        "title": font.render("Tic Tac Toe!?", False, MyColor.label),
        "cs50p": font.render("This is CS50P!!!", False, MyColor.label),
        "start_btn": font.render("Press me!", False, MyColor.label),
        "start": font.render("Start", False, MyColor.label),
    }

    start_rect = add_sprite_rect(screen, panel, labels["start_btn"], 0.3, panel.center, (panel.CENTER, panel.MIDDLE), (0,0))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if start_rect.collidepoint(pos):
                
                game_state = "game"
        
        if event.type == pygame.VIDEORESIZE:
            panel.resize(screen.get_size())
            

        if event.type == pygame.QUIT:
            running = False

    panel.add(screen, labels["title"], 1, panel.north, (panel.CENTER, panel.TOP))
    panel.add(screen, labels["cs50p"], 0.5, panel.center, (panel.CENTER, panel.TOP), (0, 20))
    panel.add(screen, labels["start"], 0.3, panel.center, (panel.CENTER, panel.MIDDLE), (0, -60))

    pygame.display.flip()
    clock.tick(60)

    

def draw_result_screen(screen: pygame.Surface, panel: Panel, play_area: PlayArea, clock: pygame.Clock):
    global running
    global game_state
    global player1
    global player2
    global winner
    font = pygame.font.Font("fonts/VT323.ttf", size=40)
    labels ={
        "game_result": font.render("Game Result", False, MyColor.green),
        "win": font.render("Win", False, MyColor.blue),
        "loss": font.render("Lose", False, MyColor.pink),
        "cs50p": font.render("This is CS50P!!!", False, MyColor.label),
        "score1": font.render(str(player1["score"]), False, MyColor.label),
        "score2": font.render(str(player2["score"]), False, MyColor.label),
        "again": font.render("Play again", False, MyColor.purple),
        "quit": font.render("Leave", False, MyColor.orange),
        "reset": font.render("Reset", False, MyColor.indigo),
    }

    again = add_sprite_rect(screen, panel, labels["again"], 0.5, panel.center, (panel.CENTER, panel.MIDDLE), (0,40))
    reset = add_sprite_rect(screen, panel, labels["reset"], 0.2, panel.center, (panel.CENTER, panel.BOTTOM), (0,-90))
    quit = add_sprite_rect(screen, panel, labels["quit"], 0.2, panel.center, (panel.CENTER, panel.BOTTOM), (0,-40))

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            panel.resize(screen.get_size())

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if again.collidepoint(pos):
                game_state = "game"
            elif reset.collidepoint(pos):
                player1["score"] = 0
                player1["player_symbol"] = 1
                player1["name"] = "Player 1"
                player2["score"] = 0
                player2["player_symbol"] = 2
                player2["name"] = "Player 2"
                game_state = "start"
            elif quit.collidepoint(pos):
                running = False

        if event.type == pygame.QUIT:
            running = False


    panel.add(screen, labels["game_result"], 0.8, panel.north, (panel.CENTER, panel.MIDDLE), (0, 0))
    panel.add(screen, labels["score1"], 0.3, panel.west, (panel.CENTER, panel.BOTTOM), (0, 0))
    panel.add(screen, labels["score2"], 0.3, panel.east, (panel.CENTER, panel.BOTTOM), (0, 0))
    if winner == player1:
        panel.add(screen, labels["loss"], 0.9, panel.east, (panel.CENTER, panel.TOP), (0, 0))
        panel.add(screen, labels["win"], 0.78, panel.west, (panel.CENTER, panel.TOP), (0, 0))
    else:
        panel.add(screen, labels["loss"], 0.78, panel.west, (panel.CENTER, panel.TOP), (0, 0))
        panel.add(screen, labels["win"], 0.9, panel.east, (panel.CENTER, panel.TOP), (0, 0))

    

    # print(f"Player 1 Score: {player1['score']}, Move: {player1["player_symbol"]}")
    # print(f"Player 2 Score: {player2['score']}, Move: {player2["player_symbol"]}")
    
    pygame.display.flip()
    clock.tick(60)


def add_sprite_rect(screen: pygame.Surface, panel: Panel, sprite: pygame.Surface, size_pct: float, region: pygame.Rect, pos: tuple [int, int], gap: tuple[int, int]):
    wgap, hgap = gap

    w, h  = panel.responsive_size(sprite.get_size(), region, size_pct)
    x, y = panel.determine_position((w, h), region, pos)

    x += wgap
    y += hgap
    
    sprite_resized = pygame.transform.scale(sprite, (w, h))
    screen.blit(sprite_resized, (x, y))
    # Return the rect for collision detection
    return pygame.Rect(x, y, w, h)

if __name__ == "__main__":
    main()
