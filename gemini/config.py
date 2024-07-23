import google.generativeai as genai
from .tools import *
from DNDAPP.settings import GOOGLE_AI_KEY

genai.configure(api_key=GOOGLE_AI_KEY)

DND_model = genai.GenerativeModel("gemini-1.5-flash-latest",
                                    system_instruction="You are a DND dungeon master",)