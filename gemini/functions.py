from . import config
from . import prompts
def generate_response(message, game_id):
    model = config.DND_model
    prompt = prompts.prompt_generate_response(message, game_id)
    

    return "tmp"
def send_chat():
    pass