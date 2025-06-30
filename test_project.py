from project import switch_player_symbol, player_reset, set_winner


def test_switch_player_symbol():
    # Switch player working 
    assert switch_player_symbol(1) == 2
    assert switch_player_symbol(2) == 1


def test_player_reset():
    player = {"score": 10, "player_symbol": 2}
    player_reset(player)
    # Check if the player is reset correctly 
    assert player["score"] == 0
    assert player["player_symbol"] == 1


def test_set_winner():
    test_player = {"name": "Player", "player_symbol": 1, "score": 2}
    assert set_winner(test_player) == test_player
    # Check updated score
    assert test_player["score"] == 3
