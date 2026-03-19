from aiogram import Router, F, types
from locales import LOCALES

router = Router()

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    """
    Must answer True within 10 seconds of receiving PreCheckoutQuery.
    """
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    """
    Handle successful payment confirmation.
    """
    # Try to determine language, default to 'ru' if unknown
    # In a real app we might store it in a DB or get from state, 
    # but here we can just use RU as it's the only one implemented.
    lang = "ru"
    locale = LOCALES[lang]
    
    await message.answer(text=locale["payment_success"])
