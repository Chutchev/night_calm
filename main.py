"""
Main entry point for the Night Calm Telegram Bot.
Initializes the bot, dispatcher, and starts the polling.
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import router

async def main():
    """
    Asynchronous main function for bot initialization and startup.
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize bot and dispatcher with memory storage (no database)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Include all route handlers
    dp.include_router(router)
    
    print("Night Calm Bot is starting...")
    # Start polling for updates
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
