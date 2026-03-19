"""
Router for handling main menu button selections.
Routes users to specific techniques based on their choice.
"""
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from locales import LOCALES
from states import NightCalmStates
from locales import LOCALES
from states import NightCalmStates
from .techniques import start_fast_mode, start_racing_thoughts, start_anxiety_mode, start_relax_mode

router = Router()

@router.message(NightCalmStates.main_menu)
async def handle_menu(message: types.Message, state: FSMContext):
    """
    Listens for main menu button texts and triggers corresponding functions.
    """
    # Fetch current user session data (language)
    data = await state.get_data()
    lang = data.get("lang", "ru")
    text = message.text
    
    # Route to Fast Mode
    if text == LOCALES[lang]["btn_fast"]:
        await start_fast_mode(message, state, lang)
    # Route to Racing Thoughts (GTD + Shuffle)
    elif text == LOCALES[lang]["btn_thoughts"]:
        await start_racing_thoughts(message, state, lang)
    # Route to Anxiety Grounding
    elif text == LOCALES[lang]["btn_anxiety"]:
        await start_anxiety_mode(message, state, lang)
    # Route to Relaxation (Breathing)
    elif text == LOCALES[lang]["btn_relax"]:
        await start_relax_mode(message, state, lang)
    # Re-show menu if input is invalid
    else:
        await message.answer(LOCALES[lang]["menu_choose"])
