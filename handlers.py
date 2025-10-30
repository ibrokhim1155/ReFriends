from aiogram import types, F
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter, MEMBER
from aiogram.fsm.context import FSMContext
from config import dp, bot, ADMIN_ID
from db import conn, cursor
from states import GroupState
from keyboards import main_menu, back_menu, admin_start_menu

temp_referrals = {}


def get_referral_count(user_id: int) -> int:
    cursor.execute("SELECT referrals FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else 0


def get_referral_stats():
    cursor.execute("""
        SELECT full_name, user_id, referrals
        FROM users
        WHERE user_id != ?
        ORDER BY referrals DESC
    """, (ADMIN_ID,))
    return cursor.fetchall()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name or "Noma’lum"
    args = message.text.split(maxsplit=1)
    payload = args[1] if len(args) > 1 else None

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (ADMIN_ID,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (user_id, full_name) VALUES (?, ?)", (ADMIN_ID, "Admin"))
        conn.commit()

    if user_id == ADMIN_ID:
        await message.answer(
            "🔧 Admin paneliga xush kelibsiz!\nBu yerda siz referal guruh yoki kanal qo‘shishingiz mumkin.",
            reply_markup=admin_start_menu()
        )
        return

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        referred_by = int(payload) if payload and payload.isdigit() and int(payload) != user_id else None
        cursor.execute(
            "INSERT INTO users (user_id, full_name, referred_by) VALUES (?, ?, ?)",
            (user_id, full_name, referred_by)
        )
        conn.commit()
        if referred_by:
            temp_referrals[user_id] = referred_by

    cursor.execute("SELECT group_link FROM users WHERE user_id = ?", (ADMIN_ID,))
    admin_group = cursor.fetchone()
    group_link = admin_group[0] if admin_group and admin_group[0] else None

    if not group_link:
        await message.answer("Admin hali guruh linkini qo‘shmagan.")
        return

    await message.answer(
        f"👋 Xush kelibsiz, {full_name}!\n\n"
        f"📨 Sizning referal havolangiz:\n"
        f"<code>https://t.me/{(await bot.get_me()).username}?start={user_id}</code>\n\n"
        f"👥 Siz orqali kelganlar soni: {get_referral_count(user_id)} ta\n\n"
        f"🔗 Guruhga kirish: {group_link}",
        reply_markup=main_menu(user_id)
    )


@dp.callback_query(F.data == "add_group")
async def add_group_link(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("📎 Guruh linkini yuboring (masalan: https://t.me/mygroup):")
    await state.set_state(GroupState.group_link)


@dp.message(GroupState.group_link)
async def save_group_link(message: types.Message, state: FSMContext):
    link = message.text.strip()
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        await message.answer("❌ Sizda bu amalni bajarish uchun huquq yo‘q.")
        await state.clear()
        return
    cursor.execute("UPDATE users SET group_link = ? WHERE user_id = ?", (link, ADMIN_ID))
    conn.commit()
    await message.answer(f"✅ Guruh link saqlandi:\n<code>{link}</code>", reply_markup=back_menu())
    await state.clear()


@dp.callback_query(F.data == "back")
async def back_to_main(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id == ADMIN_ID:
        await callback.message.edit_text(
            "🔧 Admin paneliga xush kelibsiz!\nBu yerda siz referal guruh yoki kanal qo‘shishingiz mumkin.",
            reply_markup=admin_start_menu()
        )
        return

    cursor.execute("SELECT group_link FROM users WHERE user_id = ?", (ADMIN_ID,))
    admin_group = cursor.fetchone()
    group_link = admin_group[0] if admin_group and admin_group[0] else None
    if not group_link:
        await callback.message.edit_text("Admin hali guruh linkini qo‘shmagan.", reply_markup=main_menu(user_id))
        return

    await callback.message.edit_text(
        f"🏠 Asosiy menyu\n\n"
        f"📨 Sizning referal havolangiz:\n"
        f"<code>https://t.me/{(await bot.get_me()).username}?start={user_id}</code>\n\n"
        f"👥 Siz orqali kelganlar soni: {get_referral_count(user_id)} ta\n\n"
        f"🔗 Guruh: {group_link}",
        reply_markup=main_menu(user_id)
    )


@dp.callback_query(F.data == "ref_stats")
async def show_ref_stats(callback: types.CallbackQuery):
    stats = get_referral_stats()
    if not stats:
        await callback.message.edit_text("📊 Hozircha foydalanuvchilar mavjud emas.", reply_markup=admin_start_menu())
        return

    text = "📊 <b>Referal statistika:</b>\n\n"
    for row in stats:
        name = row["full_name"] or "Noma’lum"
        count = row["referrals"]
        text += f"👤 <b>{name}</b> — {count} ta odam\n"
    await callback.message.edit_text(text, reply_markup=admin_start_menu())


@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def on_user_join(event: types.ChatMemberUpdated):
    new_user = event.new_chat_member.user
    new_user_id = new_user.id
    if new_user_id in temp_referrals:
        referrer_id = temp_referrals.pop(new_user_id)
        cursor.execute("UPDATE users SET referrals = referrals + 1 WHERE user_id = ?", (referrer_id,))
        conn.commit()
        try:
            await bot.send_message(referrer_id, f"🎉 Sizning referalingiz ({new_user.full_name}) guruhga qo‘shildi!")
        except:
            pass
