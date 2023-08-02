from aiogram.dispatcher.filters.state import State, StatesGroup

class UserSectionsState(StatesGroup):
    MENU = State()
    SOLUTION = State()
    TASK = State()

class UserStatusState(StatesGroup):
    USER = State()
    ADMIN = State()