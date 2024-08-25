from game.models import Game, Character

def prompt_generate_response(message, game_id):
    game = Game.objects.get(id=game_id)
    character = Character.objects.get(game=game)
    return f"""
User's Input:
-&-&-
{message}
-&-&-

Current User Character Status:
    hp: {character.hp} / {10 + 2 * character.stat[2]} (current hp / max hp)
    level: {character.level}
    Stats:
    {character.stat} (Strength, Dexterity, Vigor, Intelligence, Faith, Arcane)
    Inventory:
    {character.inventory}
    Equipped Items: 
    {character.equipped} (Left Hand, Right Hand, Armor Slot)
"""

def prompt_intro(game_id):
    game = Game.objects.get(id=game_id)
    character = Character.objects.get(game=game)
    return f"""
# UI
- Users can see their inventory, hp, stats, level in the screen, so you don't need to tell them. 
# GAME RULES
- Users CANNOT use items that aren't in their inventory
- CANNOT heal more than max hp
- There are two modes in our game: Combat, and non-combat:

In Combat : 
Active when facing an enemy
Active when interacting with an npc encounter or a trap
Active when inside a potentially dangerous location

→ the player can choose only one actions per turn

When NOT in combat : 
→ player can do whatever they want
→ player can actively look for encounters with hostile or friendly (or neutral) npcs and events

Items : 
Consumables, and non-consumables
When a player acquires an item, you can decide what it will be, what it will do, and whether it is consumable or reusable. You can add these description in the "lore" section of the item.

Equipments : 
Equipments can be discarded or equipped, but equipping use a turn when done in combat

Encounters : 
Guaranteed friendly encounter after 5 hostile events
10% chance
Friendly events cannot occur twice in a row



Please choose a starting position, and its story line for the following character:
{character.name}({character.origin})

Current User Character Status:
    hp: {character.hp} / {10 + 2 * character.stat[2]} (current hp / max hp)
    level: {character.level}
    Stats:
    {character.stat} (Strength, Dexterity, Vigor, Intelligence, Faith, Arcane)
    Inventory:
    {character.inventory}
    Equipped Items: 
    {character.equipped} (Left Hand, Right Hand, Armor Slot)

3 choices for starting position:
1. bonfire
2. castle
3. dark forest

You should prompt user to take the next action.

OUTPUT FORMAT:
{{'response' : YOUR RESPONSE GOES HERE, 'user_status': {{'hp': CHARACTER'S CHANGED HP, 'level': USER'S CHANGED LEVEL, 'inventory': USER'S CHANGED INVENTORY, 'stat': USER'S CHANGED STAT, 'equipped': USER'S EQUIPPED ITEMS}}}}
**If there is no change in user_status, you don't need to include some of the fields. For example, if no status changed except hp, user_status would be {{'hp':10}}
- Decrease hp whenever you think you should
- 'inventory': should reflect the user's complete inventory whenever user consumes or gains an item. 
- 'inventory' and 'equipped' goes as a set: whenever the inventory OR equipped item changes, please include both keys in the user_status. Both would be returned, or none of it will be returned. 
- 'equipped' should be the item_key data in the inventory, not the display name.
"""