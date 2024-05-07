from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    start = State()
    get_role = State()
    dialog = State()
