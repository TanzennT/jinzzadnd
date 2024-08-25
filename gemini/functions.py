from . import config
from . import prompts
from game.models import Log, Game
import json

def get_chat_history(game_id):
    logs = Log.objects.filter(game=game_id)
    history = []
    for log in logs:
        for content in log.contents:  # Iterate through each message in the log
            history.append({
                "role": content["role"],
                "parts": [
                    {"text": json.dumps(content["parts"][0]["text"])}  # Assuming you have only one "text" part
                ]
            })
    return history


def generate_response(message, game_id):
    get_chat_history(game_id)
    model = config.DND_model
    prompt = prompts.prompt_generate_response(message, game_id)
    chat = model.start_chat(history=get_chat_history(game_id)) # Error in setting history
    response = chat.send_message(prompt)
    
    # Save Log
    log = Log()
    chat_len = len(chat.history)
    content = []
    content.append({"role": chat.history[-2].role, "parts": [ {"text": chat.history[-2].parts[0].text}]})
    content.append({"role": chat.history[-1].role, "parts": [ {"text": json.loads(chat.history[-1].parts[0].text)}]})
    log.game = Game.objects.get(id=game_id)
    log.contents = content
    log.save()
    print(response.text)
    return json.loads(response.text)

def generate_intro(game_id):
    game = Game.objects.get(id=game_id)
    model = config.DND_model
    prompt = prompts.prompt_intro(game_id)
    print(prompt)
    chat = model.start_chat()
    response = chat.send_message(prompt)

    # Save Log
    log = Log()
    content = []
    content.append({"role": chat.history[-2].role, "parts": [ {"text": chat.history[-2].parts[0].text}]})
    content.append({"role": chat.history[-1].role, "parts": [ {"text": json.loads(chat.history[-1].parts[0].text)}]})
    log.game = game
    log.contents = content
    log.save()
    return json.loads(response.text)