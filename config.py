"""
Configuration module for handling environment variables and bot settings.
"""
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Telegram Bot Token from environment or fallback placeholder
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Donation Settings
SUPPORT_URL = "https://example.com"
DONATION_CHANCE = 0.07  # 7% chance to show donation nudge
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN", "YOUR_PAYMENT_PROVIDER_TOKEN_HERE")
