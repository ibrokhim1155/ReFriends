from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMIN_ID

def back_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Orqaga", callback_data="back")
    return builder.as_markup()



def admin_panel_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="💸 To‘lov so‘rovlari", callback_data="admin_payouts")
    builder.button(text="➕ Kanal qo‘shish", callback_data="add_channel")
    builder.button(text="🗑 Kanallarni o‘chirish", callback_data="admin_delete_channels")
    builder.button(text="⬅️ Asosiy menyu", callback_data="back")
    builder.adjust(1)
    return builder.as_markup()


def admin_start_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Referal guruh/link qo‘shish", callback_data="add_group")
    builder.button(text="👥 Referal statistika", callback_data="ref_stats")
    builder.adjust(1)
    return builder.as_markup()


def main_menu(user_id: int):
    builder = InlineKeyboardBuilder()
    if user_id == ADMIN_ID:
        builder.button(text="➕ Referal guruh/link qo‘shish", callback_data="add_group")
    builder.adjust(1)
    return builder.as_markup()
