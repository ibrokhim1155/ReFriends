# from aiogram.exceptions import TelegramBadRequest
# from config import bot, cursor
#
# def get_required_channels():
#     cursor.execute("SELECT username FROM channels")
#     return [row[0] for row in cursor.fetchall()]
#
# async def is_subscribed(user_id: int) -> bool:
#     try:
#         for username in get_required_channels():
#             member = await bot.get_chat_member(f"@{username}", user_id)
#             if member.status not in ("member", "administrator", "creator"):
#                 return False
#         return True
#     except TelegramBadRequest as e:
#         print(f"Subscription check failed: {e.message}")
#         return False
