"""
Module for handling the /start command and initial user greeting.
Sets user language and displays the main navigation menu.
"""
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import SUPPORT_URL, PAYMENT_PROVIDER_TOKEN
from locales import LOCALES
from states import NightCalmStates

router = Router()

@router.callback_query(F.data == "start_payment")
async def start_payment_cb(cb: types.CallbackQuery, state: FSMContext):
    """
    Handles the 'start_payment' callback from the donation nudge.
    """
    await cb.answer()
    data = await state.get_data()
    lang = data.get("lang", "ru")
    locale = LOCALES.get(lang, LOCALES["ru"])
    
    # Send a native Telegram invoice (same as /support)
    await cb.message.answer_invoice(
        title=locale["payment_title"],
        description=locale["payment_description"],
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=[
            types.LabeledPrice(label=locale["btn_support"], amount=10000)  # 100.00 RUB
        ],
        payload="support_donation",
        start_parameter="support",
    )

@router.message(Command("support", "donate"))
async def support_command(message: types.Message, state: FSMContext):
    """
    Shows information about how to support the project via native Telegram payments.
    """
    data = await state.get_data()
    lang = data.get("lang", "ru")
    locale = LOCALES.get(lang, LOCALES["ru"])
    
    # Send a native Telegram invoice
    await message.answer_invoice(
        title=locale["payment_title"],
        description=locale["payment_description"],
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=[
            types.LabeledPrice(label=locale["btn_support"], amount=10000)  # 100.00 RUB
        ],
        payload="support_donation",
        start_parameter="support",
    )

@router.message(CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    """
    Initializes the session when the user types /start.
    Defaults language to Russian and displays the main menu.
    """
    # Default localization to RU
    await state.update_data(lang="ru")
    lang_code = "ru"
    
    # Create main menu buttons
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=LOCALES[lang_code]["btn_thoughts"])],
            [types.KeyboardButton(text=LOCALES[lang_code]["btn_anxiety"])],
            [types.KeyboardButton(text=LOCALES[lang_code]["btn_relax"])],
            [types.KeyboardButton(text=LOCALES[lang_code]["btn_fast"])],
        ],
        resize_keyboard=True
    )
    
    # Send welcome text and main menu
    await message.answer(
        text=LOCALES[lang_code]["start_welcome"] + "\n\n" + LOCALES[lang_code]["menu_choose"],
        reply_markup=kb
    )
    
    # Set the state to main menu listening
    await state.set_state(NightCalmStates.main_menu)
