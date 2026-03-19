"""
Core module for techniques logic.
Implements 'Ambient Model' using message editing and timeouts.
Contains Fast Mode, Racing Thoughts (Shuffle), Anxiety Grounding, and Relaxation.
"""
import asyncio
import random
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from locales import LOCALES
from states import NightCalmStates
from utils.donations import add_donation_logic

router = Router()

def get_letter_words(lang: str):
    """
    Randomly selects a letter and a list of words for Cognitive Shuffle.
    Used to divert brain from complex racing thoughts into simple imagery.
    """
    if lang == "ru":
        data = {
            "М": ["Молния ⚡️", "Морковь 🥕", "Мост 🌉", "Медведь 🧸", "Месяц 🌙"],
            "С": ["Солнце ☀️", "Слон 🐘", "Сыр 🧀", "Самолет ✈️", "Свеча 🕯️"],
            "К": ["Кот 🐱", "Корабль 🚢", "Книга 📖", "Колесо 🎡", "Ключ 🔑"],
        }
        letter = random.choice(list(data.keys()))
        return letter, data[letter]
    return "A", ["Apple 🍎", "Ant 🐜"]

# Handlers for "Fast Mode" random selection
async def start_fast_mode(message: types.Message, state: FSMContext, lang: str):
    """
    Entry point for Fast Mode. Picks random sensory tasks and starts the chain.
    """
    tasks = [
        LOCALES[lang]["fast_vision"],
        LOCALES[lang]["fast_touch"],
        LOCALES[lang]["fast_sound"],
        LOCALES[lang]["fast_smell"]
    ]
    random.shuffle(tasks)
    
    # Send first task
    msg = await message.answer(tasks[0])
    await state.set_state(NightCalmStates.fast_mode)
    await state.update_data(current_tasks=tasks[1:], current_msg_id=msg.message_id)
    
    # Build hybrid keyboard (Next or Exit)
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=LOCALES[lang]["btn_next"], callback_data="next_step")],
        [types.InlineKeyboardButton(text=LOCALES[lang]["btn_main_menu"], callback_data="exit_tech")]
    ])
    await msg.edit_reply_markup(reply_markup=kb)
    
    # NO AUTO-PROGRESSION - User will click 'Next'

@router.callback_query(F.data == "next_step")
async def next_step_cb(cb: types.CallbackQuery, state: FSMContext):
    """
    Manual 'Next' button handler. Speeds up the technique.
    """
    await cb.answer()
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await next_step_logic(cb.message, state, lang)

@router.callback_query(F.data == "exit_tech")
async def exit_tech_cb(cb: types.CallbackQuery, state: FSMContext):
    """
    Exit early.
    """
    await cb.answer()
    lang = (await state.get_data()).get("lang", "ru")
    
    text, kb_builder = add_donation_logic(LOCALES[lang]["fast_final"], InlineKeyboardBuilder(), lang)
    await cb.message.edit_text(text, reply_markup=kb_builder.as_markup())
    await state.set_state(NightCalmStates.main_menu)

async def next_step_logic(message: types.Message, state: FSMContext, lang: str):
    """
    Logic for transitioning to the next step in a technique.
    Handles both manual (button) and automatic (timeout) triggers.
    """
    
    # Increment step ID to ignore previous pending timeouts
    data = await state.get_data()
    step_id = data.get("step_id", 0) + 1
    await state.update_data(step_id=step_id)
    
    tasks = data.get("current_tasks", [])
    
    if not tasks:
        # Final message
        text, kb_builder = add_donation_logic(LOCALES[lang]["fast_final"], InlineKeyboardBuilder(), lang)
        await message.edit_text(text, reply_markup=kb_builder.as_markup())
        await state.set_state(NightCalmStates.main_menu)
        return

    # Update Task Content
    next_task = tasks[0]
    try:
        await message.edit_text(next_task)
        # Re-attach keyboard for manual control
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=LOCALES[lang]["btn_next"], callback_data="next_step")],
            [types.InlineKeyboardButton(text=LOCALES[lang]["btn_main_menu"], callback_data="exit_tech")]
        ])
        await message.edit_reply_markup(reply_markup=kb)
    except Exception:
        pass # Handle cases where message is gone

    # Update remaining tasks for next calls
    await state.update_data(current_tasks=tasks[1:])
    
    # NO AUTO-PROGRESSION (User requested manual control)
    # The technique will now only advance when the 'Next' button is clicked.

