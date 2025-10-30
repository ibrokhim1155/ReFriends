from aiogram.fsm.state import State, StatesGroup

class GroupState(StatesGroup):
    group_link = State()

class ChannelState(StatesGroup):
    title = State()
    username = State()
