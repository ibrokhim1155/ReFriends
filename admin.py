from aiogram import types, F
from aiogram.fsm.context import FSMContext
from config import dp
from db import conn, cursor
from states import ChannelState
from keyboards import admin_panel_menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@dp.callback_query(F.data == "admin")
async def admin_panel(callback: types.CallbackQuery):
    await callback.message.edit_text("🔧 Admin paneliga xush kelibsiz", reply_markup=admin_panel_menu())


@dp.callback_query(F.data == "admin_payouts")
async def view_payouts(callback: types.CallbackQuery):
    cursor.execute("SELECT id, user_id, amount FROM payouts WHERE approved = 0")
    payouts = cursor.fetchall()

    if not payouts:
        await callback.message.edit_text("✅ Hozircha tasdiqlanmagan so'rovlar yo'q", reply_markup=admin_panel_menu())
        return

    for payout_id, user_id, amount in payouts:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_{payout_id}"),
                InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin")
            ]
        ])
        await callback.message.answer(
            f"📄 <b>So'rov ID:</b> {payout_id}\n"
            f"<b>Foydalanuvchi ID:</b> {user_id}\n"
            f"<b>Miqdor:</b> {amount} so'm",
            reply_markup=markup
        )


@dp.callback_query(F.data.startswith("approve_"))
async def approve_payout(callback: types.CallbackQuery):
    payout_id = int(callback.data.split("_")[1])
    cursor.execute("UPDATE payouts SET approved = 1 WHERE id = ?", (payout_id,))
    conn.commit()
    await callback.message.answer("✅ To'lov so'rovi tasdiqlandi.")


@dp.callback_query(F.data == "add_channel")
async def add_channel_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("📢 Kanal <b>nomini</b> kiriting:")
    await state.set_state(ChannelState.title)


@dp.message(ChannelState.title)
async def set_channel_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(ChannelState.username)
    await message.answer("📡 Kanal username/linkini kiriting (masalan: @mychannel):")


@dp.message(ChannelState.username)
async def save_channel(message: types.Message, state: FSMContext):
    data = await state.get_data()
    title = data['title']
    username = message.text.strip().replace("@", "").replace("https://t.me/", "")

    try:
        cursor.execute("INSERT OR IGNORE INTO channels (title, username) VALUES (?, ?)", (title, username))
        conn.commit()
        await message.answer(f"✅ Kanal qo‘shildi:\n<b>{title}</b> - @{username}")
    except Exception as e:
        await message.answer("❗ Kanal qo‘shishda xatolik yuz berdi.")
        print("Kanal INSERT xatosi:", e)

    await state.clear()


@dp.callback_query(F.data == "admin_delete_channels")
async def delete_channel_list(callback: types.CallbackQuery):
    cursor.execute("SELECT id, title, username FROM channels")
    channels = cursor.fetchall()
    if not channels:
        await callback.message.answer("❗ Kanallar mavjud emas.", reply_markup=admin_panel_menu())
        return

    for chan_id, title, username in channels:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🗑 O‘chirish", callback_data=f"delete_chan_{chan_id}"),
                InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin")
            ]
        ])
        await callback.message.answer(f"📢 <b>{title}</b> - @{username}", reply_markup=markup)


@dp.callback_query(F.data.startswith("delete_chan_"))
async def delete_channel(callback: types.CallbackQuery):
    chan_id = int(callback.data.split("_")[-1])
    cursor.execute("DELETE FROM channels WHERE id = ?", (chan_id,))
    conn.commit()
    await callback.message.answer("✅ Kanal o‘chirildi.")
