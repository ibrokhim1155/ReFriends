from aiogram.fsm.state import State, StatesGroup

class WithdrawState(StatesGroup):
    full_name = State()
    card_number = State()

class ChannelState(StatesGroup):
    title = State()
    username = State()
