from . import config
from . import prompts
def generate_response(message, game_id):
    model = config.DND_model
    prompt = prompts.prompt_generate_response(message, game_id)
    chat = model.start_chat()
    response = chat.send_message(prompt)
    return response.text

def generate_intro(game_id):
    model = config.DND_model
    prompt = prompts.prompt_intro(game_id)
    print(prompt)
    chat = model.start_chat()
    response = chat.send_message(prompt)
    return response.text