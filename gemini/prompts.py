from game.models import Game, Character

def prompt_generate_response(message, game_id):
    game = Game.objects.get(id=game_id)
    character = Character.objects.get(game=game)
    return f"""
Your last response:
{game.last_response}

User's Input:
{message}

Current User Character Status:
{character.hp} / {10 + 2 * character.stat[2]}
    Stats:
    {character.stat} (Strength, Dexterity, Vigor, Intelligence, Faith, Arcane)

    """
    pass

def prompt_intro(game_id):
    game = Game.objects.get(id=game_id)
    character = Character.objects.get(game=game)
    return f"""
Please choose a starting position for the following character:
{character.name}: {character.origin}

3 choices for starting position:
1. bonfire
2. castle
3. dark forest
    """