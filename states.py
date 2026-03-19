"""
FSM (Finite State Machine) states for the Night Calm bot.
Defines the current navigation level and ongoing techniques.
"""
from aiogram.fsm.state import State, StatesGroup

class NightCalmStates(StatesGroup):
    """
    States representing the user's progress through the bot's features.
    """
    main_menu = State()               # User is in the main menu selection
    fast_mode = State()               # User is in the randomized fast sensory mode
    racing_thoughts_gtd = State()     # User is answering the GTD filter question
    racing_thoughts_shuffle = State() # User is watching the cognitive shuffle word sequence
    anxiety_mode = State()            # User is in the anxiety/grounding technician
    relax_mode = State()              # User is in the 4-7-8 breathing technician
