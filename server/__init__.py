actions = (
    "acciones",
    "votar",
    "apuesta",
    "salir",
    "mano",
    "bote",
    "fichas",
    "pasar",
    "mesa",
)


def validate_users_turn(game, player):
    return game.get_current_player() == player
