actions = (
    "acciones",
    "votar",
    "salir",
    "mano",
    "bote",
    "fichas",
    "check",
    "mesa",
    "raise",
    "call",
    "fold",
    "all-in",
)


def validate_users_turn(game, player):
    return game.get_current_player() == player
