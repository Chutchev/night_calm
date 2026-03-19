from aiogram import Router
from .start import router as start_router
from .menu import router as menu_router
from .techniques import router as techniques_router
from .payments import router as payments_router

router = Router()
router.include_router(start_router)
router.include_router(menu_router)
router.include_router(techniques_router)
router.include_router(payments_router)
