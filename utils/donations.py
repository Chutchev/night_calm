import random
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import DONATION_CHANCE, SUPPORT_URL
from locales import LOCALES

def add_donation_logic(text: str, keyboard_builder: InlineKeyboardBuilder, lang: str = "ru"):
    """
    Randomly adds donation nudge text and a button to the message.
    """
    if random.random() < DONATION_CHANCE:
        locale = LOCALES.get(lang, LOCALES["ru"])
        
        # Add nudge text
        new_text = text + locale["donation_nudge"]
        
        # Add donation button
        keyboard_builder.button(text=locale["btn_support"], url=SUPPORT_URL)
        
        return new_text, keyboard_builder
    
    return text, keyboard_builder
