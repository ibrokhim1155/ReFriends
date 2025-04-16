from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Do‘st taklif qilish", callback_data="ref")],
        [InlineKeyboardButton(text="💰 Balans", callback_data="balance")],
        [InlineKeyboardButton(text="💸 Pul yechish", callback_data="withdraw")],
        [InlineKeyboardButton(text="🆘 Yordam", callback_data="help")]
    ])

def back_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back")]
    ])

def admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📈 Pul so'rovlarini ko'rish", callback_data="admin_payouts")],
        [InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_channel")],
        [InlineKeyboardButton(text="🗑 Kanallarni o‘chirish", callback_data="admin_delete_channels")],
        [InlineKeyboardButton(text="ℹ️ Yordam foydalanuvchisini sozlash", callback_data="admin_help")]
    ])