# Racing Thoughts Start
async def start_racing_thoughts(message: types.Message, state: FSMContext, lang: str):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=LOCALES[lang]["btn_yes"], callback_data="gtd_yes")],
        [types.InlineKeyboardButton(text=LOCALES[lang]["btn_no"], callback_data="gtd_no")]
    ])
    msg = await message.answer(LOCALES[lang]["gtd_question"], reply_markup=kb)
    await state.set_state(NightCalmStates.racing_thoughts_gtd)

@router.callback_query(F.data == "gtd_yes")
async def gtd_yes_cb(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()
    lang = (await state.get_data()).get("lang", "ru")
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=LOCALES[lang]["btn_next"], callback_data="start_shuffle")]
    ])
    await cb.message.edit_text(LOCALES[lang]["gtd_yes"], reply_markup=kb)

@router.callback_query(F.data == "gtd_no")
async def gtd_no_cb(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()
    lang = (await state.get_data()).get("lang", "ru")
    await start_cognitive_shuffle(cb.message, state, lang)

@router.callback_query(F.data == "start_shuffle")
async def start_shuffle_cb(cb: types.CallbackQuery, state: FSMContext):
    """
    Manual 'Next' button handler for Racing Thoughts (Cognitive Shuffle).
    """
    await cb.answer()
    lang = (await state.get_data()).get("lang", "ru")
    await start_cognitive_shuffle(cb.message, state, lang)

async def start_cognitive_shuffle(message: types.Message, state: FSMContext, lang: str):
    letter, words = get_letter_words(lang)
    await message.edit_text(LOCALES[lang]["shuffle_intro"].format(letter=letter))
    await asyncio.sleep(4)
    await sequence_words(message, words, state, lang)

async def sequence_words(message: types.Message, words: list, state: FSMContext, lang: str):
    for word in words:
        if await state.get_state() == NightCalmStates.main_menu: break # Stop if user exited
        await message.edit_text(word)
        await asyncio.sleep(5)
    
    # Final message
    text, kb_builder = add_donation_logic(LOCALES[lang]["fast_final"], InlineKeyboardBuilder(), lang)
    await message.edit_text(text, reply_markup=kb_builder.as_markup())
    await state.set_state(NightCalmStates.main_menu)

# Anxiety & Relax Placeholders (Simplified for now)
async def start_anxiety_mode(message: types.Message, state: FSMContext, lang: str):
    """
    Entry point for Anxiety Grounding.
    Combines Butterfly Hug and slow sensory tasks.
    """
    # Define tasks for this mode
    tasks = [
        LOCALES[lang]["anxiety_butterfly"],
        LOCALES[lang]["anxiety_grounding"]
    ]
    
    # First message: Intro + first task
    msg = await message.answer(LOCALES[lang]["anxiety_intro"])
    await state.set_state(NightCalmStates.anxiety_mode)
    
    # Initial setup: next task + keyboard
    await asyncio.sleep(3) # Short breather before first task
    await msg.edit_text(tasks[0])
    
    await state.update_data(current_tasks=tasks[1:])
    
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=LOCALES[lang]["btn_next"], callback_data="next_step")],
        [types.InlineKeyboardButton(text=LOCALES[lang]["btn_main_menu"], callback_data="exit_tech")]
    ])
    await msg.edit_reply_markup(reply_markup=kb)

async def start_relax_mode(message: types.Message, state: FSMContext, lang: str):
    """
    Breathing mode (4-7-8). This remains somewhat automatic as 
    clicking buttons mid-breath is counter-productive. 
    """
    msg = await message.answer(LOCALES[lang]["relax_intro"])
    await state.set_state(NightCalmStates.relax_mode)
    
    await asyncio.sleep(4)
    for _ in range(4): # 4 cycles of 4-7-8
        try:
            await msg.edit_text(LOCALES[lang]["relax_inhale"])
            await asyncio.sleep(4)
            await msg.edit_text(LOCALES[lang]["relax_hold"])
            await asyncio.sleep(7)
            await msg.edit_text(LOCALES[lang]["relax_exhale"])
            await asyncio.sleep(8)
        except Exception:
            break # Exit if message is gone
        
    # Final message
    text, kb_builder = add_donation_logic(LOCALES[lang]["fast_final"], InlineKeyboardBuilder(), lang)
    await msg.edit_text(text, reply_markup=kb_builder.as_markup())
    await state.set_state(NightCalmStates.main_menu)
