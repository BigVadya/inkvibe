import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
import datetime
from tattoo_price import (
    start_tattoo_price, process_size, process_location, process_style, process_overlap, TattooPriceFSM
)

API_TOKEN = os.getenv('BOT_TOKEN') or 'TOKEN'

# --- FSM States ---
class Register(StatesGroup):
    fio = State()
    age = State()
    master = State()
    date = State()
    time = State()

# --- DB ---
async def init_db():
    async with aiosqlite.connect('tattoo.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            fio TEXT,
            age INTEGER
        )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            master TEXT,
            date TEXT,
            time TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS deleted_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            master TEXT,
            date TEXT,
            time TEXT,
            deleted_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )''')
        await db.commit()

# --- Bot ---
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

MASTERS = ["Алексей", "Мария", "Иван"]
TIMES = ["10:00", "12:00", "14:00", "16:00"]

@dp.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with aiosqlite.connect('tattoo.db') as db:
        async with db.execute("SELECT fio, age FROM users WHERE user_id=?", (user_id,)) as c:
            user = await c.fetchone()
    if user:
        # Уже зарегистрирован — показываем меню профиля
        class DummyCallback:
            def __init__(self, message):
                self.from_user = message.from_user
                self.message = message
        await show_profile_menu(DummyCallback(message), show_message=False)
    else:
        await message.answer('Добро пожаловать в тату-студию! Давайте зарегистрируемся. Введите ваше ФИО:')
        await state.set_state(Register.fio)

@dp.message(Register.fio)
async def process_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await message.answer("Введите ваш возраст:")
    await state.set_state(Register.age)

@dp.message(Register.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (10 <= int(message.text) <= 100):
        await message.answer("Пожалуйста, введите корректный возраст (10-100):")
        return
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    user_id = message.from_user.id
    fio = data.get("fio")
    age = data.get("age")
    # Сохраняем пользователя в БД
    async with aiosqlite.connect('tattoo.db') as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id, fio, age) VALUES (?, ?, ?)", (user_id, fio, age))
        await db.commit()
    await state.clear()
    # Показываем меню профиля
    class DummyCallback:
        def __init__(self, message):
            self.from_user = message.from_user
            self.message = message
    await show_profile_menu(DummyCallback(message), show_message=False)

@dp.callback_query(lambda c: c.data.startswith("master:"), Register.master)
async def process_master(callback: types.CallbackQuery, state: FSMContext):
    master = callback.data.split(":", 1)[1]
    await state.update_data(master=master)
    days = [
        (datetime.date.today() + datetime.timedelta(days=i)).strftime('%d.%m.%Y')
        for i in range(1, 4)
    ]
    builder = InlineKeyboardBuilder()
    for d in days:
        builder.button(text=d, callback_data=f"date:{d}")
    builder.button(text="⬅️ Назад", callback_data="back_to_master")
    await callback.message.edit_text(f"Мастер: {master}\nВыберите дату:", reply_markup=builder.as_markup())
    await state.set_state(Register.date)

@dp.callback_query(lambda c: c.data == "back_to_master", Register.date)
async def back_to_master_from_date(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    for m in MASTERS:
        builder.button(text=m, callback_data=f"master:{m}")
    builder.button(text="⬅️ Назад", callback_data="profile")
    await callback.message.edit_text("Выберите мастера:", reply_markup=builder.as_markup())
    await state.set_state(Register.master)

@dp.callback_query(lambda c: c.data.startswith("date:"), Register.date)
async def process_date(callback: types.CallbackQuery, state: FSMContext):
    date = callback.data.split(":", 1)[1]
    await state.update_data(date=date)
    builder = InlineKeyboardBuilder()
    for t in TIMES:
        builder.button(text=t, callback_data=f"time:{t}")
    builder.button(text="⬅️ Назад", callback_data="back_to_date")
    await callback.message.edit_text(f"Дата: {date}\nВыберите время:", reply_markup=builder.as_markup())
    await state.set_state(Register.time)

@dp.callback_query(lambda c: c.data == "back_to_date", Register.time)
async def back_to_date_from_time(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    master = data.get("master")
    days = [
        (datetime.date.today() + datetime.timedelta(days=i)).strftime('%d.%m.%Y')
        for i in range(1, 4)
    ]
    builder = InlineKeyboardBuilder()
    for d in days:
        builder.button(text=d, callback_data=f"date:{d}")
    builder.button(text="⬅️ Назад", callback_data="back_to_master")
    await callback.message.edit_text(f"Мастер: {master}\nВыберите дату:", reply_markup=builder.as_markup())
    await state.set_state(Register.date)

@dp.callback_query(lambda c: c.data.startswith("time:"), Register.time)
async def process_time(callback: types.CallbackQuery, state: FSMContext):
    time = callback.data.split(":", 1)[1]
    data = await state.get_data()
    user_id = callback.from_user.id
    fio = data.get("fio")
    age = data.get("age")
    master = data.get("master")
    date = data.get("date")
    # Проверяем занятость
    async with aiosqlite.connect('tattoo.db') as db:
        async with db.execute("SELECT 1 FROM records WHERE master=? AND date=? AND time=?", (master, date, time)) as c:
            busy = await c.fetchone()
        if busy:
            await callback.answer("Это время уже занято у выбранного мастера!", show_alert=True)
            return
        await db.execute("INSERT OR IGNORE INTO users (user_id, fio, age) VALUES (?, ?, ?)", (user_id, fio, age))
        await db.execute("INSERT INTO records (user_id, master, date, time) VALUES (?, ?, ?, ?)", (user_id, master, date, time))
        await db.commit()
    await state.clear()
    await show_profile_menu(callback, show_message=True)

async def show_profile_menu(callback, show_message=False):
    user_id = callback.from_user.id
    async with aiosqlite.connect('tattoo.db') as db:
        async with db.execute("SELECT fio, age FROM users WHERE user_id=?", (user_id,)) as c:
            user = await c.fetchone()
        async with db.execute("SELECT id, master, date, time FROM records WHERE user_id=? ORDER BY id DESC", (user_id,)) as c:
            records = await c.fetchall()
    if not user:
        await callback.message.edit_text("Вы не зарегистрированы.")
        return
    fio, age = user
    text = f"<b>👤 Ваш профиль</b>\n" \
           f"<b>ФИО:</b> {fio}\n" \
           f"<b>Возраст:</b> {age}\n\n" \
           f"<b>🗓 Ваши записи:</b>\n"
    if records:
        for i, (rec_id, master, date, time) in enumerate(records, 1):
            text += f"<b>{i}.</b> {master} — <i>{date} {time}</i>\n"
    else:
        text += "<i>Нет записей.</i>"
    builder = InlineKeyboardBuilder()
    builder.button(text="🆕 Новая запись", callback_data="new_record")
    if records:
        builder.button(text="❌ Отменить запись", callback_data="cancel_record")
    builder.button(text="🕓 История", callback_data="history")
    builder.button(text="💰 Примерная стоимость татуировки", callback_data="tattoo_price")
    builder.adjust(2)  # Делаем по 2 кнопки в ряд
    if show_message:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())
    else:
        await callback.message.answer(text, parse_mode="HTML", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data == "profile")
async def show_profile(callback: types.CallbackQuery):
    await show_profile_menu(callback, show_message=True)

@dp.callback_query(lambda c: c.data == "new_record")
async def new_record(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    async with aiosqlite.connect('tattoo.db') as db:
        async with db.execute("SELECT fio, age FROM users WHERE user_id=?", (user_id,)) as c:
            user = await c.fetchone()
    if not user:
        await callback.message.edit_text('Давайте зарегистрируемся! Введите ваше ФИО:')
        await state.set_state(Register.fio)
    else:
        builder = InlineKeyboardBuilder()
        for m in MASTERS:
            builder.button(text=m, callback_data=f"master2:{m}")
        builder.button(text="⬅️ Назад", callback_data="profile")
        await callback.message.edit_text("Выберите мастера:", reply_markup=builder.as_markup())
        await state.set_state(Register.master)

@dp.callback_query(lambda c: c.data.startswith("master2:"), Register.master)
async def process_master2(callback: types.CallbackQuery, state: FSMContext):
    master = callback.data.split(":", 1)[1]
    await state.update_data(master=master)
    days = [
        (datetime.date.today() + datetime.timedelta(days=i)).strftime('%d.%m.%Y')
        for i in range(1, 4)
    ]
    builder = InlineKeyboardBuilder()
    for d in days:
        builder.button(text=d, callback_data=f"date2:{d}")
    builder.button(text="⬅️ Назад", callback_data="back_to_master2")
    await callback.message.edit_text(f"Мастер: {master}\nВыберите дату:", reply_markup=builder.as_markup())
    await state.set_state(Register.date)

@dp.callback_query(lambda c: c.data == "back_to_master2", Register.date)
async def back_to_master2_from_date(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    for m in MASTERS:
        builder.button(text=m, callback_data=f"master2:{m}")
    builder.button(text="⬅️ Назад", callback_data="profile")
    await callback.message.edit_text("Выберите мастера:", reply_markup=builder.as_markup())
    await state.set_state(Register.master)

@dp.callback_query(lambda c: c.data.startswith("date2:"), Register.date)
async def process_date2(callback: types.CallbackQuery, state: FSMContext):
    date = callback.data.split(":", 1)[1]
    await state.update_data(date=date)
    builder = InlineKeyboardBuilder()
    for t in TIMES:
        builder.button(text=t, callback_data=f"time2:{t}")
    builder.button(text="⬅️ Назад", callback_data="back_to_date2")
    await callback.message.edit_text(f"Дата: {date}\nВыберите время:", reply_markup=builder.as_markup())
    await state.set_state(Register.time)

@dp.callback_query(lambda c: c.data == "back_to_date2", Register.time)
async def back_to_date2_from_time(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    master = data.get("master")
    days = [
        (datetime.date.today() + datetime.timedelta(days=i)).strftime('%d.%m.%Y')
        for i in range(1, 4)
    ]
    builder = InlineKeyboardBuilder()
    for d in days:
        builder.button(text=d, callback_data=f"date2:{d}")
    builder.button(text="⬅️ Назад", callback_data="back_to_master2")
    await callback.message.edit_text(f"Мастер: {master}\nВыберите дату:", reply_markup=builder.as_markup())
    await state.set_state(Register.date)

@dp.callback_query(lambda c: c.data.startswith("time2:"), Register.time)
async def process_time2(callback: types.CallbackQuery, state: FSMContext):
    time = callback.data.split(":", 1)[1]
    data = await state.get_data()
    user_id = callback.from_user.id
    master = data.get("master")
    date = data.get("date")
    # Проверяем занятость
    async with aiosqlite.connect('tattoo.db') as db:
        async with db.execute("SELECT 1 FROM records WHERE master=? AND date=? AND time=?", (master, date, time)) as c:
            busy = await c.fetchone()
        if busy:
            await callback.answer("Это время уже занято у выбранного мастера!", show_alert=True)
            return
        await db.execute("INSERT INTO records (user_id, master, date, time) VALUES (?, ?, ?, ?)", (user_id, master, date, time))
        await db.commit()
    await state.clear()
    await show_profile_menu(callback, show_message=True)

@dp.callback_query(lambda c: c.data == "cancel_record")
async def cancel_record(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    async with aiosqlite.connect('tattoo.db') as db:
        async with db.execute("SELECT id, master, date, time FROM records WHERE user_id=? ORDER BY id DESC", (user_id,)) as c:
            records = await c.fetchall()
    if not records:
        await callback.message.edit_text("У вас нет записей.")
        return
    builder = InlineKeyboardBuilder()
    for rec_id, master, date, time in records:
        builder.button(text=f"{master} — {date} {time}", callback_data=f"delrec:{rec_id}")
    builder.button(text="⬅️ Назад", callback_data="profile")
    await callback.message.edit_text("Выберите запись для отмены:", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data.startswith("delrec:"))
async def delete_record(callback: types.CallbackQuery):
    rec_id = int(callback.data.split(":", 1)[1])
    async with aiosqlite.connect('tattoo.db') as db:
        async with db.execute("SELECT user_id, master, date, time FROM records WHERE id=?", (rec_id,)) as c:
            rec = await c.fetchone()
        if rec:
            user_id, master, date, time = rec
            deleted_at = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
            await db.execute("INSERT INTO deleted_records (user_id, master, date, time, deleted_at) VALUES (?, ?, ?, ?, ?)", (user_id, master, date, time, deleted_at))
        await db.execute("DELETE FROM records WHERE id=?", (rec_id,))
        await db.commit()
    await callback.answer("Запись отменена!", show_alert=True)
    await show_profile_menu(callback, show_message=True)

@dp.callback_query(lambda c: c.data == "history")
async def show_history(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    async with aiosqlite.connect('tattoo.db') as db:
        async with db.execute("SELECT master, date, time, deleted_at FROM deleted_records WHERE user_id=? ORDER BY deleted_at DESC", (user_id,)) as c:
            records = await c.fetchall()
    text = "<b>🕓 История удалённых записей</b>\n"
    if records:
        for i, (master, date, time, deleted_at) in enumerate(records, 1):
            text += f"<b>{i}.</b> {master} — <i>{date} {time}</i> (удалено: {deleted_at})\n"
    else:
        text += "<i>Нет удалённых записей.</i>"
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data="profile")
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data == "tattoo_price")
async def tattoo_price_start(callback: types.CallbackQuery, state: FSMContext):
    await start_tattoo_price(callback.message, state)

@dp.callback_query(lambda c: c.data.startswith("tattoo_size:"), TattooPriceFSM.size)
async def tattoo_price_size(callback: types.CallbackQuery, state: FSMContext):
    await process_size(callback, state)

@dp.callback_query(lambda c: c.data.startswith("tattoo_location:"), TattooPriceFSM.location)
async def tattoo_price_location(callback: types.CallbackQuery, state: FSMContext):
    await process_location(callback, state)

@dp.callback_query(lambda c: c.data.startswith("tattoo_style:"), TattooPriceFSM.style)
async def tattoo_price_style(callback: types.CallbackQuery, state: FSMContext):
    await process_style(callback, state)

@dp.callback_query(lambda c: c.data.startswith("tattoo_overlap:"), TattooPriceFSM.overlap)
async def tattoo_price_overlap(callback: types.CallbackQuery, state: FSMContext):
    await process_overlap(callback, state)

# --- Main ---
def main():
    asyncio.run(init_db())
    asyncio.run(dp.start_polling(bot))

if __name__ == '__main__':
    main() 