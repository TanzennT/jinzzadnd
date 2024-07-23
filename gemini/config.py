import google.generativeai as genai
from .tools import *

GOOGLE_AI_KEY = "AIzaSyB__EjVsdE30r0jG6HnjdpcZt1OfUrqVhY"

genai.configure(api_key=GOOGLE_AI_KEY)

DND_model = genai.GenerativeModel("gemini-1.5-flash-latest",
                                    system_instruction="You are a DND dungeon master",)